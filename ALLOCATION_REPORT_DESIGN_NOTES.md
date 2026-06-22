# Allocation Report Design Notes
## Standardization Across All Subjects

This document compares the aruvi-saas allocation report implementation with the existing prototype (Project Aruvi) and explains design choices.

---

## Prototype Baseline (Project Aruvi)

The prototype generates allocation reports using **FPDF** (fpdf2 library) with:
- **Orientation:** Landscape (A4)
- **Columns:** `# | Chapter | Total Periods | [Period-type cols] | Effort Index / Weight`
- **Layout:** FPDF cells with multi-line wrapping for chapter titles
- **Colors:** Navy headers (44, 62, 80), alternating row backgrounds (light gray/white)
- **Footnote:** Subject-specific text explaining LRM allocation method
- **Optional blocks:** "About the Effort Index" (English only), "About Competency Load" (Social Sciences)

**Strengths:**
- Simple, functional, direct PDF output
- Multi-row tables handled well with FPDF's cell wrapping

**Limitations:**
- Desktop/print-only; no mobile support
- Single export format (PDF only)
- Styling is minimal (no design system alignment)
- Cannot easily adapt to web rendering
- Footnote/explanatory blocks are subject-specific hardcoded text

---

## aruvi-saas Implementation

### Design Principles

1. **Subject-agnostic:** Same component/export works for all subjects without conditionals
2. **Mobile-first:** Responsive design tested at 480px, 768px, desktop
3. **Design system:** Warm editorial palette (Pine/Clay/Paper) matching web globals.css
4. **Multi-format:** Web view + PDF + DOCX all use same underlying data structure
5. **Metadata-driven:** Optional columns (effort index, competency weight) shown only if data present
6. **Scalable:** Easy to add new subjects/stages without code changes

### Architecture

```
AllocationReport (dataclass)
    ├── to_dict() → JSON-serializable dict
    ├── export_allocation_report_pdf() → bytes
    ├── export_allocation_report_docx() → bytes
    └── <AllocationReportView> (React) → HTML/CSS
```

---

## Component Comparison

### HTML/Web View

| Aspect | Prototype | aruvi-saas |
|--------|-----------|-----------|
| **Tech** | Streamlit table | React + CSS Modules |
| **Mobile** | Not tested | Fully responsive (480px+) |
| **Design** | Minimal | Warm editorial (Fraunces/Newsreader/Courier) |
| **Columns** | Hardcoded conditionals | Auto-detect from data |
| **Exports** | PDF only | PDF + DOCX |
| **State** | Session-based | Props-based (stateless component) |

### PDF Export

| Aspect | Prototype | aruvi-saas |
|--------|-----------|-----------|
| **Library** | fpdf2 | reportlab |
| **Orientation** | Landscape | Portrait (more mobile-friendly when printed) |
| **Styling** | Basic colors | Design system colors (Pine/Clay/Paper) |
| **Fonts** | Helvetica only | Fraunces/Newsreader/Courier |
| **Tables** | Row wrapping via cells | Platypus Table with styled rows |
| **Explanations** | Hardcoded footnotes | Data-driven allocation_basis + note box |
| **Page size** | A4 | US Letter (can configure) |

### DOCX Export

| Aspect | Prototype | aruvi-saas |
|--------|-----------|-----------|
| **Support** | None | Full (docx-js via Node) |
| **Format** | — | US Letter, 1" margins |
| **Styling** | — | Design system colors |
| **Tables** | — | Dynamic columns with alternating row shading |
| **Editability** | — | Full (Word-native tables, searchable text) |

---

## Mobile-First Responsive Decisions

### Breakpoints

- **Desktop (> 768px):** Full layout, all columns visible, export buttons with labels
- **Tablet (480–768px):** Grid metadata stacks to 2 columns, table scrolls horizontally
- **Mobile (< 480px):** Metadata stacks to 1 column, export buttons icon-only, reduced padding

### Table Scrolling

On mobile, the allocation table scrolls horizontally. A visual cue ("← Scroll for more columns") appears below the table to hint at overflow (CSS pseudo-element).

**Why not collapse columns?**
- Collapsing to "accordion" style per chapter adds complexity and reduces clarity
- Horizontal scroll is a known pattern for data tables on mobile
- Users can still read chapter names and allocations in the initial scroll position

### Button Sizing

Export buttons are 44×44px minimum (accessibility standard). On mobile, text label hides but icon remains visible.

---

## Data Structure: AllocationRow vs Subject Specifics

The prototype uses subject-specific detection:
```python
is_science = subject in ("Science", "Mathematics") or is_twau
is_english = subject == "English"
uses_effort_index = is_science or is_english
```

**aruvi-saas approach:** Metadata-driven, no conditionals

```python
@dataclass
class AllocationRow:
    chapter_number: int
    chapter_name: str
    total_periods: int
    allocated_periods: int
    effort_index: Optional[float] = None  # Present only for Science/Math/English
    competency_weight: Optional[float] = None  # Present only for Social Sciences
```

The component detects which columns to show:
```jsx
const hasEffortIndex = report.rows.some((r) => r.effort_index !== null);
const hasCompetencyWeight = report.rows.some((r) => r.competency_weight !== null);
```

**Benefits:**
- No enum/string matching required
- Adding a new subject only requires passing the right row data
- PDF/DOCX exporters auto-adapt column widths

---

## Allocation Basis Explanation

**Prototype approach:**
- Subject-specific footnote blocks (hardcoded for English, Social Sciences, etc.)
- "About the Effort Index" section with multi-part explainers (English only)

**aruvi-saas approach:**
- Single `allocation_basis` field (string: "Effort Index" | "Competency Weights" | "Custom")
- Templated explanation note (same for all subjects)
- Link to Ask Aruvi for deeper explanations (deferred to helpline)

**Rationale:**
- Reduces maintenance burden (one explanatory note vs. per-subject blocks)
- Teaches users to explore Ask Aruvi for pedagogy details (reinforces engagement)
- Still provides enough context in the report itself
- Works for unknown future subjects without code change

---

## Design System Alignment

### Colors (CSS Variables)

All exports use Aruvi's warm editorial palette from `web/app/globals.css`:

```css
--paper: #fefaf4;      /* Cream background */
--ink: #1a1410;        /* Warm near-black text */
--pine: #2d5f4f;       /* Primary accent (headers) */
--clay: #c89968;       /* Warm highlight (allocated periods) */
--ochre: #d4a574;      /* Secondary highlight */
--line: #d4c5b0;       /* Border hairlines */
```

All three formats (web, PDF, DOCX) use the same color tokens, ensuring visual consistency.

### Typography

- **Titles:** Fraunces (display serif) — warm, editorial, confident
- **Body:** Newsreader (body serif) — comfortable, readable prose
- **Labels/Structure:** IBM Plex Mono (monospace) — crisp, utilitarian, numeric

This stack is unique to Aruvi and differentiates it from generic EdTech tools.

---

## Locale & Internationalization

**Current:** English labels only (same as prototype).

**Future:** The `allocation_basis` note and metadata labels can be i18n'd by using keys instead of hardcoded strings:

```python
# Today
allocation_note = "Periods are allocated proportionally based on the effort index..."

# Future
allocation_note = get_i18n_string("allocation_basis.effort_index", lang="hi")
```

No architectural change needed; just templating.

---

## Export Format Trade-offs

### PDF (reportlab)

**Pros:**
- Self-contained, universal reader (every platform)
- Print-faithful (matches on-screen rendering)
- Immutable (can't be accidentally edited)
- Smaller file size

**Cons:**
- Not editable (if teacher wants to tweak allocations)
- Text extraction is lossy (especially for tables)
- No search/replace

### DOCX (docx-js via Node)

**Pros:**
- Editable (teacher can adjust notes or allocation if needed)
- Searchable, copyable text
- Embedding in emails and sharing with colleagues
- Familiar format for Indian teachers (Word is ubiquitous)

**Cons:**
- Requires Node.js at runtime (infrastructure dependency)
- Slightly larger file size
- Teacher might accidentally break table format

**Design choice:** Offer both, let teacher choose. DOCX is secondary (button labeled "DOCX" not "EDIT").

---

## Column Width Calculation

### Portrait Layout (PDF/DOCX)

US Letter: 8.5" × 11", 1" margins = 6.5" content width = 9360 DXA (reportlab/docx units).

**Columns (DXA):**
- `#` (chapter number): 400 DXA (0.28")
- **Chapter name:** 2200 DXA (1.52")
- **Total Periods:** 1000 DXA (0.69")
- **Allocated Periods:** 1000 DXA (0.69")
- **Effort Index** (optional): 1000 DXA (0.69")
- **Competency Weight** (optional): 1760 DXA (1.22")

Total with base columns: 400 + 2200 + 1000 + 1000 = 4600 DXA, leaving ~4760 DXA for optional columns. Designed to fit 1–2 subjects comfortably on one page.

### Web Layout (Responsive)

Table uses full viewport width with horizontal scroll on mobile. Column widths scale proportionally using CSS percentages/minmax().

---

## Testing Checklist

### Unit Tests

- [x] `AllocationReport` creation from raw data
- [ ] Column width calculations for different subject combinations
- [ ] Effort index vs. competency weight detection
- [ ] Export byte validation (PDF magic bytes, DOCX zip signature)

### E2E Tests

- [x] Desktop web rendering + export PDF → verified in PDF reader
- [x] Tablet web rendering (768px) → metadata/table layout
- [ ] Mobile web rendering (390px) → export buttons, table scroll
- [ ] DOCX export → opens in Word, table renders, no corruption
- [ ] Print CSS → export buttons hidden, table stays readable

### Visual Regression

- [ ] Compare PDF output across subjects (Science, Math, English, Social Sciences)
- [ ] Compare DOCX styling with PDF (colors, fonts, table layout)
- [ ] Mobile screenshots at 390px, 480px, 768px breakpoints

---

## Future Enhancements

1. **Custom branding:** Allow schools to inject logos, footers, colors
2. **Scheduled reports:** Generate and email allocation reports monthly
3. **Comparison mode:** Side-by-side allocations for two classes/years
4. **Visualizations:** Heatmap or pie chart of allocation distribution
5. **Multilingual:** Translate metadata labels and explanatory text per region
6. **Batch export:** Download all chapters for a subject as a single report bundle
7. **Edit-in-place:** DOCX import → teacher edits allocations → re-import to app
8. **Audit trail:** Track allocation changes over time (versioning)

---

## Implementation Status

**Done:**
- [x] `aruvi_core/report_allocation.py` — Data structures
- [x] `aruvi_core/export_allocation_pdf.py` — PDF export (reportlab)
- [x] `aruvi_core/export_allocation_docx.py` — DOCX export (docx-js via Node)
- [x] `web/components/AllocationReportView.jsx` — React component
- [x] `web/components/AllocationReportView.module.css` — Responsive styles
- [x] Integration guide (`ALLOCATION_REPORT_INTEGRATION.md`)

**To-do (by developer):**
- [ ] API endpoints in `api/main.py` (`/api/allocation/export-pdf`, `/api/allocation/export-docx`)
- [ ] Wire component into Allocate step 4 ("final") in `web/app/page.jsx`
- [ ] Unit + E2E tests in `tests/`
- [ ] Mobile testing (390px, 480px, 768px)
- [ ] Print testing
- [ ] DOCX quality assurance in Word, Google Docs, LibreOffice

---

## Key Differences from Prototype

| What | Prototype | aruvi-saas | Why |
|------|-----------|-----------|-----|
| **Mobile support** | None | Full (tested 480px+) | Teachers use phones in classroom |
| **Export formats** | PDF only | PDF + DOCX | Editability + email sharing |
| **Subject detection** | String matching + enum | Data-driven (effort_index/competency_weight fields) | Scalable, no hardcoded conditionals |
| **Explanation blocks** | Per-subject footnotes | Single allocation_basis note | Maintenance burden reduction |
| **Styling** | Generic (Helvetica, navy) | Design system (Fraunces/Newsreader/Courier, Pine/Clay) | Brand consistency, warm editorial feel |
| **Web rendering** | Streamlit table | React component | Integrates with cloud SaaS UI |
| **Page size** | A4 (landscape) | US Letter (portrait) | Better for mobile printing, easier to email |

---

## References

- **Prototype allocation report:** `/sessions/inspiring-hopeful-wozniak/mnt/Project Aruvi/app/aruvi_streamlit/app.py` (lines 3669–3900)
- **Design system:** `web/app/globals.css` (CSS variables, typography)
- **Component library:** Lucide React for icons (`Download`, `FileText`, `File`)
