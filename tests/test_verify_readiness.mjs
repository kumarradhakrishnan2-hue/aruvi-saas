/* Read-after-write verification — the readiness comparator (founder doctrine, 2026-08-10).
 *
 * The mechanism is only worth having if the comparator is EXACTLY as strict as the teacher's
 * intent and no stricter. A false alarm teaches her to ignore the warning, which leaves her
 * worse off than no check at all. So this suite is mostly about what must NOT fire.
 *
 *   node tests/test_verify_readiness.mjs
 */
import { verifiedWrite, readinessFingerprint, planIsPrepared, planIsArchived,
         sectionStateMatches } from "../web/app/lib/verify.js";

let fails = 0;
const ok = (label, cond, detail = "") => {
  if (cond) console.log(`  ok    ${label}`);
  else { fails++; console.log(`  FAIL  ${label}${detail ? " — " + detail : ""}`); }
};

const profile = (over = {}) => [{
  name: "Mathematics",
  grades: [{
    grade: "IX",
    sections: [{ tag: "9A", sec: "A" }, { tag: "9B", sec: "B" }],
    durations: [50],
    periods_per_week: 7,
    ...over,
  }],
}];

console.log("MUST NOT FIRE — differences the teacher did not make");
ok("identical", readinessFingerprint(profile()) === readinessFingerprint(profile()));
ok("section order",
   readinessFingerprint(profile()) ===
   readinessFingerprint([{ name: "Mathematics", grades: [{ grade: "IX",
     sections: [{ tag: "9B", sec: "B" }, { tag: "9A", sec: "A" }],
     durations: [50], periods_per_week: 7 }] }]));
ok("subject order",
   readinessFingerprint([...profile(), { name: "Science", grades: [] }]) ===
   readinessFingerprint([{ name: "Science", grades: [] }, ...profile()]));
ok("grade case (VIII vs viii)",
   readinessFingerprint([{ name: "M", grades: [{ grade: "ix", sections: [], durations: [], periods_per_week: 1 }] }]) ===
   readinessFingerprint([{ name: "M", grades: [{ grade: "IX", sections: [], durations: [], periods_per_week: 1 }] }]));
ok("duration order",
   readinessFingerprint(profile({ durations: [60, 50] })) ===
   readinessFingerprint(profile({ durations: [50, 60] })));
ok("ppw as string vs number",
   readinessFingerprint(profile({ periods_per_week: "7" })) === readinessFingerprint(profile()));
ok("budget / ppw-split changes are ignored (derived, not her edit)",
   readinessFingerprint([{ ...profile()[0], budget: { method: "weeks", value: 30 } }]) ===
   readinessFingerprint(profile()));

console.log("\nMUST FIRE — facts she actually changed");
ok("a section removed",
   readinessFingerprint(profile()) !==
   readinessFingerprint(profile({ sections: [{ tag: "9A", sec: "A" }] })));
ok("a duration changed",
   readinessFingerprint(profile()) !== readinessFingerprint(profile({ durations: [45] })));
ok("periods per week changed",
   readinessFingerprint(profile()) !== readinessFingerprint(profile({ periods_per_week: 8 })));
ok("a whole subject dropped",
   readinessFingerprint([...profile(), { name: "Science", grades: [] }]) !==
   readinessFingerprint(profile()));
ok("the profile emptied entirely",
   readinessFingerprint(profile()) !== readinessFingerprint([]));

console.log("\nTHE THREE OUTCOMES");
const want = readinessFingerprint(profile());
const expect = (y) => readinessFingerprint(y.subjects) === want;

const r1 = await verifiedWrite({
  write: async () => {},
  read: async () => ({ subjects: profile() }),
  expect,
});
ok('server agrees -> "ok"', r1.status === "ok", r1.status);

const r2 = await verifiedWrite({
  write: async () => {},
  read: async () => ({ subjects: profile({ periods_per_week: 3 }) }),
  expect,
});
ok('server disagrees -> "mismatch"', r2.status === "mismatch", r2.status);

const r3 = await verifiedWrite({
  write: async () => {},
  read: async () => { throw new Error("network"); },
  expect,
});
ok('server unreachable -> "unverified", NOT an error', r3.status === "unverified", r3.status);

const r4 = await verifiedWrite({
  write: async () => { throw new Error("500"); },     // the POST fails …
  read: async () => ({ subjects: profile() }),        // … but the write landed
  expect,
});
ok('a throwing write with a landed value -> "ok" (the read is the arbiter)',
   r4.status === "ok", r4.status);

const r5 = await verifiedWrite({
  write: async () => {},
  read: async () => ({ subjects: profile() }),
  expect: () => { throw new Error("bad comparator"); },
});
ok('a throwing comparator -> "unverified", never a false alarm', r5.status === "unverified", r5.status);

console.log("\nAREA 2 · the lesson is mine");
ok("present, object register",
   planIsPrepared({ "mathematics/ix/ch_04_50m13.json": {} }, "mathematics", "ix", "ch_04_50m13.json"));
ok("present, array register",
   planIsPrepared([{ key: "mathematics/ix/a.json" }], "mathematics", "ix", "a.json"));
ok("absent -> false", !planIsPrepared({}, "mathematics", "ix", "a.json"));
ok("another teacher's grade does not count",
   !planIsPrepared({ "mathematics/viii/a.json": {} }, "mathematics", "ix", "a.json"));

console.log("\nAREA 3 · archived / restored (the same fact, inverted)");
ok("archived", planIsArchived({ "science/ix/p.json": {} }, "science", "ix", "p.json"));
ok("restored", !planIsArchived({}, "science", "ix", "p.json"));

console.log("\nAREAS 4+5 · the section card");
const S = { science_ix_9A: { chapter: "ch_08.json", done: false } };
ok("attached to the right chapter",
   sectionStateMatches(S, "science_ix_9A", { chapter: "ch_08.json" }));
ok("attached to a DIFFERENT chapter -> mismatch",
   !sectionStateMatches(S, "science_ix_9A", { chapter: "ch_09.json" }));
ok("attach is not failed by a done flag it never set",
   sectionStateMatches(S, "science_ix_9A", { chapter: "ch_08.json" }));
ok("mark complete, server still false -> mismatch",
   !sectionStateMatches(S, "science_ix_9A", { chapter: "ch_08.json", done: true }));
ok("mark complete, server true -> ok",
   sectionStateMatches({ science_ix_9A: { chapter: "ch_08.json", done: true } },
                       "science_ix_9A", { chapter: "ch_08.json", done: true }));
ok("unbind: no row is what we wanted",
   sectionStateMatches({}, "science_ix_9A", { chapter: null }));
ok("unbind: a surviving row -> mismatch",
   !sectionStateMatches(S, "science_ix_9A", { chapter: null }));
ok("a section we never touched is not judged",
   sectionStateMatches(S, "science_ix_9B", { chapter: null }));

console.log(fails ? `\n${fails} FAILURE(S)` : "\nall verification checks passed");
process.exit(fails ? 1 : 0);
