# Allocation Report Integration Guide

## Overview

The allocation report sits on the **final allocation step** (step 4 in the Allocate flow). It provides a standardized, mobile-responsive report of how periods are allocated across chapters, with export to PDF and DOCX formats.

The implementation is subject-agnostic — the same components and exports work for all subjects (Science, Social Sciences, Mathematics, English, The World Around Us).

---

## Components

### 1. **Report Data Structure** (`aruvi_core/report_allocation.py`)

- `AllocationReport` dataclass: Holds report metadata and rows
- `AllocationRow` dataclass: Single chapter row (number, name, total periods, allocated periods, optional effort index / competency weight)
- `create_report()` factory: Builds a report from raw allocation data
- `format_report_title()` / `format_report_subtitle()`: Formatting helpers

**Usage in API:**

```python
from aruvi_core.report_allocation import create_report

# After the allocate engine runs (in api/data.py or allocate endpoint)
rows = [
    {"chapter_number": 1, "chapter_name": "Learning Together", "total_periods": 40, "allocated_periods": 10, "effort_index": 15.0},
    {"chapter_number": 2, "chapter_name": "Wit and Humour", "total_periods": 40, "allocated_periods": 5, "effort_index": 13.5},
    # ...
]

report = create_report(
    subject="english",
    grade=7,
    stage="middle",
    period_profile_name="Core",  # User-defined name
    period_duration_minutes=40,
    allocation_rows=rows,
    allocation_basis="Effort Index",
    notes=None,
)

# Serialize for frontend
report_dict = report.to_dict()
```

### 2. **React Component** (`web/components/AllocationReportView.jsx`)

Renders the report with:
- Header (title, subtitle, date)
- Export buttons (PDF, DOCX)
- Metadata grid (period duration, total periods, allocation basis)
- Allocation table (smart columns based on subject metadata)
- Allocation basis note (contextual explanation)
- Optional report notes
- Footer

**Mobile-responsive:** Tested at 480px, 768px, and desktop widths. Button text hides on mobile; tables scroll horizontally with visual cue.

**Usage in page.jsx:**

```jsx
import AllocationReportView from "@/components/AllocationReportView";

export default function AllocatePage() {
  const [report, setReport] = useState(null);

  const handleExportPDF = async () => {
    const response = await fetch("/api/allocation/export-pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(report),
    });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `allocation-report-grade-${report.grade}-${report.subject}.pdf`;
    a.click();
  };

  const handleExportDOCX = async () => {
    const response = await fetch("/api/allocation/export-docx", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(report),
    });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `allocation-report-grade-${report.grade}-${report.subject}.docx`;
    a.click();
  };

  return (
    <AllocationReportView
      report={report}
      onExportPDF={handleExportPDF}
      onExportDOCX={handleExportDOCX}
    />
  );
}
```

### 3. **PDF Export** (`aruvi_core/export_allocation_pdf.py`)

Uses reportlab to generate warm-editorial PDFs matching the web design:
- Fraunces title, Newsreader body, Courier mono labels
- Pine (primary), Clay (accent), Line (borders) colors
- Metadata table with 3-row key-value layout
- Sortable allocation table with alternating row backgrounds
- Allocation basis note in a clay-tinted left-border box
- Footer with report metadata

**Usage in API:**

```python
from aruvi_core.export_allocation_pdf import export_allocation_report_pdf

@app.post("/api/allocation/export-pdf")
async def export_pdf(report_dict: dict):
    report = AllocationReport(**report_dict)  # Reconstruct from dict
    pdf_bytes = export_allocation_report_pdf(report)
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=allocation-report.pdf"},
    )
```

### 4. **DOCX Export** (`aruvi_core/export_allocation_docx.py`)

Uses `docx` (Node.js library) via subprocess to generate Word documents:
- Same design language as PDF
- US Letter page size, 1-inch margins
- Metadata table with conditional row shading
- Allocation table with dynamic columns (effort index / competency weight only if present)
- Allocation basis note with left-border styling
- Optional report-level notes section
- Footer (Courier, small, centered)

**Requires Node.js and `npm install -g docx`**

**Usage in API:**

```python
from aruvi_core.export_allocation_docx import export_allocation_report_docx

@app.post("/api/allocation/export-docx")
async def export_docx(report_dict: dict):
    report = AllocationReport(**report_dict)  # Reconstruct from dict
    docx_bytes = export_allocation_report_docx(report)
    return StreamingResponse(
        iter([docx_bytes]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=allocation-report.docx"},
    )
```

---

## Data Flow

### Allocation → Report → Export

```
1. User completes allocate step (selects chapters, defines periods, gets suggested allocation)
2. API runs allocate engine → produces AllocationData
3. API transforms AllocationData → create_report() → AllocationReport
4. API sends report dict to frontend
5. Frontend renders AllocationReportView
6. User clicks PDF/DOCX → frontend POST to /api/allocation/export-{pdf|docx}
7. API calls export function → returns bytes
8. Frontend downloads file
```

### Allocate Step (step 4: "final")

The "final" step in the Allocate flow should:
1. Display the read-only final allocation table (as before)
2. Below that, display the AllocationReportView component
3. Provide "Save Allocation" and "Download" buttons (or integrate downloads into report export buttons)

---

## API Endpoints

Add these to `api/main.py`:

```python
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from aruvi_core.report_allocation import AllocationReport

router = APIRouter(prefix="/api/allocation", tags=["allocation"])

@router.post("/export-pdf")
async def export_pdf(report_dict: dict):
    """Export allocation report as PDF."""
    report = AllocationReport(**report_dict)
    pdf_bytes = export_allocation_report_pdf(report)
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=allocation-report-grade-{report.grade}.pdf"},
    )

@router.post("/export-docx")
async def export_docx(report_dict: dict):
    """Export allocation report as DOCX."""
    report = AllocationReport(**report_dict)
    docx_bytes = export_allocation_report_docx(report)
    return StreamingResponse(
        iter([docx_bytes]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=allocation-report-grade-{report.grade}.docx"},
    )

app.include_router(router)
```

---

## Mobile Verification Checklist

Before shipping, verify on mobile (390px × 844px):

- [ ] Header title and buttons render without horizontal overflow
- [ ] Export buttons visible (text hidden, icons visible)
- [ ] Metadata grid stacks to 1-2 columns (not 3)
- [ ] Allocation table scrolls horizontally with visual cue
- [ ] Tap targets on buttons ≥44px (all buttons are)
- [ ] Text is readable at default zoom (base font 14-16px)
- [ ] No fixed-width divs cause layout issues
- [ ] Footer readable at mobile size
- [ ] Print styles hide export buttons

**Test with:** DevTools mobile viewport or actual phone

---

## Customization by Subject

The report is subject-agnostic, but optional metadata columns adapt:

- **Science/Social Sciences:** Show `effort_index`
- **Mathematics/English:** Show `competency_weight` (or both if present)
- **The World Around Us:** Show neither (falls back to base columns)

The component detects which columns to show based on `report.rows` data presence, so no code change needed — data is king.

---

## Design System Reference

All colors and fonts use CSS variables from `web/app/globals.css`:

- `--f-display`: Fraunces (titles)
- `--f-body`: Newsreader (prose)
- `--f-mono`: IBM Plex Mono (labels, tables)
- `--paper`: #fefaf4 (background)
- `--ink`: #1a1410 (text)
- `--pine`: #2d5f4f (primary accent)
- `--clay`: #c89968 (warm highlight)
- `--ochre`: #d4a574 (secondary highlight)
- `--line`: #d4c5b0 (borders)

Keep these consistent across all exports (PDF, DOCX, web).

---

## Testing

### Unit Tests

```python
# tests/test_report_allocation.py
from aruvi_core.report_allocation import create_report

def test_create_report():
    rows = [
        {"chapter_number": 1, "chapter_name": "Ch1", "total_periods": 40, "allocated_periods": 10},
        {"chapter_number": 2, "chapter_name": "Ch2", "total_periods": 40, "allocated_periods": 8},
    ]
    report = create_report(
        subject="english",
        grade=7,
        stage="middle",
        period_profile_name="Core",
        period_duration_minutes=40,
        allocation_rows=rows,
        allocation_basis="Effort Index",
    )
    assert report.total_periods == 18
    assert report.rows[0].chapter_name == "Ch1"
```

### Export Tests

```python
# tests/test_export_allocation.py
from aruvi_core.export_allocation_pdf import export_allocation_report_pdf
from aruvi_core.export_allocation_docx import export_allocation_report_docx

def test_export_pdf():
    report = ...  # create_report()
    pdf_bytes = export_allocation_report_pdf(report)
    assert pdf_bytes.startswith(b"%PDF")  # PDF magic bytes

def test_export_docx():
    report = ...  # create_report()
    docx_bytes = export_allocation_report_docx(report)
    assert docx_bytes[:4] == b"PK\x03\x04"  # ZIP magic bytes
```

### E2E Test

1. Allocate a subject/grade
2. Render allocation report
3. Export PDF → verify opens in PDF reader, table renders correctly
4. Export DOCX → verify opens in Word, table renders correctly, no corruption

---

## Known Limitations

1. **Node.js required for DOCX:** Subprocess call to `node`. If Node not available, gracefully return error with fallback to PDF.
2. **DOCX tables don't reflow:** Very long chapter names may overflow cells. Consider truncation or multi-line rendering.
3. **Print CSS:** Print preview in browser should hide export buttons (CSS handles this). Test in actual print dialog.
4. **Mobile tables:** Very narrow screens (< 360px) may still scroll. Acceptable trade-off for legibility.

---

## Future Enhancements

1. **Template customization:** Allow schools to brand reports with logo, header/footer overrides
2. **Scheduled reports:** Generate and email allocation reports on a schedule
3. **Comparison reports:** Side-by-side allocation for two classes/years
4. **Heatmap visualization:** Visual allocation by chapter color intensity
5. **Multilingual:** Translate metadata labels and note text per region

---

## Files Checklist

- [x] `aruvi_core/report_allocation.py` — Data structures + factories
- [x] `aruvi_core/export_allocation_pdf.py` — PDF generation
- [x] `aruvi_core/export_allocation_docx.py` — DOCX generation
- [x] `web/components/AllocationReportView.jsx` — React component
- [x] `web/components/AllocationReportView.module.css` — Responsive styles
- [ ] `api/main.py` — Add export endpoints (to be wired by developer)
- [ ] `web/app/page.jsx` — Integrate report into Allocate step (to be wired by developer)
- [ ] `tests/test_report_allocation.py` — Unit tests (to be created)
- [ ] `tests/test_export_allocation.py` — Export tests (to be created)

---

## Quick Start (for developer wiring)

1. Import the report class and export functions:
   ```python
   from aruvi_core.report_allocation import create_report
   from aruvi_core.export_allocation_pdf import export_allocation_report_pdf
   from aruvi_core.export_allocation_docx import export_allocation_report_docx
   ```

2. After allocate engine runs, call `create_report()` with allocation data

3. Send report dict to frontend via `/api/allocate/final` endpoint

4. Render `<AllocationReportView>` in step 4 of Allocate flow

5. Wire up export callbacks in `page.jsx` → call `/api/allocation/export-{pdf|docx}` endpoints

6. Test on desktop and mobile (390px viewport)

7. Verify PDF/DOCX open correctly in readers

**Done!**
