# End-of-chapter section attribution, mathematics IX, chapters 5-8.
# Format: chapter -> item id -> (book_ref, dominant, all_sections|None, why)
# book_ref is copied verbatim from the summary JSON and is a match guard.
# Every ref below is a real member of that chapter's summary sections[];
# all_sections is in sections[] order and always contains `dominant`.
#
# Read against the textbook PDFs in textbooks/mathematics/ix/. Chapters 5, 7, 8
# check out against the book. CHAPTER 6 DOES NOT — see its banner below.
#
# ── ch 5 · I'm Up and Down, and Round and Round ───────────────────────────────
# section -> technique map (PDF pp.93-117; the whole EoC set was parked on 5.8):
#   5.1   Definitions        : circle as locus, centre, RADIUS, chord, diameter.
#                              "all radii are equal" is the isosceles-triangle lever.
#   5.2   Symmetries         : full rotational symmetry; every diameter is a line of
#                              reflection symmetry; the diameter is the longest chord.
#   5.3   How Many Circles?  : the centres of ALL circles through A, B lie on the
#                              perpendicular bisector of AB (locus argument); unique
#                              circle through 3 non-collinear points; circumcircle.
#   5.4   Chords & the angles: T2 equal chords => equal angles at the centre; T3 the
#         they subtend         converse (SSS / SAS congruence of the two radii triangles).
#   5.5   Midpoints & perp.  : T4 centre-to-midpoint is PERPENDICULAR to the chord;
#         bisectors of chords  T5 the perpendicular from the centre BISECTS the chord.
#   5.6   Distance of chords : "distance" = perpendicular distance to the midpoint;
#         from the centre      T6 equal chords are equidistant; T7 the converse.
#   5.6.1 Which unequal chord: T8 the longer chord is the nearer one; and — at the TAIL
#         is farther           of the section (Ex. Set 5.5 Q2, p.105) — the explicit
#                              relation r^2 = d^2 + (c/2)^2, i.e. chord = 2*sqrt(r^2-d^2).
#                              This is the arithmetic engine of Q1/Q3/Q4/Q9/Q18.
#   5.7   Angles subtended   : arc, major/minor arc, and the angle an arc subtends AT
#         by an arc            THE CENTRE (defined as the swept angle).
#   5.7.1 Angle at a point on: T9 central angle = 2 x angle at a point on the circle
#         the circle outside   outside the arc; COROLLARY angle in a semicircle = 90 deg;
#         the arc              angles in the same segment are equal.
#   5.8   Concyclicity       : T10 equal angles on the same side => concyclic; cyclic
#                              quadrilateral; T11 opposite angles sum to 180 deg; T12 converse.
#
# ── ch 6 · Measuring Space: Perimeter and Area ────────────────────────────────
# !! DO NOT TRUST / DO NOT APPLY WITHOUT RE-AUTHORING. The ch-6 summary does not
# !! describe the ch-6 textbook chapter AT ALL. The book (PDF pp.118-154) runs
# !! 6.1 Perimeter of a Shape · 6.2 Perimeter of a Circle - the C/D Ratio ·
# !! 6.3 pi Is Irrational · 6.4 Length of an Arc · 6.5 Problems, Puzzles and
# !! Paradoxes on Perimeter · 6.6 Area of a Rectangle · 6.7 Area of a
# !! Parallelogram · 6.8 Area of a Triangle (6.8.1 Heron's formula) ·
# !! 6.9 Squaring a Rectangle · 6.10 Area of a Circle (6.10.1 Area of a Sector).
# !! The summary's sections[], prose_summary, worked examples, exercise sets, page
# !! numbers and end-of-chapter items are all fabricated (they read like an NCERT
# !! Heron's-formula + areas-of-pathways chapter). The book's 16 unstarred EoC
# !! questions (pp.149-152: area models of identities, isosceles/right-triangle
# !! area and perimeter, Heron two-ways, wheel revolutions, quadrant from
# !! circumference, trapezium and kite area, side-scaling, circles packed in a
# !! rectangle) have NO overlap with the summary's 9 items. The entries below are
# !! therefore attribution INTERNAL TO THE FABRICATED SUMMARY only: each
# !! description mapped onto the summary's own section list
# !!   6.2 recap of perimeter/area formulas · 6.8 pathways (borders, crossroads) ·
# !!   6.9 circular paths / rings · 6.10 combinations of plane figures
# !! They repair nothing real. Ch 6 needs re-running through the chapter skill.
#
# ── ch 7 · The Mathematics of Maybe: Introduction to Probability ──────────────
# section -> technique map (PDF pp.155-173):
#   7.1   What is Probability : probability as a MEASUREMENT of likelihood; random
#                               events; subjective probability.
#   7.1.1 Randomness          : random experiment / trial - outcomes known, result not.
#   7.1.2 The Probability Scale: 0 = impossible, 1 = certain, 0.5 = even chance;
#                               ranking and LABELLING events along the scale.
#   7.2   Measuring objectively: the two objective routes (evidence vs theory).
#   7.2.1 Experimental prob.  : outcome / sample-space vocabulary first appears here;
#                               P = times occurred / trials; RELATIVE FREQUENCY.
#   7.2.2 Theoretical prob.   : P = favourable / possible under EQUALLY LIKELY
#                               outcomes; the letters-of-a-word count (Example 4).
#   7.2.3 Statistical data    : probability read off survey counts / a grouped
#                               frequency table; sampling up to a population;
#                               law of large numbers; gambler's fallacy.
#   7.3 / 7.3.1 Sample Space  : S, its elements, sample size n(S); TABULATING S for a
#                               two-stage experiment (the Coin1/Coin2/Outcome table).
#   7.3.2 Events              : an event as a SUBSET of S - "at least one head",
#                               "greater than 4", and complements.
#   7.4   Tree Diagrams       : multi-step experiments; a tree to enumerate S and read
#                               probabilities off the branches.
#
# ── ch 8 · Predicting What Comes Next: Sequences and Progressions ─────────────
# section -> technique map (PDF pp.174-196):
#   8.1   Introduction to seq.: a sequence as an ordered list; terms and positions.
#   8.2   Explicit Rule       : t_n as a formula in n; substitute n for any term, or
#                               solve t_n = value to find a position.
#   8.3   Recursive Rule      : t_n from t_(n-1) (and deeper back-references).
#   8.4   Arithmetic Progress.: common difference d; t_n = a + (n-1)d; RECOVERING a
#                               and d from two given terms (Ex. Set 8.2 Q4 pattern).
#   8.4.1 Visualising an AP   : stage/value table -> (x, y) plot -> collinear points.
#   8.5   Sum of first n nat. : n(n+1)/2, triangular numbers, AP-sum word problems.
#   8.6   Geometric Progress. : common ratio r; t_n = a*r^(n-1).
#   8.6.1 Fun with Fractals   : Sierpinski-style stage areas as a GP.
#   8.6.2 Visualising a GP    : GP tables/graphs, decay (bouncing-ball) modelling.
# Only Q1 and Q2 are unstarred, and both are the same 8.4 technique.

CH5_8 = {
    5: {
        "E-22": ("End of Chapter Q1, p.114", "5.6", ["5.5", "5.6", "5.6.1"],
                 "r = 13, d = 5, so the half-chord is sqrt(169-25) = 12 and the chord is 24 cm. "
                 "Theorem 5 (5.5) is what makes the foot of the perpendicular the midpoint, 5.6 "
                 "supplies the 'distance of a chord from the centre' frame, and the "
                 "r^2 = d^2 + (c/2)^2 relation is written out at the tail of 5.6.1 "
                 "(Ex. Set 5.5 Q2). Nothing here touches arcs, angles or concyclicity."),
        "E-23": ("End of Chapter Q2, p.114", "5.7.1", ["5.7", "5.7.1"],
                 "The given 70 deg is the angle the arc subtends AT THE CENTRE, which is the "
                 "sweep definition of 5.7; halving it to 35 deg is Theorem 9, stated and proved "
                 "in 5.7.1. No chord arithmetic at all."),
        "E-24": ("End of Chapter Q3, p.114", "5.6", ["5.5", "5.6", "5.6.1"],
                 "Halving the given diameter gives r = 13; the 24 cm chord is bisected by the "
                 "perpendicular from the centre (Theorem 5, 5.5), so d = sqrt(169-144) = 5. Same "
                 "5.6 / 5.6.1 right triangle as Q1, solved for the distance instead of the chord."),
        "E-25": ("End of Chapter Q4, p.114", "5.6", ["5.5", "5.6", "5.6.1"],
                 "r = 15 and d = 9 give chord = 2*sqrt(225-81) = 24 cm - a direct application of "
                 "the 2*sqrt(r^2-d^2) formula from 5.6.1's exercise set, on the 5.6 "
                 "perpendicular-distance set-up, with the bisection coming from 5.5."),
        "E-26": ("End of Chapter Q5, p.114", "5.5", ["5.3", "5.5"],
                 "Two routes, both in the chapter: the centre is equidistant from the chord's "
                 "endpoints, hence on the locus 5.3 identifies as the perpendicular bisector; or "
                 "Theorem 4 (5.5) makes the centre-to-midpoint line perpendicular to the chord, "
                 "i.e. the perpendicular bisector. 5.5 is dominant - it is the theorem the "
                 "chapter has just proved and the Ex. Set 5.3 Q1 converse the question echoes."),
        "E-27": ("End of Chapter Q6, p.114", "5.7.1", ["5.7", "5.7.1"],
                 "angle ACB = 90 deg. The arc AB not containing C subtends a straight angle at "
                 "the centre (the 5.7 sweep definition) and Theorem 9 halves it - the corollary "
                 "stated in 5.7.1. 'Explain your reasoning' asks for exactly that chain."),
        "E-28": ("End of Chapter Q7, p.114", "5.8", None,
                 "Both parts are Theorem 11 alone - opposite angles of a cyclic 4-gon sum to "
                 "180 deg, giving angle C = 105 deg and angle D = 70 deg."),
        "E-29": ("End of Chapter Q8, p.114", "5.8", None,
                 "(2x+10) + (3x-20) = 180 by Theorem 11, so x = 38, angle P = 86 deg and "
                 "angle R = 94 deg. Only the cyclic-quadrilateral angle sum of 5.8, plus routine "
                 "linear-equation work from an earlier chapter."),
        "E-30": ("End of Chapter Q9, p.114", "5.6", ["5.5", "5.6", "5.6.1"],
                 "Half-chord 8 and d = 6 give r = 10 - the 5.6 / 5.6.1 right triangle solved for "
                 "the hypotenuse, once Theorem 5 (5.5) has supplied the bisection."),
        "E-31": ("End of Chapter Q10, p.114", "5.8", ["5.7.1", "5.8"],
                 "Sides in order 5, 5, 12, 12 make a cyclic kite. The two angles that lie between "
                 "a 5 and a 12 are equal (congruent triangles across the axis) and, by Theorem 11 "
                 "(5.8), sum to 180 deg - so each is 90 deg. The diagonal joining them is "
                 "therefore a diameter (the semicircle corollary of 5.7.1) and the area is two "
                 "right triangles: 2 x 1/2 x 5 x 12 = 60 square units."),
        "E-32": ("End of Chapter Q18, p.115", "5.6", ["5.5", "5.6", "5.6.1"],
                 "With distances d and d+7 and half-chords 12 and 5: 144 + d^2 = 25 + (d+7)^2 "
                 "gives d = 5 and r = 13. Needs Theorem 5's bisection (5.5), the "
                 "perpendicular-distance frame of 5.6, and Theorem 8 of 5.6.1 to know the 24 cm "
                 "chord is the nearer of the two same-side chords (which fixes d vs d+7)."),
        "E-33": ("End of Chapter Q20, p.115", "5.7.1", ["5.7.1", "5.8"],
                 "angle MOP and angle MNP both stand on chord MP with O and N on the same arc, so "
                 "they are equal - angles in the same segment, the standing consequence of "
                 "Theorem 9 in 5.7.1. MN being a diameter additionally forces angle MPN = 90 deg "
                 "by the same section's semicircle corollary; the inscribed-quadrilateral setting "
                 "is 5.8's."),
        "E-34": ("End of Chapter Q21, p.115", "5.8", None,
                 "angle CDE = 180 deg - angle CDA = angle ABC follows from Theorem 11 plus the "
                 "straight angle at D. The exterior-angle property of a cyclic quadrilateral is "
                 "wholly inside 5.8."),
        "E-35": ("End of Chapter Q24, p.116", "5.7.1", ["5.1", "5.7.1"],
                 "In Fig. 5.30 a and b split the angle at A, and OA = OB = OC are radii (the 5.1 "
                 "definition), so both triangles are isosceles; the angle sum of the big triangle "
                 "gives 2(a+b) = 180, i.e. a+b = 90 deg. It justifies 5.7.1's semicircle "
                 "corollary WITHOUT using Theorem 9 - the radii-equal fact of 5.1 is the lever."),
        "E-36": ("End of Chapter Q26, p.116", "5.8", ["5.7.1", "5.8"],
                 "Fig. 5.31 joins the centre, giving p, q at the circumference and u, v at O. "
                 "Theorem 9 (5.7.1) gives u = 2p and v = 2q, and u + v = 360 deg then yields "
                 "p + q = 180 deg - the proof of Theorem 11, which is the 5.8 statement being "
                 "justified."),
    },
    # See the ch-6 banner above: the summary does not match the textbook. These
    # tuples are internally consistent with the (fabricated) descriptions and
    # sections[] only, and should not be applied as a repair.
    6: {
        "E-26": ("End of Chapter Q1, p.121", "6.8", ["6.2", "6.8"],
                 "Uniform border round a rectangular lawn: outer minus inner rectangle, solved "
                 "for the width - the pathway decomposition the summary puts in 6.8, on 6.2's "
                 "rectangle-area recap. UNVERIFIABLE: no such question in the book (its EoC Q1, "
                 "p.149, asks for area models of algebraic identities) - see the ch-6 banner."),
        "E-27": ("End of Chapter Q2, p.121", "6.8", ["6.2", "6.8"],
                 "Two crossroads through a rectangular park, with the overlapping square "
                 "subtracted once - the crossroads case named in the summary's 6.8, on 6.2's "
                 "rectangle-area recap. UNVERIFIABLE: no such question in the book (see banner)."),
        "E-28": ("End of Chapter Q3, p.122", "6.9", None,
                 "Ring between two concentric circles, pi(R^2 - r^2) with R = r + width - exactly "
                 "the summary's 6.9 and nothing else. UNVERIFIABLE: no such question in the book "
                 "(see banner)."),
        "E-29": ("End of Chapter Q4, p.122", "6.9", None,
                 "Same circular-ring area as Q3, then multiplied by a rate to get a cost - the "
                 "summary's 6.9 covers both the ring and its cost problems. UNVERIFIABLE: no such "
                 "question in the book (see banner)."),
        "E-30": ("End of Chapter Q5, p.122", "6.10", ["6.2", "6.10"],
                 "Rectangle plus semicircle on one side: decompose, add - the composite-figure "
                 "method of the summary's 6.10, using the recap formulas of 6.2. UNVERIFIABLE: no "
                 "such question in the book (see banner)."),
        "E-31": ("End of Chapter Q6, p.122", "6.10", ["6.2", "6.10"],
                 "Square plus triangle: decompose into the two known shapes and add - the "
                 "summary's 6.10 on 6.2's square/triangle formulas. UNVERIFIABLE: no such "
                 "question in the book (see banner)."),
        "E-32": ("End of Chapter Q7, p.123", "6.10", ["6.2", "6.10"],
                 "Plot shaped as a rectangle plus a triangle from given measurements - the same "
                 "6.10 decomposition, with 6.2 supplying base x height and 1/2 base x height. "
                 "UNVERIFIABLE: no such question in the book (see banner)."),
        "E-33": ("End of Chapter Q8, p.123", "6.10", ["6.2", "6.10"],
                 "Decorative/floor design built from several plane shapes - repeated 6.10 "
                 "decomposition with additions and subtractions over 6.2's formulas. "
                 "UNVERIFIABLE: no such question in the book (see banner)."),
        "E-34": ("End of Chapter Q9, p.123", "6.10", ["6.2", "6.10"],
                 "Total area of a composite figure converted into a material cost or quantity - "
                 "6.10's decomposition plus a rate, on 6.2's formulas. UNVERIFIABLE: no such "
                 "question in the book (see banner)."),
    },
    7: {
        "E-13": ("End of Chapter Q1, p.169-170", "7.1.2", ["7.1.2", "7.2.2", "7.3.1"],
                 "Four blanks across the chapter: (i) 0 and (iii) 1 are the two endpoints of the "
                 "probability scale (7.1.2 - two of the four, hence dominant); (ii) 'sample "
                 "space' is the object of 7.3.1 (first named in passing in 7.2.1); (iv) 1/2 for "
                 "heads is the equally-likely theoretical ratio of 7.2.2."),
        "E-14": ("End of Chapter Q2, p.170", "7.2.1", ["7.2.1", "7.2.3"],
                 "The blank wants the words 'relative frequency' and its value 15/50 = 0.3; both "
                 "the term and the formula are defined in 7.2.1. The 50-student survey is the "
                 "collected-data setting of 7.2.3, whose Example 5 is itself a 50-student survey."),
        "E-15": ("End of Chapter Q3, p.170", "7.2.2", ["7.1.2", "7.2.2"],
                 "The question is a validity test for 7.2.2's equally-likely assumption: the fair "
                 "coin (ii) and fair die (iii) pass, while a car starting (i) and a draw from 3 "
                 "red / 7 blue marbles judged by colour (iv) do not, and (v) is only "
                 "approximately even. The 'equally likely / even chance' vocabulary the "
                 "explanations must use is set up on the scale in 7.1.2."),
        "E-16": ("End of Chapter Q4, p.170", "7.3.1", ["7.2.2", "7.3.1", "7.3.2", "7.4"],
                 "All five parts demand the sample space IN WRITING (7.3.1, dominant - it is the "
                 "instruction repeated five times) and then P = favourable/possible (7.2.2). "
                 "(i) 'at least one head' and (iii) 'greater than 4' are 7.3.2's own worked "
                 "events, and (iv) 'not red' is a complement; (v)'s eight-outcome three-coin "
                 "space is most easily built by extending the two-coin tree of 7.4."),
        "E-17": ("End of Chapter Q5, p.170", "7.2.2", None,
                 "One draw from three distinguishable candies: P(strawberry) = 1/3 straight from "
                 "the equally-likely ratio of 7.2.2. The three outcomes are read off directly and "
                 "no further machinery is used."),
        "E-18": ("End of Chapter Q6, p.171", "7.3.1", ["7.3.1", "7.4"],
                 "Listing all 2 x 3 = 6 shirt-and-pants outfits IN A TABLE is the two-stage "
                 "sample-space enumeration of 7.3.1, whose two-coin example uses exactly that "
                 "Coin1/Coin2/Outcome table; 7.4's tree is the chapter's alternative route to the "
                 "same multi-step enumeration. No probability is asked for."),
        "E-19": ("End of Chapter Q7, p.171", "7.2.3", ["7.2.1", "7.2.3"],
                 "A grouped frequency table of 1000 recorded cases: 20/1000, (210+325)/1000 and "
                 "445/1000. That is relative frequency (7.2.1) applied to past statistical data, "
                 "which is 7.2.3's whole subject and where reading probabilities off collected "
                 "data is taught."),
        "E-20": ("End of Chapter Q8, p.171", "7.2.2", ["7.2.2", "7.3.2"],
                 "PEACE is the letters-of-a-word count of 7.2.2's Example 4 (PROBABILITY): "
                 "P(P, E or C) = 4/5. Part (ii) 'not an E' = 3/5 is a complementary event, i.e. "
                 "the subset-of-S view of 7.3.2."),
    },
    8: {
        "E-29": ("End of Chapter Q1, p.194", "8.4", None,
                 "t11 = 38 and t16 = 73 give a + 10d = 38 and a + 15d = 73, so d = 7, a = -32 and "
                 "t31 = 178. Pure t_n = a + (n-1)d work - the same two-equations move as Ex. Set "
                 "8.2 Q4 inside 8.4. No GP, no sum formula, no visualisation."),
        "E-30": ("End of Chapter Q2, p.194", "8.4", None,
                 "a + 2d = 16 and t7 - t5 = 2d = 12 give d = 6 and a = 4, so the AP is 4, 10, 16, "
                 "22, ... Again only the common difference and nth-term formula of 8.4."),
    },
}
