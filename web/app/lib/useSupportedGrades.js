"use client";
import { useEffect, useState } from "react";
import { ALL_GRADES, fetchSupportedGrades } from "./format";

/* Shared hook: the grades a subject supports (intersected with the master list), used by BOTH
 * the setup flow (Readiness) and the editor (MyClasses) so the coverage rule lives in one place.
 * Returns the allowed grade list for `subjectName`; falls back to ALL_GRADES until the fetch
 * resolves (so the UI never flashes empty), then narrows to the supported set. */
export default function useSupportedGrades(subjectName) {
  const [byName, setByName] = useState({});   // { subjectName: ["VI",…] }
  useEffect(() => {
    if (!subjectName || byName[subjectName]) return;
    let live = true;
    fetchSupportedGrades(subjectName).then((ups) => {
      if (live) setByName((m) => ({ ...m, [subjectName]: ups }));
    });
    return () => { live = false; };
  }, [subjectName, byName]);
  const supported = byName[subjectName];
  return supported ? ALL_GRADES.filter((g) => supported.includes(g)) : ALL_GRADES;
}
