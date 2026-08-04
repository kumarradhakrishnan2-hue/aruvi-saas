# The C1–C14 cycle, in plain English

A companion to `docs/testing.md` §4. Same fourteen steps, no jargon — what each one asks and
why it exists. The formal wording in `testing.md` and the tracker stays the authority; this is
the version you read when you want to remember *the point*.

**Who does what:** **[You]** runs things in Terminal · **[Claude]** reads and checks · **[Both]**
means you drive the app and I read the result.

---

## First, the words this cycle keeps using

**A chapter's library** — the same chapter written three times at three lengths. For VIII ch 3
that is 16, 13 and 10 lessons. Every version is complete on its own, with its own questions.

**Serving** — what happens when a teacher says "I have 12 lessons for this chapter." The
software picks the closest version it already has and adapts it. No AI runs at that moment; it
is selection and arithmetic, which is why it is free and instant.

**Borrowing / a fill** — when the teacher's number lands *between* two versions. We take the
shorter version and borrow a lesson from another version to make up the difference.

**The synthesis lesson** — the final wrap-up lesson that only the longest version has. It is
the one lesson designed to pull the whole chapter together, so it is the natural thing to borrow
when a teacher's plan is nearly complete.

**The register** — three things the teacher-facing text must never do: state a number of minutes
inside the lesson text, point forward to "the next lesson", or mention days and dates. All three
break because the same lesson gets served at different lengths, in different orders, to
different teachers.

**A defect** — a logged problem with a severity. S1 stops everything, S2 is something a teacher
would see and call wrong, S3 is a rule breach they wouldn't notice, S4 is cosmetic.

---

## C1 · Build it **[You]**

Generate the three versions with the AI and confirm they landed.

*The point:* this is the only step that spends money, so everything after it is checking work
that has already been paid for. It also confirms the basics — three files, the right lengths, the
app can see the chapter.

## C2 · What did it cost **[Claude]**

Add up the tokens and rupees for this chapter, including any re-runs.

*The point:* one chapter's price times 330 chapters is the number that decides whether the whole
corpus is affordable. Two chapters in, the figure has already moved 28%, which is exactly why we
count rather than assume.

## C3 · Did the AI follow the rulebooks **[Claude]**

Read the longest version and one short version against every rule in both constitutions — the
lesson-plan one and the assessment one — and mark each rule pass or fail with a quote.

*The point:* the rulebooks are the product. And it has to be *two* versions, because a rulebook
that only holds when the AI has plenty of room hasn't been proven. On this chapter that worry ran
both ways: some rules broke only on the long version, one broke only on the short.

## C4 · The old untested worries **[Claude]**

We keep a running list of "we changed this, but only checked it on paper, never on a real
generation." This step works through the entries that apply to this subject.

*The point:* it is very easy to edit a rulebook, confirm the saved files still look right, and
never find out whether the AI actually obeys the new wording. This is the step that catches that.

## C5 · Read the automatic report **[Claude]**

The build already ran a long list of machine checks. Read the report and confirm every line says
PASS, and that the quarantine folder is empty.

*The point:* the machine checks the things a human reads past — that no section got skipped, that
lessons appear in the right order, that every requested length can actually be served. If a file
failed, it was moved to quarantine, and a quarantined file must never reach a teacher.

## C6 · Try it as a teacher would **[You]**

Call the app the way the real product does, asking for several different lesson counts: exactly
what a version holds, something in between, one more than the longest, one below the shortest,
and a mixed week.

*The point:* everything before this tested files. This tests the actual path a teacher takes, and
it is the first step that needs the three test logins set up.

## C7 · Read the words a teacher will read **[Claude]**

Scan every teacher-facing sentence for the three banned things.

*The point:* a stray "for four minutes" or "in the next lesson" is quietly wrong for whoever gets
that lesson at a different length or in a different position. Cheap to find, invisible until a
teacher hits it.

## C8 · The join **[Claude]**

Where a borrowed lesson was spliced in, read the lesson *before* it and the lesson *itself*, in
full, one after the other, the way a teacher meets them on two consecutive days. Rate each join:
reads fine, slightly rough but harmless, or genuinely jumpy.

*The point:* this join is the single thing that killed two earlier versions of the architecture.
Both times the machine checks said everything was fine and only reading it as a teacher revealed
the problem. If one step in this cycle earns its keep, it is this one.

## C9 · Questions point at the right lesson **[Claude]**

Check that every assessment question is attached to the lesson it belongs to after the plan has
been reshuffled — and that a question whose lesson didn't make the cut says so instead of
attaching itself somewhere wrong.

*The point:* a question silently landing on the wrong day is exactly the kind of error a teacher
sees and we don't.

## C10 · Files behave **[Claude]**

Names follow the convention, asking twice returns the cached copy rather than rebuilding, older
files aren't disturbed, and a quarantined file is invisible to serving.

*The point:* mostly it protects the teacher from having her plan rewritten underneath her
mid-chapter, and protects us from serving a file we've already condemned.

## C11 · Speed **[Claude]**

Time one uncached request.

*The point:* the whole reason serving is selection instead of generation is that it should take
milliseconds. If it doesn't, the design premise is wrong. Over 5 seconds is a defect.

## C12 · The downloads **[Both]**

Export the lesson plan, the assessment and the combined document as PDF and Word, plus the
allocation report, and open all eight.

*The point:* many teachers will print rather than read on screen. A borrowed lesson has to read as
one whole lesson on paper, with nothing blank and no raw code showing.

## C13 · Error messages **[Both]**

Deliberately ask for impossible things — a chapter with no plan, sixty periods, a broken file —
and read what comes back.

*The point:* when something goes wrong the teacher should get a sentence she understands, not a
crash or a wall of code.

## C14 · Copyright **[Claude]**

Check that nothing has been lifted from the textbook wholesale, that no third-party material
(poems, lyrics, images) has been reproduced, and that anything genuinely quoted is attributed.

*The point:* we are generating material from copyrighted textbooks and putting it in front of
teachers. Paraphrase is the expectation; a lifted passage is a real liability, not a style note.

## SIGN · You decide **[You]**

Everything above passing is the *precondition*, not the verdict. I present four things and you
rule: the table of what every possible lesson count gets a teacher (and what it loses), the
roughest join from C8 read out in full, the synthesis lesson in full, and each short version's
ending — does the compression still teach, or has it collapsed into a summary lecture?

*The point:* no amount of machine checking can tell you whether a lesson is worth teaching. This
step is never self-approved, and it never gets skipped.
