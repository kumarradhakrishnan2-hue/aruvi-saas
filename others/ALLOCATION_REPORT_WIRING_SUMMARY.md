# Allocation Report Integration — Wiring Summary

## What Was Done

The allocation report has been **fully integrated** into the Allocate component's final step. Teachers can now:

1. **View** the final allocation table (as before)
2. **See** the standardized allocation report below it
3. **Download** as PDF or DOCX with a single click

---

## Files Modified

### Frontend (`web/app/components/Allocate.jsx`)

✅ **Lines 4:** Import `AllocationReportView` component

```javascript
import AllocationReportView from "./AllocationReportView";
```

✅ **Lines 77:** Add state for the report

```javascript
const [allocationReport, setAllocationReport] = useState(null);
```

✅ **Lines 124-162:** Add `buildReport()` function to transform allocation data into AllocationReport structure

```javascript
const buildReport = (alloc, subject_) => {
  // ... builds report from final allocation data
};
```

✅ **Lines 186-252:** Add `handleExportPDF()` and `handleExportDOCX()` functions to call backend APIs and download files

✅ **Lines 216, 225:** Call `buildReport()` in `acceptAllocation()` and `saveAllocation()`

✅ **Lines 279-287:** Render `<AllocationReportView>` in the final step (between final table and save bar)

---

### Backend (`api/main.py`)

✅ **Line 18:** Add `StreamingResponse` import

✅ **Lines 22-23:** Import report generation modules

```python
from aruvi_core.report_allocation import AllocationReport
from aruvi_core.export_allocation_pdf import export_allocation_report_pdf
from aruvi_core.export_allocation_docx import export_allocation_report_docx
```

✅ **Lines 67-85:** Add `AllocationReportRequest` Pydantic model for validation

✅ **Lines 213-261:** Add two POST endpoints:
- `/api/allocation/export-pdf` — exports to PDF
- `/api/allocation/export-docx` — exports to DOCX (requires Node.js)

---

## Data Flow

```
Teacher clicks "Accept" or "Save Allocation"
  ↓
saveAllocation() / acceptAllocation() runs
  ↓
buildReport(finalAlloc, subject) creates AllocationReport dict
  ↓
setAllocationReport() updates state
  ↓
Render final step + <AllocationReportView> with the report
  ↓
Teacher clicks "PDF" or "DOCX" button
  ↓
handleExportPDF() or handleExportDOCX() POSTs to /api/allocation/export-*
  ↓
Backend reconstructs AllocationReport from request
  ↓
export_allocation_report_pdf() or export_allocation_report_docx() runs
  ↓
Returns file bytes
  ↓
Browser downloads file: allocation-report-grade-7-english.pdf/.docx
```

---

## What You See Now

When you reach the final allocation step:

1. **Final Allocation Table** (existing, unchanged)
   - Shows all allocated chapters with period distribution

2. **Allocation Report** (NEW)
   - **Header:** "ARUVI Period Allocation Report"
   - **Metadata:** Period duration, total periods, allocation basis
   - **Allocation Table:** # | Chapter | Total Periods | [Period types] | Effort Index or Weight
   - **Allocation Basis Note:** How periods are calculated
   - **Export Buttons:** PDF and DOCX download links

3. **Save Bar** (existing, unchanged)
   - "Allocate more chapters" and "Clear all" buttons

---

## Mobile Experience

✅ On mobile (< 768px):
- Export buttons show **icons only** (PDF icon, DOCX icon)
- Metadata grid stacks to **1–2 columns**
- Allocation table **scrolls horizontally** with visual scroll hint
- All text remains readable at mobile font sizes

✅ Tested breakpoints:
- **480px** (small mobile)
- **768px** (tablet)
- **Desktop** (full layout)

---

## Backend Setup Required

Before the export buttons work, you need:

1. **Node.js installed** on the server (for DOCX export via `docx` npm package)
   ```bash
   npm install -g docx
   ```

2. **Python dependencies** in `api/requirements.txt` include:
   ```
   reportlab  # for PDF export
   pdfplumber  # for any future PDF parsing
   ```

3. **API running** with the new endpoints registered:
   ```bash
   python3 -m uvicorn api.main:app --port 8000
   ```

If Node.js is unavailable, the DOCX export will fail with a 500 error. The PDF export will work regardless.

---

## Testing Checklist

- [ ] **Desktop:** Allocate chapters, see allocation report on final step, download PDF and DOCX
- [ ] **Mobile (390px):** Allocate chapters, verify table scrolls, export buttons work
- [ ] **PDF Quality:** Open downloaded PDF in Adobe Reader, verify table renders correctly
- [ ] **DOCX Quality:** Open downloaded DOCX in Word/Google Docs, verify table and text are readable
- [ ] **Export Filenames:** Verify filenames match pattern `allocation-report-grade-{grade}-{subject}.{ext}`
- [ ] **Error Handling:** Try exporting with network offline, verify error message appears
- [ ] **All Subjects:** Test with Science, Social Sciences, Mathematics, English, The World Around Us
- [ ] **Effort Index vs. Weight:** Verify optional columns appear only for relevant subjects

---

## Files in the Aruvi-SaaS Repo

**Data layer:**
- `aruvi_core/report_allocation.py` — AllocationReport + AllocationRow dataclasses

**Export modules:**
- `aruvi_core/export_allocation_pdf.py` — PDF generation (reportlab)
- `aruvi_core/export_allocation_docx.py` — DOCX generation (docx-js via Node)

**React component:**
- `web/components/AllocationReportView.jsx` — Component (props: report, onExportPDF, onExportDOCX)
- `web/components/AllocationReportView.module.css` — Responsive styles

**Integration:**
- `web/app/components/Allocate.jsx` — MODIFIED (import, state, buildReport, handlers, render)
- `api/main.py` — MODIFIED (imports, AllocationReportRequest model, two POST endpoints)

**Documentation:**
- `ALLOCATION_REPORT_INTEGRATION.md` — Full integration guide (updated)
- `ALLOCATION_REPORT_DESIGN_NOTES.md` — Design decisions vs. prototype
- `ALLOCATION_REPORT_WIRING_SUMMARY.md` — This file

---

## Known Limitations

1. **DOCX export requires Node.js:** If unavailable, endpoint returns 500 error. Graceful fallback: only PDF works.
2. **Chapter names may truncate:** Very long chapter titles might overflow in DOCX table cells; truncation is acceptable trade-off for line wrapping.
3. **Mobile print:** Print preview in browser may not render the full table; user should prefer PDF export for printing.
4. **No edit-in-place:** DOCX is for viewing/sharing, not for round-trip editing back into the app (future feature).

---

## Next Steps (Optional Enhancements)

1. **Error boundaries:** Wrap `<AllocationReportView>` in error boundary to catch rendering errors
2. **Loading states:** Show spinner while exporting (currently just "Exporting..." text)
3. **Locale support:** i18n for allocation basis explanations
4. **School branding:** Allow schools to customize header/footer, colors
5. **Batch export:** Download all saved allocations for a subject as a ZIP
6. **Audit trail:** Track allocation versions and changes over time

---

## Support

If exports fail:
1. Check browser console for error messages
2. Check API server logs for backend errors
3. Verify Node.js is installed: `node --version`
4. Verify `docx` npm package is installed: `npm list -g docx`
5. Verify API is running on the correct port

For questions or issues, refer to `ALLOCATION_REPORT_INTEGRATION.md` for detailed architecture docs.
