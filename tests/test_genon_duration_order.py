"""Duration ordering — the week, not the row (partition v0.4).

A duration matrix is a bag. The teacher's timetable is a repeating week. These
tests hold the four properties that turn one into the other:

  1. the weekly cycle is recovered from the counts and repeated;
  2. the shortest duration opens the week;
  3. longer periods sit in the interior, never at an edge of a week;
  4. no two long periods are adjacent — across the week boundary either.

Run: python3 tests/test_genon_duration_order.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.genon.partition import _spread, order_durations  # noqa: E402

FAILED = []


def check(label, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + label + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILED.append(label)


def runs(seq, value):
    """Lengths of the maximal runs of `value`, including empty runs at the edges."""
    out, n = [], 0
    for x in seq:
        if x == value:
            out.append(n)
            n = 0
        else:
            n += 1
    out.append(n)
    return out


print("\n── 1. the founder's worked example: SS IX, 7x50 + 2x60 weekly ──")
# She picks 18 periods for the partitioned plan. The profile ratio scales to
# 14 x 50 + 4 x 60 — two of her weeks.
seq = order_durations([(50, 14), (60, 4)])
check("18 periods total", len(seq) == 18, str(len(seq)))
check("14 fifties and 4 sixties",
      (seq.count(50), seq.count(60)) == (14, 4), str((seq.count(50), seq.count(60))))
check("the week repeats verbatim", seq[:9] == seq[9:], str(seq))
check("the week is 50 50 60 50 50 50 60 50 50",
      seq[:9] == [50, 50, 60, 50, 50, 50, 60, 50, 50], str(seq[:9]))
check("no two long periods adjacent (week boundary included)",
      all(not (seq[i] == 60 and seq[i + 1] == 60) for i in range(len(seq) - 1)), str(seq))
check("sequence opens and closes on the shortest duration",
      seq[0] == 50 and seq[-1] == 50)
check("total minutes unchanged", sum(seq) == 50 * 14 + 60 * 4, str(sum(seq)))

print("\n── 2. row order and split rows do not change the sequence ──")
check("rows typed longest-first give the same sequence",
      order_durations([(60, 4), (50, 14)]) == seq)
check("a duration typed as two rows aggregates",
      order_durations([(50, 10), (60, 4), (50, 4)]) == seq)

print("\n── 3. a single duration is untouched ──")
check("17 x 50 stays 17 x 50", order_durations([(50, 17)]) == [50] * 17)
check("empty matrix is empty", order_durations([]) == [])
check("zero and negative rows are dropped",
      order_durations([(50, 12), (60, 0), (0, 3)]) == [50] * 12)

print("\n── 4. dispersion properties across many mixed matrices ──")
# The engine recovers the week as counts / gcd(counts), which may be FINER than the
# week the teacher happens to think in: 9 x 45 + 3 x 60 reduces to a 3+1 cycle, not
# 9+3. That is deliberate — the finer cycle is the more dispersed arrangement, and
# without weekday data we cannot tell the two apart anyway. So the test derives the
# cycle from the sequence and asserts the properties on whatever cycle the engine chose.


def cycle_of(seq):
    """Shortest prefix the sequence is a whole repetition of."""
    for c in range(1, len(seq) + 1):
        if len(seq) % c == 0 and all(seq[i:i + c] == seq[:c] for i in range(0, len(seq), c)):
            return seq[:c]
    return list(seq)


cases = [(7, 2, 2), (5, 1, 3), (6, 3, 2), (9, 3, 1), (4, 1, 5), (8, 2, 3), (11, 4, 2)]
for short, long_, weeks in cases:
    s = order_durations([(45, short * weeks), (60, long_ * weeks)])
    cyc = cycle_of(s)
    label = f"{short}x45 + {long_}x60 per week, {weeks} week(s)"
    ok_len = len(s) == (short + long_) * weeks
    ok_counts = (s.count(45), s.count(60)) == (short * weeks, long_ * weeks)
    ok_edges = cyc[0] == 45 and cyc[-1] == 45
    ok_adj = all(not (s[i] == 60 and s[i + 1] == 60) for i in range(len(s) - 1))
    gaps = runs(cyc, 60)
    ok_even = max(gaps) - min(gaps) <= 1          # short runs as equal as arithmetic allows
    check(label, ok_len and ok_counts and ok_edges and ok_adj and ok_even,
          f"len={len(s)} counts_ok={ok_counts} edges_ok={ok_edges} adj_ok={ok_adj} "
          f"cycle={cyc} gaps={gaps}")

print("\n── 5. three durations ──")
s3 = order_durations([(40, 10), (50, 5), (60, 5)])
check("20 periods, counts preserved",
      len(s3) == 20 and (s3.count(40), s3.count(50), s3.count(60)) == (10, 5, 5), str(s3))
check("the shortest duration opens", s3[0] == 40, str(s3[:4]))
check("longest never adjacent to itself",
      all(not (s3[i] == 60 and s3[i + 1] == 60) for i in range(len(s3) - 1)), str(s3))

print("\n── 6. degenerate: more long periods than short ones can separate ──")
# Adjacency here is arithmetic, not a choice — the engine must still return a
# well-formed sequence with the right counts rather than crash or drop periods.
s4 = order_durations([(50, 2), (60, 10)])
check("counts preserved when the long duration is the majority",
      len(s4) == 12 and s4.count(50) == 2 and s4.count(60) == 10, str(s4))
check("the two short periods are spread, not clumped",
      abs(s4.index(50) - (len(s4) - 1 - s4[::-1].index(50))) > 1, str(s4))

print("\n── 7. _spread puts the remainder in the middle ──")
check("_spread(7, 2) == [2, 3, 2]", _spread(7, 2) == [2, 3, 2], str(_spread(7, 2)))
check("_spread(14, 4) sums to 14 and varies by at most 1",
      sum(_spread(14, 4)) == 14 and max(_spread(14, 4)) - min(_spread(14, 4)) <= 1,
      str(_spread(14, 4)))
check("_spread(9, 0) == [9]", _spread(9, 0) == [9])

print("\n" + ("ALL PASS" if not FAILED else f"{len(FAILED)} FAILED: {FAILED}"))
sys.exit(1 if FAILED else 0)
