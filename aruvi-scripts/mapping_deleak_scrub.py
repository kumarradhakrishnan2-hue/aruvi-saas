import json, re, sys


PRE = [
    (r"(?i)\bRemove this competency and the chapter has no purpose left\b", "Without it the chapter has no purpose left"),
    (r"[;,]?\s*it does not qualify for a higher weight[^;.]*", ""),

    (r"\ban architecturally distinct,? named section\b", "a self-contained section"),
    (r"\barchitecturally distinct,? named sections\b", "separate sections"),
    (r"\barchitecturally distinct,? named section\b", "self-contained section"),

    (r"\ban architecturally distinct section\b", "a self-contained section"),
    (r"\barchitecturally distinct sections\b", "separate sections"),
    (r"\barchitecturally distinct section\b", "self-contained section"),

    (r"\bthe substantive Weight\s*3\b", "the chapter's central focus"),
    (r"\bnamed structural elements\b", "parts of the chapter"),
    (r"\bnamed structural element\b", "part of the chapter"),

    (r"\bplacing it at Weight\s*1\b", "keeping it a supporting mention"),
    (r"\bplacing it at Weight\s*2\b", "keeping it a major strand"),

    (r"^As a section that could stand alone as a learning unit on\b", "This section could be taught as a lesson in its own right on"),
    (r"\bmatching (C-\d+\.\d+) at Weight\s*3\b", r"making \1 the chapter's central focus"),
    (r"\bmatching (C-\d+\.\d+) at Weight\s*2\b", r"making \1 a major strand"),
    (r"\bmatching (C-\d+\.\d+) at Weight\s*1\b", r"making \1 a supporting mention"),
    (r",?\s*and as the C-code of the sub-discipline governing the chapter's primary structural activity \(([^)]+)\)[^,.;]*", r", and \1 is the discipline the chapter is built around"),

    # ---------- added pass 5 ----------
    (r"^[A-Z][A-Za-z ]{2,30} sub-discipline\.?$", ""),
    (r",?\s*(?:thus\s+|thereby\s+)?(?:satisfying|meeting|which satisfies|and satisfies|it satisfies|which meets|and meets)\s+Rules?\s*\d+(?:\s*\([a-z]\))?(?:\s*and\s*(?:Rules?\s*)?\d*\s*\([a-z]\))?(?:\s+for\s+Weight\s*[123])?", ""),
    (r"\bBoth sections could stand as independent learning units\b", "Either could be taught as a lesson in its own right"),
    (r"\bcould stand as (?:an )?independent learning units?\b", "could be taught as a lesson in its own right"),
    (r"\bit receives Weight\s*2 rather than Weight\s*3\b", "it is a major strand rather than the chapter's central focus"),
    (r"\breceives Weight\s*3\b", "is treated as the chapter's central focus"),
    (r"\breceives Weight\s*2\b", "is treated as a major strand"),
    (r"\breceives Weight\s*1\b", "is treated as a supporting mention"),
    (r"\btakes Weight\s*3\b", "is the chapter's central focus"),
    (r"\btakes Weight\s*2\b", "is a major strand"),
    (r"\btakes Weight\s*1\b", "is a supporting mention"),
    (r"\bRule\s*7 permits Weight\s*3 for this[^,.;]*", "this is where the chapter's central focus sits"),

    # standalone rule verdicts -> delete the sentence entirely
    (r"^Rules?\s*\d+(?:\s*\([a-z]\))?(?:\s*(?:and|,)\s*(?:Rules?\s*)?\d+(?:\s*\([a-z]\))?)*\s+(?:is|are)\s+(?:satisfied|met)(?:\s+and\s+Rules?\s*\d+(?:\s*\([a-z]\))?\s+is\s+not)?(?:\s+(?:on|by)\s+[^.]*)?\.?$", ""),
    # leading rule verdict + colon -> strip the prefix, keep the substance
    (r"^Rules?\s*\d+(?:\s*\([a-z]\))?(?:\s*and\s*\d+(?:\s*\([a-z]\))?)*\s+(?:is|are)\s+(?:both\s+)?(?:satisfied|met)\s*[:,]\s*", ""),
    (r"^Rules?\s*\d+(?:\s*\([a-z]\))?\s+is\s+met\s+by\s+", "This is met by "),
    (r"^Rules?\s*\d+(?:\s*\([a-z]\))?\s+(?:is|are)\s+(?:satisfied|met)\s+and\s+", ""),
    (r",?\s*(?:so|and)\s+the competency does not reach a dedicated section or a Rules?\s*\d+\s*\([a-z]\)\s*thread", ", so it is not developed as a thread across sections"),
    (r"\bqualifying as present but not substantive\b", "so it is present but not a main focus"),
    (r"\bpresent but not substantive\b", "present but not a main focus"),
    (r"\bconfirming Weight\s*3 eligibility\b", "confirming it as the chapter's central focus"),
    (r"\bit is Weight\s*2,\s*not Weight\s*3\b", "it is a major strand rather than the chapter's central focus"),
    (r"\bso Weight\s*1 applies\b", "so it counts as a supporting mention"),
    (r"\blimiting this to Weight\s*1\b", "keeping it a supporting mention"),
    (r"\bmeeting the Weight\s*1 threshold\b", "keeping it a supporting mention"),
    (r"\bthe Weight\s*3 sits inside that cluster\b", "the chapter's central focus sits inside that cluster"),
    (r"\bThe primary sub-discipline is\b", "The chapter is primarily"),
    (r"\(([A-Za-z ]+?) sub-discipline\)", r"(a \1 competency)"),
    # dissolution, all phrasings
    (r"(?i)\b(?:complete removal of|removal of|removing|remove)\s+.{0,60}?dissolves?\b.{0,60}?(?=[,;.]|$)", "the chapter would have no purpose without it"),
    (r"(?i)\bdoes not (?:structurally )?dissolve\b.{0,60}?(?=[,;.]|$)", "is not the chapter's reason for being"),
    (r"(?i)\bthe chapter dissolves entirely\b", "the chapter has no purpose left"),
    (r"(?i)\bthe chapter's fundamental organising purpose dissolves\b", "the chapter has no purpose left"),
]

RULES = [
    # ---------- whole-clause deletions: explicit rule citations ----------
    (r",?\s*(?:and\s+)?(?:thus\s+|thereby\s+|so\s+)?(?:satisfying|meeting|which satisfies|and satisfies|it satisfies|which meets|and meets|matching[^,.;]*?at)\s+Rules?\s*\d+(?:\s*\([a-z]\))?(?:\s+for\s+Weight\s*[123])?", ""),
    (r"\s*[—–-]\s*Weight\s*[123]\s+under\s+Rules?\s*\d+", ""),
    (r",?\s*meeting the Weight\s*[123]\s+condition under Rules?\s*\d+", ""),
    (r",?\s*qualifying (?:it|them) for Weight\s*[123] under Rules?\s*[\d\s,and]+", ""),
    (r",?\s*(?:it\s+)?(?:alone\s+)?qualif(?:ies|y) for Weight\s*[123] under Rules?\s*[\d\s,and]+", ""),
    (r",?\s*(?:so|and)\s+no higher weight applies\s*\(Rules?\s*\d+\)", ""),
    (r"\s*\(Rules?\s*\d+[^)]*\)", ""),
    (r",?\s*under\s+Rules?\s*\d+(?:\s*\([a-z]\))?(?:\s*(?:and|,)\s*\d+)*", ""),
    (r",?\s*(?:as\s+)?(?:per|by)\s+Rules?\s*\d+(?:\s*\([a-z]\))?", ""),
    (r"\bRule\s*8's positional test is (?:also\s+)?satisfied,?\s*(?:since|as|because)\s*", "This is also the idea named in "),
    (r"\bRule\s*8's positional test resolves it against", "The tie is resolved against"),
    (r"\bRule\s*7 permits Weight\s*3 for this[^,.;]*", "this is the chapter's governing discipline"),
    (r"\bRule\s*7 permits Weight\s*3[^,.;]*", "this is the chapter's governing discipline"),
    (r"\bRule\s*7 restricts Weight\s*3 (?:away from|to)[^,.;]*", "the chapter's central focus lies elsewhere"),
    (r"\bRule\s*7 does not bar it,?\s*", ""),
    (r",?\s*(?:where|as|since)\s+CG-\d and CG-\d both approach the Weight\s*3 test[^,.;]*", ""),
    (r",?\s*as the second [A-Za-z]+ competency approaching the Weight\s*3 test", ""),
    (r"\bRules?\s*\d+(?:\s*\([a-z]\))?\b", "the mapping standard"),

    # ---------- weight machinery ----------
    (r"\bit is Central \(Weight\s*3\)", "it is the chapter's central focus"),
    (r"\bWeight\s*3\b", "central focus"),
    (r"\bWeight\s*2\b", "major strand"),
    (r"\bWeight\s*1\b", "supporting mention"),
    (r"\bweighted at 3\b", "treated as the chapter's central focus"),
    (r"\bweighted at 2\b", "treated as a major strand"),
    (r"\bweighted at 1\b", "treated as a supporting mention"),
    (r"\s*\(not [123]\)", ""),
    (r"\bthe competency is Present rather than Substantive\b", "it is present but not a main focus"),
    (r"\bthe competency is Present\b", "it is present but not a main focus"),
    (r"\bPresent rather than Substantive\b", "present but not a main focus"),
    (r",?\s*(?:so|and)\s+it does not qualify for a higher weight[^,.;]*", ""),
    (r",?\s*(?:so|and)\s+no higher weight applies", ""),
    (r",?\s*but as it is not the chapter's central organizing purpose it does not displace C-\d\.\d for central focus", ""),
    (r",?\s*it is held at major strand[^,.;]*behind", ", it sits behind"),

    # ---------- dissolution / structural test ----------
    (r"\bComplete removal of (?:this|the) competency (?:would\s+)?(?:structurally\s+)?dissolves?[^,.;]*", "This is what the chapter is fundamentally about"),
    (r"\bRemoval of this competency would dissolve[^,.;]*", "This is what the chapter is fundamentally about"),
    (r"\bRemoving it structurally dissolves the chapter", "Take this away and the chapter has no purpose"),
    (r"\bremoval of (?:this|the) competency would (?:structurally )?dissolve[^,.;]*", "the chapter would have no purpose without it"),
    (r"\bthe dissolution test\b", "the chapter's core purpose"),

    # ---------- constitution boilerplate echoes ----------
    (r"\bis developed substantively and deliberately across multiple named sections\b", "runs as a deliberate thread through several sections"),
    (r"\bis developed substantively across multiple named sections\b", "runs as a deliberate thread through several sections"),
    (r"\bdeveloped substantively and deliberately across multiple named sections\b", "developed as a deliberate thread through several sections"),
    (r"\bdeveloped substantively across multiple named sections\b", "developed as a deliberate thread through several sections"),
    (r"\bcould stand alone as a learning unit\b", "could be taught as a lesson in its own right"),
    (r"\bstand alone as a learning unit\b", "be taught as a lesson in its own right"),
    (r"\ba dedicated, architecturally distinct (?:named )?section\b", "a section of its own"),
    (r"\bdedicated, architecturally distinct\b", "self-contained"),
    (r"\barchitecturally distinct named sections?\b", "separate sections"),
    (r"\barchitecturally distinct sections?\b", "separate sections"),
    (r"\barchitecturally distinct and self-contained\b", "self-contained"),
    (r"\barchitecturally distinct\b", "self-contained"),
    (r"\bare architecturally met\b", "are met by the chapter's structure"),
    (r"\bthe sub-discipline governing the chapter's primary structural activity\b", "the discipline the chapter is built around"),
    (r"\bthe chapter's primary structural activity\b", "what the chapter is built around"),
    (r"\bprimary structural activity\b", "central activity"),
    (r"\bthe chapter's governing sub-discipline\b", "the discipline the chapter is built around"),
    (r"\bgoverning sub-discipline\b", "the discipline the chapter is built around"),
    (r"\bnamed structural elements?\b", "parts of the chapter"),
    (r"\bthe chapter's own organising logic makes\b", "the chapter itself makes"),
    (r"\bthe chapter's organising logic\b", "the way the chapter is built"),
    (r"\bshares? the chapter's overarching structural framework\b", "sits inside the chapter's main structure"),
    (r"\bovearching structural framework\b", "main structure"),
    (r"\boverarching structural framework\b", "main structure"),

    # ---------- classification vocabulary ----------
    (r"\bco-central\b", "equally central"),
    (r"\badjunct competency\b", "supporting competency"),
    (r"\bincidental scaffolding\b", "passing use"),
    (r"\bincidental mention\b", "passing mention"),
    (r"\bincidental illustration\b", "passing illustration"),
    (r"\bincidental appearance\b", "passing appearance"),
    (r"\bincidental computation\b", "passing computation"),
    (r"\bincidental number use\b", "passing number use"),
    (r"\bincidental vocabulary\b", "passing vocabulary"),
    (r"\bmerely incidental\b", "merely passing"),
    (r"\brather than incidental\b", "rather than passing"),
    (r"\bnot incidental\b", "not a passing reference"),
    (r"\bincidental\b", "passing"),
    (r"\bsubstantive rather than passing\b", "a real part of the work rather than a passing reference"),
    (r"\bsubstantively engages\b", "genuinely develops"),
    (r"\bsubstantively engaging\b", "genuinely developing"),
    (r"\bsubstantively addressed\b", "genuinely developed"),
    (r"\bsubstantively credits\b", "gives real space to"),
    (r"\bsubstantively engaging\b", "genuinely developing"),
    (r"\bsubstantive engagement with\b", "genuine work on"),
    (r"\bsubstantive use\b", "genuine use"),
    (r"\bsubstantive application\b", "genuine application"),
    (r"\bsubstantive pattern-recognition strand\b", "genuine pattern-recognition strand"),
    (r"\ba substantive\b", "a genuine"),
    (r"\bsubstantive,? independent strand\b", "an independent strand of genuine work"),
    (r"\bsubstantive\b", "genuine"),
    (r"\bsubstantively\b", "genuinely"),

    # ---------- added pass 2 ----------
    (r"\bit is Weight\s*2,\s*not Weight\s*3\b", "it is a major strand rather than the chapter's central focus"),
    (r"\bso Weight\s*1 applies\b", "so it counts as a supporting mention"),
    (r"\blimiting this to Weight\s*1\b", "keeping it a supporting mention"),
    (r"\bconfirming Weight\s*3 eligibility\b", "confirming it as the chapter's central focus"),
    (r"\bmeeting the Weight\s*1 threshold\b", "keeping it a supporting mention"),
    (r"\bpresent but not substantive\b", "present but not a main focus"),
    (r"\bRemove (?:this competency|C-\d+\.\d+) and the chapter[^,;.]*dissolves?[^,;.]*", "This is what the chapter is fundamentally about"),
    (r"(?:Complete r|R)emov(?:al of|ing)\s+[^,;.]{0,60}?dissolves?[^,;.]*second structural pillar[^,;.]*", "This is one of the two things the chapter is built on"),
    (r"(?:Complete r|R)emov(?:al of|ing)\s+[^,;.]{0,60}?dissolves?[^,;.]*", "This is what the chapter is fundamentally about"),
    (r"\bdoes not (?:structurally )?dissolve[^,;.]*", "is not the chapter's reason for being"),
    (r"\barchitecturally\s+", ""),

    # ---------- added pass 3 ----------
    (r"\bdeveloped substantively and deliberately across multiple architecturally distinct named sections\b", "developed as a deliberate thread across several self-contained sections"),
    (r"\ba dedicated, architecturally distinct named section\b", "a section of its own"),
    (r"\bdedicated, architecturally distinct named section\b", "section of its own"),
    (r"\barchitecturally distinct activity block\b", "self-contained activity block"),
    (r"\bTwo architecturally distinct named sections\b", "Two self-contained sections"),
    (r"\bso Weight\s*3 is not reached\b", "so it is not the chapter's central focus"),
    (r"\bRemove this competency and the chapter loses its organising purpose\b", "Without it the chapter loses its purpose"),
    (r"\bno second C-code within CG-\d is substantively addressed\b", "no second competency in this group is genuinely developed"),
    (r"\barchitecturally\s+", ""),

    # ---------- added pass 4 ----------
    (r"(?i)\bRemove this competency and the chapter has no organising purpose\b", "Without it the chapter has no purpose"),
    (r"(?i)\bRemove this competency and every named section collapses\b", "Every named section of the chapter depends on it"),
    (r"(?i)\bComplete removal of this competency would leave no chapter\b", "Without it there is no chapter"),
    (r"(?i)\bRemove this competency and no chapter remains\b", "Without it there is no chapter"),
    (r"\bmeet the standard for a second core competency\b", "make this a second main competency of the chapter"),
    (r"\bthe primary competency in play\b", "the main competency at work here"),
    (r"\bhas as its entire structural purpose\b", "is built entirely around"),
    (r"\bThe dedicated named section\b", "The section"),
    (r"\ba dedicated named section\b", "a section"),
    (r"\bdedicated named sections?\b", "section"),

    (r"\bthe (History|Geography|Political Science|Economics) sub-discipline\b", r"\1"),
    (r"\b(History|Geography|Political Science|Economics) sub-discipline\b", r"\1"),
    (r"\bthe primary sub-discipline\b", "the discipline the chapter is built around"),
]

CLEANUP = [
    (r"\b(because|since|as)\s*,\s*", r"\1 "),
    (r"\bdistinct, real\b", "distinct, genuine"),
    (r"\ban (?=self-contained|distinct)", "a "),
    (r"\bdoes not rise to major strand\b", "is not a major strand"),
    (r"^(?:Central|Substantive|Present|Contributory)\s*[—–-]\s*", ""),
    (r"\s{2,}", " "),
    (r"\s+([,.;:])", r"\1"),
    (r",\s*,", ","),
    (r",\s*\.", "."),
    (r";\s*\.", "."),
    (r"\s*[—–]\s*\.", "."),
    (r"^\s*[,;—–]\s*", ""),
    (r"\s*,\s*$", "."),
    (r"\s*;\s*$", "."),
]

TRIVIAL = re.compile(
    r"^(?:this|it|the section|the competency|both demands|together they|these|"
    r"they)?[\s,.;'\"—–]*$", re.I)



OVERRIDES = {
 "It then distinguishes substantive from procedural justice and the presumption of innocence as the mechanisms by which fairness is secured.":
   "It then distinguishes substantive from procedural justice and the presumption of innocence as the mechanisms by which fairness is secured.",

 "Complete removal of this competency structurally dissolves the chapter's organizing purpose, and because the chapter's primary structural activity explicitly crosses all four sub-disciplines (its purpose is the integrated field itself), Rule 7 permits Weight 3 for this cross-cutting integrative competency; Rule 8's positional test is also satisfied, since the field-and-its-disciplines idea is named in the chapter title and concluding synthesis.":
   "The chapter would have no purpose without it: its whole point is the integrated field, and it deliberately crosses all four disciplines. The chapter title and the concluding synthesis both name this idea.",
 "This substantive multi-section development satisfies Rule 5(b) for Weight 2, but as a cross-cutting competency outside the chapter's primary Political Science activity it does not qualify for Weight 3 under Rule 7.":
   "It runs as a deliberate thread through several sections, though the chapter's central focus stays on elections and political institutions.",
 "Complete removal of the competency defining production, distribution, and their influencing factors would structurally dissolve the chapter's organising purpose, qualifying it for Weight 3 under Rules 4 and 7; where CG-7 and CG-8 both approach the Weight 3 test, the definitional problem-of-choice and production core reserves the single Weight 3 for C-7.1 under Rule 8.":
   "The chapter would have no purpose without it — production, distribution and what shapes them are its central focus.",
 "This satisfies Rule 5(a) for Weight 2; as the second Economics competency approaching the Weight 3 test, it is held at Weight 2 under Rule 8 behind the chapter's central production-and-choice purpose (Rule 7 does not bar it, both codes being within the governing Economics sub-discipline).":
   "This is a major strand of the chapter, sitting just behind its central purpose of production and the problem of choice.",
 "These are named structural passages about institutions in the context of disaster response, qualifying as present but not substantive.":
   "Institutions appear in named passages about disaster response, but only in passing rather than as a developed theme.",
 "These are designated passages within landform sections rather than a dedicated section or architecturally distinct activity block, and the chapter enumerates resource endowments as a closing beat for each landform without comparing distribution and availability across regions as an analytical thread.":
   "Resources appear as a closing note inside each landform section rather than in a section or activity block of their own, and the chapter never compares availability across regions as a theme in its own right.",
 "Rule 6 is satisfied on the commodity and consumption elements of C-9.1.":
   "The chapter touches C-9.1 through its commodity and consumption material.",
 "Rule 6 is satisfied on C-6.2's services demand.":
   "The chapter touches C-6.2 through its material on services.",
}


def scrub(s):
    if s.strip() in OVERRIDES:
        return OVERRIDES[s.strip()]
    out = s
    for pat, rep in PRE:
        out = re.sub(pat, rep, out)
    for pat, rep in RULES:
        out = re.sub(pat, rep, out)
    for pat, rep in CLEANUP:
        out = re.sub(pat, rep, out)
    out = out.strip()
    if out and not out.endswith(('.', '!', '?', '"', "'")):
        out += '.'
    if out:
        out = out[0].upper() + out[1:]
    return out


if __name__ == '__main__':
    rows = json.load(open(sys.argv[1]))
    for r in rows:
        r['rewrite'] = scrub(r['text'])
    json.dump(rows, open(sys.argv[2], 'w'))
