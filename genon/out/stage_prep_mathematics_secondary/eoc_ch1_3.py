# End-of-chapter section attribution, mathematics IX, chapters 1-3.
# Format: chapter -> item id -> (book_ref, dominant, all_sections|None, why)
# book_ref is copied verbatim from the summary JSON and is a match guard.
#
# ch 1 - Orienting Yourself: The Use of Coordinates
#   section -> technique map:
#   1.1 Introduction        : history of grid thinking; Brahmagupta's zero + negative
#                             numbers as the precondition for a FOUR-quadrant plane.
#   1.2 Settling In         : informal scale model of a real space on a rectangular
#                             grid (Shalini's 1 cm : 1 ft pins-and-thread room plan).
#   1.3 The 2-D Cartesian   : axes, origin (0,0), sign convention, points on an axis
#       Coordinate System     (x,0)/(0,y), the four quadrants and their sign patterns,
#                             plotting (x,y), (x,y) != (y,x) unless x = y.
#   1.4 Distance Between    : distance along / parallel to an axis as a coordinate
#       Two Points            difference; the Baudhayana-Pythagoras distance formula
#                             sqrt((x2-x1)^2 + (y2-y1)^2); reflection of a figure in an
#                             axis and the invariance of side lengths under it.
#
# ch 2 - Introduction to Linear Polynomials
#   section -> technique map:
#   2.1 Introduction        : algebraic expressions, terms/variables/coefficients;
#                             univariate polynomials, DEGREE, and the names
#                             linear/quadratic/cubic/constant. (Ex. Set 2.1 = find the
#                             degree, write a polynomial of a given degree, name a
#                             coefficient.)
#   2.2 Linear Polynomials  : EVALUATING a polynomial at a value (the input-output /
#                             function view, incl. a quadratic in Ex. Set 2.2 Q2);
#                             forming a LINEAR EQUATION by equating a linear polynomial
#                             to a constant and solving word problems with it.
#   2.3 Exploring linear    : the nth term of a growing pattern as a linear expression;
#       patterns              constant common difference; "find a linear expression /
#                             linear pattern" for savings, decline, fare situations.
#   2.4 Linear growth and   : the same modelling written as a function C(d), h(t), with
#       linear decay          a table of values, and named growth vs decay.
#   2.5 Linear Relationships: y = ax + b; solving for a and b from two (x, y) data points.
#   2.6 Visualising linear  : plotting y = ax + b from two points; slope a; y-intercept
#       relationships         b; effect of varying a and b; parallel lines.
#
# ch 3 - The World of Numbers
#   section -> technique map (refs follow the SUMMARY's sections[] titles):
#   3.1  /3.1.1/3.1.2 : origins of counting; tally bones; ancient Indian number names.
#   3.2  /3.2.1/3.2.2 : zero as a number; whole numbers and closure; Brahmagupta's
#                       rules for zero.
#   3.3               : integers Z = naturals + zero + negatives.
#   3.3.1             : why negatives are needed (debt/fortune) and Brahmagupta's SIGN
#                       RULES for integer arithmetic (- x - = +, - x + = -).
#   3.4               : rational numbers as p/q, q != 0; equivalent fractions / rewriting
#                       two rationals over a COMMON DENOMINATOR; the four operations on
#                       rationals; closure; solving for an unknown rational.
#   3.4.1             : standard (lowest) form - p and q coprime, denominator positive.
#   3.4.2             : locating p/q on the number line by subdividing the unit interval;
#                       absolute value; DENSITY - finding rational numbers between two
#                       given rationals (average method / common-denominator method).
#   3.5               : irrational numbers - lengths not expressible as p/q, motivated by
#                       the diagonal sqrt(2) of a unit square via Baudhayana-Pythagoras.
#   3.5.1             : the historical discovery (Hippasus, the Pythagorean crisis).
#   3.5.2             : PROOF BY CONTRADICTION that sqrt(2) is irrational (and, per the
#                       Think-and-Reflect, the same argument for sqrt(3), sqrt(5), ...).
#   3.5.3             : constructing irrational lengths on the number line with
#                       right triangles and the square-root SPIRAL.
#   3.6               : real numbers = rationals + irrationals; decimal expansion as the
#                       signature that separates them.
#   3.6.1             : terminating vs non-terminating recurring decimals; the
#                       prime-factors-of-q (2s and 5s only) test WITHOUT dividing; number
#                       of decimal places; converting a terminating / pure-recurring /
#                       general-recurring decimal back to p/q.
#   3.6.2             : cyclic numbers (1/7 = 0.142857...).
#   3.6.3             : irrational decimals - non-terminating and non-repeating.
#   3.7               : conclusion - the N subset Z subset Q, R = Q union I hierarchy.

CH1_3 = {
    1: {
        "E-6": (
            "End of Chapter Q1, p.12",
            "1.3",
            None,
            "Asks for the coordinates of the point where the two axes meet - the origin "
            "(0, 0), which is defined only in 1.3 along with the axes themselves. No "
            "distance is computed, so 1.4 is not touched.",
        ),
        "E-7": (
            "End of Chapter Q2, p.12",
            "1.3",
            None,
            "H lies on the line through W parallel to the y-axis, so H = (-5, y): this is "
            "the (x, y) meaning of a coordinate as the perpendicular distance from the "
            "y-axis, taught in 1.3. Naming the quadrants H can lie in (II and III, for a "
            "negative x-coordinate) is 1.3's quadrant sign pattern.",
        ),
        "E-8": (
            "End of Chapter Q3, p.12",
            "1.3",
            ["1.3", "1.4"],
            "R(3,0) and A(0,-2) are the on-axis forms (x,0)/(0,y), and the perpendicular / "
            "axis-parallel sides of RAMP follow from shared coordinates - all 1.3. Part "
            "(iii), spotting that M(-5,-2) and P(-5,2) are mirror images in the x-axis, is "
            "the reflection-in-an-axis idea introduced in 1.4.",
        ),
        "E-9": (
            "End of Chapter Q4, p.12",
            "1.4",
            ["1.3", "1.4"],
            "Plotting Z(5,-6) in Quadrant IV and choosing I and N is 1.3, but the demand of "
            "the question - 'find the lengths of the three sides' - is the 1.4 distance "
            "work: two legs by coordinate difference and the hypotenuse by "
            "sqrt((x2-x1)^2+(y2-y1)^2).",
        ),
        "E-10": (
            "End of Chapter Q5, p.12",
            "1.3",
            ["1.1", "1.3"],
            "The answer turns on 1.3's sign convention - without negatives only Quadrant I "
            "exists, so points left of or below O cannot be named. 1.1 supplies the same "
            "claim historically ('without Brahmagupta's work the four-quadrant Cartesian "
            "plane would be impossible'), which is what the discussion is meant to recover.",
        ),
        "E-11": (
            "End of Chapter Q14, p.13",
            "1.3",
            ["1.2", "1.3"],
            "Part (i), drawing the 10x10 street grid at 1 cm = 200 m, is exactly 1.2's "
            "scaled grid model of a real space (Shalini's 1 cm : 1 ft room plan). Part (ii), "
            "why (4,3) and (3,4) each name exactly one crossing, tests 1.3's ordered-pair "
            "convention and its Think-and-Reflect that (x,y) = (y,x) only when x = y.",
        ),
        "E-12": (
            "End of Chapter Q15, p.14",
            "1.4",
            ["1.3", "1.4"],
            "Part (i) compares centre coordinates plus/minus the radius against the screen "
            "edges x = 0/800 and y = 0/600 - 1.3's reading of a coordinate as a "
            "perpendicular distance from an axis. Part (ii) needs the distance AB between "
            "(100,150) and (250,230) compared with 80 + 100, which is 1.4's distance "
            "formula and is the harder, deciding step.",
        ),
        "E-13": (
            "End of Chapter Q16, p.14",
            "1.4",
            ["1.3", "1.4"],
            "Plotting A(2,1), B(-1,2), C(-2,-1), D(1,-2) one per quadrant is 1.3, but "
            "proving ABCD is a square (four equal sides sqrt(10), equal diagonals) and "
            "computing its area both rest on 1.4's distance formula for segments parallel "
            "to neither axis.",
        ),
    },
    2: {
        "E-26": (
            "End of Chapter Q1, p.36",
            "2.1",
            None,
            "'Write a polynomial of degree 3 in x in which the coefficient of x^2 is -7' "
            "uses only the vocabulary defined in 2.1 - degree as the highest power, and the "
            "coefficient of a named term (cf. Ex. Set 2.1 Q2/Q3). Nothing linear, evaluated "
            "or graphed is involved.",
        ),
        "E-27": (
            "End of Chapter Q2, p.36",
            "2.2",
            None,
            "(i) 5x^2-3x+7 at x=1 and (ii) 4t^3-t^2+6 at t=a are pure substitution - the "
            "input-output/function view of a polynomial introduced in 2.2 and drilled in "
            "Ex. Set 2.2 Q1-Q2, which likewise evaluates a non-linear polynomial.",
        ),
        "E-28": (
            "End of Chapter Q3, p.37",
            "2.2",
            None,
            "Multiplying an unknown by 5/2 and adding 2/3 to get -7/12 is the formation of a "
            "linear equation by equating a linear polynomial to a constant, then solving it "
            "- 2.2's Example 6 and Ex. Set 2.2 word problems. The fractions add arithmetic, "
            "not a new section's method.",
        ),
        "E-29": (
            "End of Chapter Q4, p.37",
            "2.2",
            None,
            "Let the smaller number be x, the other 5x, then x+21 and 5x+21 with one twice "
            "the other: a single linear equation in one unknown, solved as in 2.2 "
            "(Example 6; Ex. Set 2.2 Q3-Q7 are the same species of two-quantity problem). "
            "No pattern, table or graph is required.",
        ),
        "E-30": (
            "End of Chapter Q5, p.37",
            "2.3",
            None,
            "'Find the amount after 6 months and 2 years and express this as a linear "
            "pattern' is Ex. Set 2.3 Q1 with different numbers - build the nth-term "
            "expression 800 + 250n for a sequence with constant difference and evaluate it "
            "at n = 6 and n = 24, which is precisely 2.3's method.",
        ),
    },
    3: {
        "E-25": (
            "End of Chapter Q1, p.65",
            "3.6.1",
            None,
            "Book Q1 converts 3/50 and 2/9 to decimals by long division, one terminating "
            "and one non-terminating recurring - the exact terminating-vs-repeating "
            "division work of 3.6.1 (Examples 2 and 3).",
        ),
        "E-26": (
            "End of Chapter Q2, p.65",
            "3.5.2",
            None,
            "Book Q2 is 'prove that sqrt(5) is an irrational number'. It reruns 3.5.2's "
            "eight-step proof by contradiction for sqrt(2), which its own Think-and-Reflect "
            "explicitly extends to sqrt(3), sqrt(5) and sqrt(7).",
        ),
        "E-27": (
            "End of Chapter Q3, p.65",
            "3.6.1",
            None,
            "Book Q3's nine parts convert decimals to p/q across all three of 3.6.1's "
            "cases: terminating (12.6, 0.0120), pure recurring (0.23-bar, 2.05-bar) and "
            "general recurring with a non-repeating head (3.052-bar, 1.235-bar, 2.125-bar, "
            "3.125-bar, 2.1625-bar).",
        ),
        "E-28": (
            "End of Chapter Q4, p.65",
            "3.4.2",
            ["3.4.2", "3.6.1"],
            "Book Q4 locates 0.532 and 1.15-bar (recurring) on the number line. The demand "
            "is 3.4.2's construction - subdivide the unit interval into q equal parts and "
            "step off p - but each decimal must first be turned into p/q (532/1000 and "
            "38/33) by 3.6.1's conversion, since 1.15-bar is recurring.",
        ),
        "E-29": (
            "End of Chapter Q5, p.65",
            "3.4.2",
            None,
            "Book Q5, 'find 6 rational numbers between 3 and 4', is pure density: 3.4.2's "
            "observation that a rational always sits between any two rationals, and its "
            "average / repeated-average method.",
        ),
        "E-30": (
            "End of Chapter Q6, p.65",
            "3.4.2",
            ["3.4", "3.4.2"],
            "Book Q6 asks for 5 rationals between 2/5 and 3/5. Density is 3.4.2, but unlike "
            "Q5 the numbers must first be rewritten over a larger common denominator "
            "(20/50 and 30/50) - the equivalent-fraction / same-denominator manipulation "
            "set out in 3.4.",
        ),
        "E-31": (
            "End of Chapter Q7, p.65",
            "3.4.2",
            ["3.4", "3.4.2"],
            "Book Q7 asks for 5 rationals between 1/6 and 2/5, whose denominators differ, so "
            "3.4's rule of expressing both over a common denominator (5/30 and 12/30, then "
            "scaled further) is genuinely required before 3.4.2's density argument delivers "
            "the five numbers.",
        ),
        "E-32": (
            "End of Chapter Q8, p.66",
            "3.4",
            None,
            "Book Q8 solves x/3 + x/5 = 16/15 for a rational x. It is 3.4's arithmetic of "
            "rational numbers - unlike denominators combined over a common denominator - "
            "matching Ex. Set 3.3 Q8, which likewise asks for 'the rational number x'.",
        ),
        "E-33": (
            "End of Chapter Q9, p.66",
            "3.4",
            ["3.3.1", "3.4"],
            "Book Q9 gives non-zero rationals with a + 1/b = 0 and asks for the sign of ab. "
            "One rewrites a = -1/b and multiplies to get ab = -1, which is 3.4's "
            "multiplication of rationals and the reciprocal; concluding that a positive "
            "times a negative is negative is 3.3.1's debt-and-fortune sign rule.",
        ),
        "E-34": (
            "End of Chapter Q10, p.66",
            "3.6.1",
            ["3.4.1", "3.6.1"],
            "Book Q10 shows a decimal terminating in the 4th place is p/10^4 with p not "
            "divisible by 10, then asks whether the lowest-form denominator must be "
            "divisible by 2^4 or 5^4. The 10^k = 2^k x 5^k reasoning is 3.6.1's "
            "prime-factor test; the second half turns on 3.4.1's lowest form (cancelling "
            "until p and q are coprime), and the answer is no - only one of 2^4, 5^4 need "
            "survive.",
        ),
        "E-35": (
            "End of Chapter Q11, p.66",
            "3.6.1",
            None,
            "Book Q11 decides, without dividing, whether 18/125 terminates and in how many "
            "places. 125 = 5^3, so it terminates in 3 places - a direct application of "
            "3.6.1's rule that q's only prime factors may be 2 and 5, and of the "
            "multiply-up-to-a-power-of-10 argument.",
        ),
        "E-36": (
            "End of Chapter Q12, p.66",
            "3.6.1",
            None,
            "Book Q12 gives a lowest-form denominator 2^3 x 5 and asks how many decimal "
            "places the expansion has. Multiplying to 2^3 x 5^3 = 10^3 gives 3 places - "
            "again 3.6.1's prime-factor argument; the lowest form is handed to the student, "
            "not derived, so 3.4.1 is not exercised.",
        ),
        "E-37": (
            "End of Chapter Q16, p.67",
            "3.5.3",
            ["3.5", "3.5.3"],
            "Book Q16 finds the hypotenuses of every right triangle in the square-root "
            "spiral (Fig. 3.14), giving sqrt(2), sqrt(3), sqrt(4), sqrt(5), ... - the spiral "
            "construction of irrational lengths in 3.5.3. The first triangle is the unit "
            "square's diagonal sqrt(2) from 3.5, which is where these lengths are shown to "
            "be irrational at all.",
        ),
    },
}
