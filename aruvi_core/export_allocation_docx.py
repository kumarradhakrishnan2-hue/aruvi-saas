"""
DOCX export for allocation reports using docx-js via Node.
Generates Word documents with warm editorial design language.
"""

import json
import subprocess
import tempfile
from pathlib import Path

from .report_allocation import AllocationReport


DOCX_GENERATOR_TEMPLATE = """
const {{ Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
         AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign }} = require('docx');
const fs = require('fs');

// Color palette (matching web design)
const colors = {{
  pine: "2d5f4f",
  clay: "c89968",
  line: "d4c5b0",
  lightGray: "f5f3f0",
  veryLightGray: "fafaf8",
}};

const border = {{ style: BorderStyle.SINGLE, size: 1, color: colors.line }};
const borders = {{ top: border, bottom: border, left: border, right: border }};

// Report data injected as JSON
const report = {report_json};

// Build document
const doc = new Document({{
  sections: [{{
    properties: {{
      page: {{
        size: {{
          width: 12240,   // 8.5 inches (US Letter)
          height: 15840,  // 11 inches
        }},
        margin: {{ top: 1440, right: 1440, bottom: 1440, left: 1440 }}, // 1 inch margins
      }},
    }},
    children: [
      // ========== HEADER ==========
      new Paragraph({{
        children: [
          new TextRun({{
            text: "ARUVI Period Allocation Report",
            bold: true,
            size: 36,
            font: "Arial",
            color: "1a1410",
          }}),
        ],
        spacing: {{ after: 120 }},
      }}),

      new Paragraph({{
        children: [
          new TextRun({{
            text: `NCF 2023 · PEDAGOGICAL PLATFORM · GRADE ${{report.grade}} · ${{report.subject.toUpperCase().replace(/_/g, ' ')}} · ${{report.generated_at.split('T')[0]}}`,
            size: 16,
            font: "Courier New",
            bold: true,
            color: colors.pine,
            allCaps: true,
          }}),
        ],
        spacing: {{ after: 240 }},
      }}),

      // ========== METADATA TABLE ==========
      new Table({{
        width: {{ size: 9360, type: WidthType.DXA }},
        columnWidths: [3120, 6240],
        rows: [
          new TableRow({{
            children: [
              new TableCell({{
                borders,
                width: {{ size: 3120, type: WidthType.DXA }},
                shading: {{ fill: colors.lightGray, type: ShadingType.CLEAR }},
                margins: {{ top: 80, bottom: 80, left: 120, right: 120 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "PERIOD DURATION",
                    size: 14,
                    font: "Courier New",
                    bold: true,
                    color: colors.pine,
                  }})],
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 6240, type: WidthType.DXA }},
                margins: {{ top: 80, bottom: 80, left: 120, right: 120 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: `${{report.period_duration_minutes}} min`,
                    size: 22,
                    bold: true,
                    font: "Arial",
                    color: "1a1410",
                  }})],
                }})],
              }}),
            ],
          }}),
          new TableRow({{
            children: [
              new TableCell({{
                borders,
                width: {{ size: 3120, type: WidthType.DXA }},
                shading: {{ fill: "ffffff", type: ShadingType.CLEAR }},
                margins: {{ top: 80, bottom: 80, left: 120, right: 120 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "TOTAL PERIODS",
                    size: 14,
                    font: "Courier New",
                    bold: true,
                    color: colors.pine,
                  }})],
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 6240, type: WidthType.DXA }},
                shading: {{ fill: colors.veryLightGray, type: ShadingType.CLEAR }},
                margins: {{ top: 80, bottom: 80, left: 120, right: 120 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: `${{report.total_periods}}`,
                    size: 22,
                    bold: true,
                    font: "Arial",
                    color: "1a1410",
                  }})],
                }})],
              }}),
            ],
          }}),
          new TableRow({{
            children: [
              new TableCell({{
                borders,
                width: {{ size: 3120, type: WidthType.DXA }},
                shading: {{ fill: colors.lightGray, type: ShadingType.CLEAR }},
                margins: {{ top: 80, bottom: 80, left: 120, right: 120 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "ALLOCATION BASIS",
                    size: 14,
                    font: "Courier New",
                    bold: true,
                    color: colors.pine,
                  }})],
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 6240, type: WidthType.DXA }},
                margins: {{ top: 80, bottom: 80, left: 120, right: 120 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: report.allocation_basis,
                    size: 22,
                    bold: true,
                    font: "Arial",
                    color: "1a1410",
                  }})],
                }})],
              }}),
            ],
          }}),
        ],
      }}),

      new Paragraph({ text: "", spacing: {{ after: 480 }} }},

      // ========== ALLOCATION TABLE ==========
      new Table({{
        width: {{ size: 9360, type: WidthType.DXA }},
        columnWidths: [{column_widths}],
        rows: [
          // Header row
          new TableRow({{
            children: [
              new TableCell({{
                borders,
                width: {{ size: 400, type: WidthType.DXA }},
                shading: {{ fill: colors.pine, type: ShadingType.CLEAR }},
                margins: {{ top: 100, bottom: 100, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "#",
                    bold: true,
                    size: 16,
                    font: "Courier New",
                    color: "ffffff",
                  }})],
                  alignment: AlignmentType.CENTER,
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 2200, type: WidthType.DXA }},
                shading: {{ fill: colors.pine, type: ShadingType.CLEAR }},
                margins: {{ top: 100, bottom: 100, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "Chapter",
                    bold: true,
                    size: 16,
                    font: "Courier New",
                    color: "ffffff",
                  }})],
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 1000, type: WidthType.DXA }},
                shading: {{ fill: colors.pine, type: ShadingType.CLEAR }},
                margins: {{ top: 100, bottom: 100, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "Total Periods",
                    bold: true,
                    size: 16,
                    font: "Courier New",
                    color: "ffffff",
                  }})],
                  alignment: AlignmentType.RIGHT,
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 1000, type: WidthType.DXA }},
                shading: {{ fill: colors.pine, type: ShadingType.CLEAR }},
                margins: {{ top: 100, bottom: 100, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "{period_profile_name} Periods",
                    bold: true,
                    size: 16,
                    font: "Courier New",
                    color: "ffffff",
                  }})],
                  alignment: AlignmentType.RIGHT,
                }})],
              }}),
              {extra_column_headers}
            ],
          }}),

          // Data rows
          {data_rows}

          // Total row
          new TableRow({{
            children: [
              new TableCell({{
                borders,
                width: {{ size: 400, type: WidthType.DXA }},
                shading: {{ fill: colors.lightGray, type: ShadingType.CLEAR }},
                margins: {{ top: 100, bottom: 100, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "",
                    size: 16,
                  }})],
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 2200, type: WidthType.DXA }},
                shading: {{ fill: colors.lightGray, type: ShadingType.CLEAR }},
                margins: {{ top: 100, bottom: 100, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "Total",
                    bold: true,
                    size: 16,
                    font: "Arial",
                  }})],
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 1000, type: WidthType.DXA }},
                shading: {{ fill: colors.lightGray, type: ShadingType.CLEAR }},
                margins: {{ top: 100, bottom: 100, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "",
                    size: 16,
                  }})],
                  alignment: AlignmentType.RIGHT,
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 1000, type: WidthType.DXA }},
                shading: {{ fill: colors.lightGray, type: ShadingType.CLEAR }},
                margins: {{ top: 100, bottom: 100, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "{total_periods}",
                    bold: true,
                    size: 16,
                    font: "Courier New",
                    color: colors.clay,
                  }})],
                  alignment: AlignmentType.RIGHT,
                }})],
              }}),
              {extra_column_footers}
            ],
          }}),
        ],
      }}),

      new Paragraph({ text: "", spacing: {{ after: 480 }} }},

      // ========== ALLOCATION BASIS NOTE ==========
      new Paragraph({{
        children: [
          new TextRun({{
            text: "How are periods allocated?",
            bold: true,
            size: 18,
            font: "Arial",
            color: colors.clay,
          }}),
        ],
        spacing: {{ after: 120 }},
      }}),

      new Paragraph({{
        children: [
          new TextRun({{
            text: "{allocation_note_text}",
            size: 18,
            font: "Arial",
          }}),
        ],
        spacing: {{ after: 240 }},
        indent: {{ left: 200 }},
      }}),

      {optional_notes_section}

      new Paragraph({{
        children: [
          new TextRun({{
            text: `Aruvi · Period Allocation Report · Grade ${{report.grade}} · {subject_display} · Page 1 of 1 · Confidential`,
            size: 14,
            font: "Courier New",
            color: "6b6b6b",
          }}),
        ],
        alignment: AlignmentType.CENTER,
        spacing: {{ before: 240 }},
      }}),
    ],
  }}],
}});

// Write to buffer (or stdout)
Packer.toBuffer(doc).then(buffer => {{
  process.stdout.write(buffer);
}}).catch(err => {{
  console.error("Error generating DOCX:", err);
  process.exit(1);
}});
"""


def export_allocation_report_docx(report: AllocationReport) -> bytes:
    """
    Generate allocation report DOCX using Node + docx package.

    Args:
        report: AllocationReport object

    Returns:
        DOCX bytes
    """
    # Prepare report data
    report_dict = report.to_dict()

    # Determine if using effort index or competency weight
    has_effort = any(r["effort_index"] is not None for r in report_dict["rows"])
    has_competency = any(
        r["competency_weight"] is not None for r in report_dict["rows"]
    )

    # Build column widths (DXA: 1440 = 1 inch)
    # Total width = 9360 DXA (6.5 inches content in 8.5" letter)
    column_widths = [400, 2200, 1000, 1000]  # #, Chapter, Total, Allocated
    if has_effort:
        column_widths.append(1000)
    if has_competency:
        column_widths.append(1760)

    column_widths_str = ", ".join(str(w) for w in column_widths)

    # Build extra column headers
    extra_headers = ""
    if has_effort:
        extra_headers += """
              new TableCell({
                borders,
                width: { size: 1000, type: WidthType.DXA },
                shading: { fill: colors.pine, type: ShadingType.CLEAR },
                margins: { top: 100, bottom: 100, left: 80, right: 80 },
                children: [new Paragraph({
                  children: [new TextRun({
                    text: "Effort Index",
                    bold: true,
                    size: 16,
                    font: "Courier New",
                    color: "ffffff",
                  })],
                  alignment: AlignmentType.RIGHT,
                })],
              }),
        """
    if has_competency:
        extra_headers += """
              new TableCell({
                borders,
                width: { size: 1760, type: WidthType.DXA },
                shading: { fill: colors.pine, type: ShadingType.CLEAR },
                margins: { top: 100, bottom: 100, left: 80, right: 80 },
                children: [new Paragraph({
                  children: [new TextRun({
                    text: "Competency Weight",
                    bold: true,
                    size: 16,
                    font: "Courier New",
                    color: "ffffff",
                  })],
                  alignment: AlignmentType.RIGHT,
                })],
              }),
        """

    # Build data rows
    data_rows = ""
    for i, row in enumerate(report_dict["rows"]):
        bg_color = "ffffff" if i % 2 == 0 else colors.get("veryLightGray", "fafaf8")

        extra_cells = ""
        if has_effort:
            effort_val = f"{row['effort_index']:.1f}" if row["effort_index"] else "—"
            extra_cells += f"""
              new TableCell({{
                borders,
                width: {{ size: 1000, type: WidthType.DXA }},
                shading: {{ fill: "{bg_color}", type: ShadingType.CLEAR }},
                margins: {{ top: 80, bottom: 80, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "{effort_val}",
                    size: 16,
                    font: "Courier New",
                  }})],
                  alignment: AlignmentType.RIGHT,
                }})],
              }}),
            """

        if has_competency:
            weight_val = (
                f"{int(row['competency_weight'] * 100)}%"
                if row["competency_weight"]
                else "—"
            )
            extra_cells += f"""
              new TableCell({{
                borders,
                width: {{ size: 1760, type: WidthType.DXA }},
                shading: {{ fill: "{bg_color}", type: ShadingType.CLEAR }},
                margins: {{ top: 80, bottom: 80, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "{weight_val}",
                    size: 16,
                    font: "Courier New",
                  }})],
                  alignment: AlignmentType.RIGHT,
                }})],
              }}),
            """

        data_rows += f"""
          new TableRow({{
            children: [
              new TableCell({{
                borders,
                width: {{ size: 400, type: WidthType.DXA }},
                shading: {{ fill: "{bg_color}", type: ShadingType.CLEAR }},
                margins: {{ top: 80, bottom: 80, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "{row['chapter_number']}",
                    size: 16,
                    font: "Courier New",
                  }})],
                  alignment: AlignmentType.CENTER,
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 2200, type: WidthType.DXA }},
                shading: {{ fill: "{bg_color}", type: ShadingType.CLEAR }},
                margins: {{ top: 80, bottom: 80, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "{row['chapter_name']}",
                    size: 16,
                    font: "Arial",
                  }})],
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 1000, type: WidthType.DXA }},
                shading: {{ fill: "{bg_color}", type: ShadingType.CLEAR }},
                margins: {{ top: 80, bottom: 80, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "{row['total_periods']}",
                    size: 16,
                    font: "Courier New",
                  }})],
                  alignment: AlignmentType.RIGHT,
                }})],
              }}),
              new TableCell({{
                borders,
                width: {{ size: 1000, type: WidthType.DXA }},
                shading: {{ fill: "{bg_color}", type: ShadingType.CLEAR }},
                margins: {{ top: 80, bottom: 80, left: 80, right: 80 }},
                children: [new Paragraph({{
                  children: [new TextRun({{
                    text: "{row['allocated_periods']}",
                    bold: true,
                    size: 16,
                    font: "Courier New",
                    color: "c89968",
                  }})],
                  alignment: AlignmentType.RIGHT,
                }})],
              }}),
              {extra_cells}
            ],
          }}),
        """

    # Build allocation note text
    if report.allocation_basis == "Effort Index":
        allocation_note = "Periods are allocated proportionally based on the effort index for each chapter. Chapters with higher effort indices receive more time to ensure mastery. Learn more in the Ask Aruvi helpline."
    elif report.allocation_basis == "Competency Weights":
        allocation_note = "Periods are allocated according to the relative weight of competencies covered in each chapter. Learn more in the Ask Aruvi helpline."
    else:
        allocation_note = "Periods are allocated according to a custom allocation strategy defined for this curriculum. Learn more in the Ask Aruvi helpline."

    # Build optional notes section
    optional_notes = ""
    if report.notes:
        optional_notes = f"""
      new Paragraph({{
        children: [
          new TextRun({{
            text: "Notes:",
            bold: true,
            size: 18,
            font: "Arial",
            color: colors.pine,
          }}),
        ],
        spacing: {{ after: 120 }},
      }}),

      new Paragraph({{
        children: [
          new TextRun({{
            text: "{report.notes}",
            size: 18,
            font: "Arial",
          }}),
        ],
        spacing: {{ after: 240 }},
        indent: {{ left: 200 }},
      }}),
    """

    # Build extra column footers
    extra_footers = ""
    if has_effort:
        extra_footers += """
              new TableCell({
                borders,
                width: { size: 1000, type: WidthType.DXA },
                shading: { fill: colors.lightGray, type: ShadingType.CLEAR },
                margins: { top: 100, bottom: 100, left: 80, right: 80 },
                children: [new Paragraph({ children: [new TextRun({ text: "" })] })],
              }),
        """
    if has_competency:
        extra_footers += """
              new TableCell({
                borders,
                width: { size: 1760, type: WidthType.DXA },
                shading: { fill: colors.lightGray, type: ShadingType.CLEAR },
                margins: { top: 100, bottom: 100, left: 80, right: 80 },
                children: [new Paragraph({ children: [new TextRun({ text: "" })] })],
              }),
        """

    subject_display = report.subject.replace("_", " ").title()

    # Populate template
    js_code = DOCX_GENERATOR_TEMPLATE.format(
        report_json=json.dumps(report_dict),
        column_widths=column_widths_str,
        extra_column_headers=extra_headers,
        data_rows=data_rows,
        extra_column_footers=extra_footers,
        period_profile_name=report.period_profile_name,
        total_periods=report.total_periods,
        allocation_note_text=allocation_note.replace('"', '\\"'),
        optional_notes_section=optional_notes,
        subject_display=subject_display,
    )

    # Write JS to temp file and execute
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
        f.write(js_code)
        js_path = f.name

    try:
        result = subprocess.run(
            ["node", js_path],
            capture_output=True,
            check=True,
            timeout=30,
        )
        return result.stdout
    finally:
        Path(js_path).unlink(missing_ok=True)
