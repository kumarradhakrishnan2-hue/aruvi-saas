"""
PDF export for allocation reports using reportlab.
Renders with warm editorial design language consistent with web UI.
"""

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib import colors
from datetime import datetime

from .report_allocation import AllocationReport


# Design palette (matching web globals.css)
COLOR_PAPER = colors.HexColor("#fefaf4")
COLOR_INK = colors.HexColor("#1a1410")
COLOR_PINE = colors.HexColor("#2d5f4f")
COLOR_CLAY = colors.HexColor("#c89968")
COLOR_OCHRE = colors.HexColor("#d4a574")
COLOR_LINE = colors.HexColor("#d4c5b0")


def export_allocation_report_pdf(report: AllocationReport) -> bytes:
    """
    Generate allocation report PDF.

    Args:
        report: AllocationReport object

    Returns:
        PDF bytes
    """
    buffer = BytesIO()

    # Page setup: US Letter, 1-inch margins
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=1 * inch,
        leftMargin=1 * inch,
        topMargin=1 * inch,
        bottomMargin=0.75 * inch,
        title=f"Allocation Report - Grade {report.grade} - {report.subject}",
    )

    # Define custom styles
    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=COLOR_INK,
        spaceAfter=6,
        alignment=TA_LEFT,
        letterSpacing=-0.5,
    )

    # Subtitle style (small caps, mono)
    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Normal"],
        fontName="Courier-Bold",
        fontSize=8,
        textColor=COLOR_PINE,
        spaceAfter=4,
        alignment=TA_LEFT,
        letterSpacing=1.5,
    )

    # Date style
    date_style = ParagraphStyle(
        "DateStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=COLOR_INK,
        spaceAfter=12,
        alignment=TA_LEFT,
    )

    # Metadata label and value styles
    meta_label_style = ParagraphStyle(
        "MetaLabel",
        parent=styles["Normal"],
        fontName="Courier-Bold",
        fontSize=7,
        textColor=COLOR_PINE,
        letterSpacing=0.5,
    )

    meta_value_style = ParagraphStyle(
        "MetaValue",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=COLOR_INK,
    )

    # Note style
    note_style = ParagraphStyle(
        "NoteStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=COLOR_INK,
        leftIndent=10,
        rightIndent=10,
        spaceBefore=6,
    )

    # Footer style
    footer_style = ParagraphStyle(
        "FooterStyle",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7,
        textColor=COLOR_INK,
        alignment=TA_CENTER,
    )

    # Build story (content to render)
    story = []

    # ========== HEADER ==========
    subject_display = report.subject.replace("_", " ").title()

    story.append(
        Paragraph("ARUVI Period Allocation Report", title_style)
    )
    story.append(
        Paragraph(
            f"NCF 2023 · PEDAGOGICAL PLATFORM · GRADE {report.grade} · {report.subject.upper().replace('_', ' ')} · {report.generated_at.strftime('%Y-%m-%d')}",
            subtitle_style,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    # ========== METADATA BOX ==========
    metadata_data = [
        [
            Paragraph("PERIOD DURATION", meta_label_style),
            Paragraph(f"{report.period_duration_minutes} min", meta_value_style),
        ],
        [
            Paragraph("TOTAL PERIODS", meta_label_style),
            Paragraph(f"{report.total_periods}", meta_value_style),
        ],
        [
            Paragraph("ALLOCATION BASIS", meta_label_style),
            Paragraph(report.allocation_basis, meta_value_style),
        ],
    ]

    metadata_table = Table(metadata_data, colWidths=[2.5 * inch, 2.5 * inch])
    metadata_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f3f0")),
            ("LINEABOVE", (0, 0), (-1, 0), 0.5, COLOR_LINE),
            ("LINEBELOW", (0, -1), (-1, -1), 0.5, COLOR_LINE),
            ("LINEBETWEEN", (0, 0), (-1, -1), 0.5, COLOR_LINE),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#fafaf8")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    story.append(metadata_table)
    story.append(Spacer(1, 0.25 * inch))

    # ========== ALLOCATION TABLE ==========
    # Header row
    has_effort = any(r.effort_index is not None for r in report.rows)
    has_competency = any(r.competency_weight is not None for r in report.rows)

    table_data = [
        [
            Paragraph("<b>#</b>", ParagraphStyle("TH", parent=styles["Normal"], fontSize=8, textColor=colors.white, alignment=TA_CENTER)),
            Paragraph("<b>Chapter</b>", ParagraphStyle("TH", parent=styles["Normal"], fontSize=8, textColor=colors.white)),
            Paragraph("<b>Total Periods</b>", ParagraphStyle("TH", parent=styles["Normal"], fontSize=8, textColor=colors.white, alignment=TA_RIGHT)),
            Paragraph(f"<b>{report.period_profile_name} Periods</b>", ParagraphStyle("TH", parent=styles["Normal"], fontSize=8, textColor=colors.white, alignment=TA_RIGHT)),
        ]
    ]

    # Add optional columns
    if has_effort:
        table_data[0].append(
            Paragraph("<b>Effort Index</b>", ParagraphStyle("TH", parent=styles["Normal"], fontSize=8, textColor=colors.white, alignment=TA_RIGHT))
        )
    if has_competency:
        table_data[0].append(
            Paragraph("<b>Competency Weight</b>", ParagraphStyle("TH", parent=styles["Normal"], fontSize=8, textColor=colors.white, alignment=TA_RIGHT))
        )

    # Data rows
    total_allocated = 0
    for row in report.rows:
        total_allocated += row.allocated_periods
        row_data = [
            Paragraph(str(row.chapter_number), ParagraphStyle("TD", parent=styles["Normal"], fontSize=8, alignment=TA_CENTER)),
            Paragraph(row.chapter_name, ParagraphStyle("TD", parent=styles["Normal"], fontSize=8)),
            Paragraph(str(row.total_periods), ParagraphStyle("TD", parent=styles["Normal"], fontSize=8, alignment=TA_RIGHT)),
            Paragraph(f"<b>{row.allocated_periods}</b>", ParagraphStyle("TD", parent=styles["Normal"], fontSize=8, textColor=COLOR_CLAY, alignment=TA_RIGHT)),
        ]

        if has_effort:
            effort_text = f"{row.effort_index:.1f}" if row.effort_index is not None else "—"
            row_data.append(Paragraph(effort_text, ParagraphStyle("TD", parent=styles["Normal"], fontSize=8, alignment=TA_RIGHT)))
        if has_competency:
            weight_text = f"{row.competency_weight * 100:.0f}%" if row.competency_weight is not None else "—"
            row_data.append(Paragraph(weight_text, ParagraphStyle("TD", parent=styles["Normal"], fontSize=8, alignment=TA_RIGHT)))

        table_data.append(row_data)

    # Total row
    total_row = [
        Paragraph("", styles["Normal"]),
        Paragraph("<b>Total</b>", ParagraphStyle("TDTotal", parent=styles["Normal"], fontSize=8, textColor=COLOR_INK)),
        Paragraph("", styles["Normal"]),
        Paragraph(f"<b>{total_allocated}</b>", ParagraphStyle("TDTotal", parent=styles["Normal"], fontSize=8, textColor=COLOR_CLAY, alignment=TA_RIGHT)),
    ]

    if has_effort:
        total_row.append(Paragraph("", styles["Normal"]))
    if has_competency:
        total_row.append(Paragraph("", styles["Normal"]))

    table_data.append(total_row)

    # Column widths
    col_widths = [0.4 * inch, 2.2 * inch, 1.0 * inch, 1.0 * inch]
    if has_effort:
        col_widths.append(1.0 * inch)
    if has_competency:
        col_widths.append(1.2 * inch)

    allocation_table = Table(table_data, colWidths=col_widths)
    allocation_table.setStyle(
        TableStyle([
            # Header styling
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_PINE),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, 0), "LEFT"),
            ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, 0), "Courier-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 7),
            ("LEFTPADDING", (0, 0), (-1, 0), 6),
            ("RIGHTPADDING", (0, 0), (-1, 0), 6),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            # Data rows
            ("BACKGROUND", (0, 1), (-1, len(table_data) - 2), colors.white),
            ("ROWBACKGROUNDS", (0, 1), (-1, len(table_data) - 2), [colors.white, colors.HexColor("#fafaf8")]),
            ("TEXTCOLOR", (0, 1), (-1, -2), COLOR_INK),
            ("ALIGN", (0, 1), (0, -2), "CENTER"),
            ("ALIGN", (2, 1), (-1, -2), "RIGHT"),
            ("VALIGN", (0, 1), (-1, -2), "MIDDLE"),
            ("FONTNAME", (0, 1), (-1, -2), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -2), 8),
            ("LEFTPADDING", (0, 1), (-1, -2), 6),
            ("RIGHTPADDING", (0, 1), (-1, -2), 6),
            ("TOPPADDING", (0, 1), (-1, -2), 6),
            ("BOTTOMPADDING", (0, 1), (-1, -2), 6),

            # Total row
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f0ede8")),
            ("TEXTCOLOR", (0, -1), (-1, -1), COLOR_INK),
            ("LINEABOVE", (0, -1), (-1, -1), 1.5, COLOR_PINE),
            ("LINEBELOW", (0, -1), (-1, -1), 1.5, COLOR_PINE),
            ("ALIGN", (2, -1), (-1, -1), "RIGHT"),
            ("VALIGN", (0, -1), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, -1), (-1, -1), "Courier-Bold"),
            ("FONTSIZE", (0, -1), (-1, -1), 8),
            ("LEFTPADDING", (0, -1), (-1, -1), 6),
            ("RIGHTPADDING", (0, -1), (-1, -1), 6),
            ("TOPPADDING", (0, -1), (-1, -1), 8),
            ("BOTTOMPADDING", (0, -1), (-1, -1), 8),

            # All grid lines
            ("GRID", (0, 0), (-1, -1), 0.5, COLOR_LINE),
        ])
    )

    story.append(allocation_table)
    story.append(Spacer(1, 0.25 * inch))

    # ========== ALLOCATION BASIS NOTE ==========
    note_title = Paragraph("<b>How are periods allocated?</b>", ParagraphStyle("NoteTitle", parent=styles["Normal"], fontSize=9, textColor=COLOR_CLAY))
    story.append(note_title)

    if report.allocation_basis == "Effort Index":
        note_text = "Periods are allocated proportionally based on the effort index for each chapter. Chapters with higher effort indices receive more time to ensure mastery. Learn more in the Ask Aruvi helpline."
    elif report.allocation_basis == "Competency Weights":
        note_text = "Periods are allocated according to the relative weight of competencies covered in each chapter. Learn more in the Ask Aruvi helpline."
    else:
        note_text = "Periods are allocated according to a custom allocation strategy defined for this curriculum. Learn more in the Ask Aruvi helpline."

    story.append(Paragraph(note_text, note_style))
    story.append(Spacer(1, 0.2 * inch))

    # ========== OPTIONAL REPORT NOTES ==========
    if report.notes:
        story.append(Paragraph("<b>Notes:</b>", ParagraphStyle("NotesTitle", parent=styles["Normal"], fontSize=9, textColor=COLOR_PINE)))
        story.append(Paragraph(report.notes, note_style))
        story.append(Spacer(1, 0.2 * inch))

    # ========== FOOTER ==========
    story.append(Spacer(1, 0.1 * inch))
    footer_text = f"Aruvi · Period Allocation Report · Grade {report.grade} · {subject_display} · Page 1 of 1 · Confidential"
    story.append(Paragraph(footer_text, footer_style))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
