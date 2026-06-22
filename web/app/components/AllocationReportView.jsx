"use client";

import React, { useState } from "react";

/**
 * AllocationReportView
 * Renders the standardized allocation report for any subject.
 * Mobile-responsive with export to PDF/DOCX.
 *
 * Styles live in app/globals.css under the `.arpt-*` namespace (project
 * convention — no CSS modules, no icon libraries).
 *
 * Props:
 *  - report: AllocationReport object
 *  - onExportPDF: callback to trigger PDF export
 *  - onExportDOCX: callback to trigger DOCX export
 *  - isPrinting: boolean to hide export buttons during print
 */
export default function AllocationReportView({
  report,
  onExportPDF,
  onExportDOCX,
  isPrinting = false,
}) {
  const [exportLoading, setExportLoading] = useState({ pdf: false, docx: false });

  if (!report) return null;

  const handleExportPDF = async () => {
    setExportLoading((p) => ({ ...p, pdf: true }));
    try {
      await onExportPDF?.();
    } finally {
      setExportLoading((p) => ({ ...p, pdf: false }));
    }
  };

  const handleExportDOCX = async () => {
    setExportLoading((p) => ({ ...p, docx: true }));
    try {
      await onExportDOCX?.();
    } finally {
      setExportLoading((p) => ({ ...p, docx: false }));
    }
  };

  const subjectDisplay = report.subject.replace(/_/g, " ");
  const totalAllocated = report.rows.reduce(
    (sum, row) => sum + (row.allocated_periods || 0),
    0
  );

  const hasEffortIndex = report.rows.some(
    (r) => r.effort_index !== null && r.effort_index !== undefined
  );
  const hasCompetencyWeight = report.rows.some(
    (r) => r.competency_weight !== null && r.competency_weight !== undefined
  );

  const basisNote =
    report.allocation_basis === "Effort Index"
      ? "Periods are allocated proportionally to each chapter's effort index — chapters with a higher effort index receive more time to ensure mastery."
      : report.allocation_basis === "Competency Weights"
      ? "Periods are allocated according to the relative weight of the competencies covered in each chapter."
      : "Periods are allocated using the allocation strategy defined for this curriculum.";

  return (
    <div className="arpt">
      <div className="arpt-head">
        <div className="arpt-head-text">
          <p className="arpt-kicker">Period Allocation Report</p>
          <h2 className="arpt-title">
            {subjectDisplay} · Grade {report.grade}
          </h2>
          <p className="arpt-date">
            {new Date(report.generated_at).toLocaleDateString(undefined, {
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </p>
        </div>

        {!isPrinting && (
          <div className="arpt-actions">
            <button
              className="arpt-btn"
              onClick={handleExportPDF}
              disabled={exportLoading.pdf}
              title="Export as PDF"
              aria-label="Export report as PDF"
            >
              <DownloadIcon />
              <span>{exportLoading.pdf ? "Exporting…" : "PDF"}</span>
            </button>
            <button
              className="arpt-btn"
              onClick={handleExportDOCX}
              disabled={exportLoading.docx}
              title="Export as Word document"
              aria-label="Export report as Word document"
            >
              <DownloadIcon />
              <span>{exportLoading.docx ? "Exporting…" : "DOCX"}</span>
            </button>
          </div>
        )}
      </div>

      <div className="arpt-meta">
        <div className="arpt-meta-item">
          <span className="arpt-meta-label">Period duration</span>
          <span className="arpt-meta-value">{report.period_duration_minutes} min</span>
        </div>
        <div className="arpt-meta-item">
          <span className="arpt-meta-label">Total periods</span>
          <span className="arpt-meta-value">{totalAllocated}</span>
        </div>
        <div className="arpt-meta-item">
          <span className="arpt-meta-label">Allocation basis</span>
          <span className="arpt-meta-value">{report.allocation_basis}</span>
        </div>
      </div>

      <div className="arpt-table-scroll">
        <table className="arpt-table">
          <thead>
            <tr>
              <th className="num">#</th>
              <th>Chapter</th>
              <th className="num">{report.period_profile_name || "Allocated"} periods</th>
              {hasEffortIndex && <th className="num">Effort index</th>}
              {hasCompetencyWeight && <th className="num">Competency weight</th>}
            </tr>
          </thead>
          <tbody>
            {report.rows.map((row, idx) => (
              <tr key={idx}>
                <td className="num arpt-chn">{row.chapter_number}</td>
                <td>{row.chapter_name}</td>
                <td className="num">{row.allocated_periods}</td>
                {hasEffortIndex && (
                  <td className="num">
                    {row.effort_index !== null && row.effort_index !== undefined
                      ? Number(row.effort_index).toFixed(1)
                      : "—"}
                  </td>
                )}
                {hasCompetencyWeight && (
                  <td className="num">
                    {row.competency_weight !== null &&
                    row.competency_weight !== undefined
                      ? Math.round(row.competency_weight * 100) + "%"
                      : "—"}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <td className="arpt-total-lbl" colSpan={2}>
                Total
              </td>
              <td className="num arpt-total">{totalAllocated}</td>
              {hasEffortIndex && <td />}
              {hasCompetencyWeight && <td />}
            </tr>
          </tfoot>
        </table>
      </div>

      <div className="arpt-note">
        <p className="arpt-note-title">How are periods allocated?</p>
        <p className="arpt-note-text">
          {basisNote} For the full reasoning, see the “How time is allocated across
          chapters” tab in the Ask Aruvi helpline.
        </p>
      </div>

      {report.notes && (
        <div className="arpt-note">
          <p className="arpt-note-title">Notes</p>
          <p className="arpt-note-text">{report.notes}</p>
        </div>
      )}
    </div>
  );
}

function DownloadIcon() {
  return (
    <svg
      width="15"
      height="15"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" y1="15" x2="12" y2="3" />
    </svg>
  );
}
