"""Invoice PDF (2026-08-26) — the document a teacher keeps for a purchase.

Same family as the other exports (export_allocation_pdf → export_data_rights_pdf):
xhtml2pdf, table layout, Georgia masthead with the clay dot, heavy rule as a one-cell
table, hairline tables. The reference the founder gave was a Stripe-style receipt mail:
number block top-right, line items, a totals ladder, and nothing else on the page.

What this document deliberately does NOT claim:
  · no GSTIN and no tax line while Aruvi is not registered — it says "No tax charged"
    in words rather than printing a 0.00 tax row, which reads like a rate that happens
    to be zero. `seller_gstin`/`tax_amount` are honoured when config supplies them, so
    registering is a config change, not a rewrite.
  · no "payment received" wording beyond what is true: online payment is not open, so
    the method line says the activation was recorded manually.
  · never the word "certified" (house rule) — Aruvi is NCF *aligned*.

Money is whole rupees, formatted with Indian digit grouping (1,00,000 — not 100,000).
Takes a ports.Invoice; storage and numbering happen before it gets here.
"""
from __future__ import annotations

import html as _html
from datetime import date, datetime
from typing import Any, Dict

from .pdf_fonts import font_face_css
from .ports import Invoice

PINE = "#164436"
CLAY = "#b65a31"
INK = "#1a1917"
LINE = "#dddddd"
HEAD = "#f1ece2"


def _esc(s) -> str:
    return _html.escape(str(s or ""))


def rupees(n: int) -> str:
    """12345 → 12,345 · 100000 → 1,00,000 (Indian grouping: last three, then pairs)."""
    s = str(abs(int(n)))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts + [tail])
    return ("-" if int(n) < 0 else "") + s


def _date(iso: str) -> str:
    """2027-08-26 or a full timestamp → 26 August 2027."""
    raw = str(iso or "")
    try:
        d = datetime.fromisoformat(raw).date() if len(raw) > 10 else date.fromisoformat(raw)
        return f"{d.day} {d.strftime('%B')} {d.year}"
    except ValueError:
        return raw


def render_invoice_html(inv: Invoice) -> str:
    """xhtml2pdf-friendly invoice (tables only — no flexbox, no rounded corners)."""
    rows = "".join(
        f'<tr>'
        f'<td class="li-d">{_esc(ln.description)}'
        + (f'<br/><span class="li-sub">Valid {_date(ln.valid_from)} to '
           f'{_date(ln.valid_until)}</span>' if ln.valid_until else "")
        + f'</td>'
        f'<td class="li-q">{int(ln.quantity)}</td>'
        f'<td class="li-a">&#8377;{rupees(ln.unit_amount * int(ln.quantity or 1))}</td>'
        f'</tr>'
        for ln in (inv.lines or [])
    )

    # The totals ladder. A tax ROW appears only when tax was actually charged; otherwise
    # the note says so in words (see the module docstring).
    tax_row = ""
    if inv.tax_amount:
        tax_row = (f'<tr><td class="tt-k">Tax</td>'
                   f'<td class="tt-v">&#8377;{rupees(inv.tax_amount)}</td></tr>')

    bill_rows = "".join(
        f'<tr><td class="kv-k">{_esc(k)}</td><td class="kv-v">{_esc(v)}</td></tr>'
        for k, v in (("Name", inv.bill_to_name), ("Mobile", inv.bill_to_phone),
                     ("Email", inv.bill_to_email), ("School", inv.bill_to_school),
                     ("Place", inv.bill_to_place))
        if str(v or "").strip()
    )

    gstin = (f'<div class="seller-gstin">GSTIN {_esc(inv.seller_gstin)}</div>'
             if inv.seller_gstin else "")

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>{font_face_css()}
  @page {{ size: a4 portrait; margin: 1.6cm 1.5cm 1.9cm 1.5cm;
           @frame footer {{ -pdf-frame-content: footerContent; bottom: 1.0cm;
                            margin-left: 1.5cm; margin-right: 1.5cm; height: 1cm; }} }}
  body {{ font-family: Helvetica; font-size: 8pt; color: {INK}; }}

  .hdr {{ width: 100%; }}
  .brand-aruvi {{ font-family: Georgia, "Times New Roman", serif; font-size: 16pt;
                  font-weight: bold; color: {PINE}; }}
  .brand-dot {{ font-family: Georgia, serif; font-size: 16pt; font-style: italic; color: {CLAY}; }}
  .brand-studio {{ font-size: 7pt; letter-spacing: 1.5px; color: #6b6a63; }}
  .brand-ncf {{ font-family: Georgia, serif; font-style: italic; font-size: 7.5pt; color: #6b6a63; }}
  .seller-gstin {{ font-size: 7pt; color: #6b6a63; margin-top: 2px; }}
  .doc-t {{ font-family: Georgia, serif; font-size: 13pt; font-weight: bold; color: {PINE};
            text-align: right; }}
  .doc-n {{ font-size: 8pt; color: #555; text-align: right; padding-top: 3px; }}
  .rule-tbl {{ width: 100%; margin-top: 10px; margin-bottom: 14px; }}
  .rule-tbl td {{ border-bottom: 2px solid {INK}; font-size: 1pt; line-height: 1pt; }}

  /* ★ THE AMOUNT BAND STAYS ON THE INVOICE (founder, 2026-08-26, correcting a
     misreading of his own earlier note): the big figure was struck from the EMAIL
     ALONE. The two documents want opposite things — the mail says what is now hers and
     for how long, so the amount is a ledger line there; the invoice is the document
     ABOUT the money, so the amount is its headline. */
  .amount-band {{ width: 100%; margin-bottom: 14px; }}
  .amount-band td {{ background-color: {HEAD}; padding: 10px 12px; }}
  .ab-k {{ font-size: 6.5pt; letter-spacing: 1px; color: {PINE}; }}
  .ab-v {{ font-family: Georgia, serif; font-size: 15pt; font-weight: bold; color: {INK}; }}
  .ab-r {{ text-align: right; font-size: 7.5pt; color: #555; }}

  .section-head {{ font-family: Georgia, serif; font-size: 9.5pt; font-weight: bold; color: {INK};
                   border-bottom: 1.25px solid {INK}; padding-bottom: 3px;
                   margin-top: 6px; margin-bottom: 7px; }}

  .kv-table {{ width: 100%; margin-bottom: 10px; }}
  .kv-k {{ width: 2.8cm; font-size: 7.5pt; color: #888; padding: 3px 6px;
           border-bottom: 0.5px solid #efefef; }}
  .kv-v {{ font-size: 8pt; color: {INK}; padding: 3px 6px; border-bottom: 0.5px solid #efefef; }}

  .li-table {{ width: 100%; margin-bottom: 8px; }}
  .li-table th {{ font-size: 6.5pt; color: #888; font-weight: normal; text-transform: uppercase;
                  letter-spacing: 0.5px; padding: 5px 6px;
                  border-top: 0.75px solid #cccccc; border-bottom: 0.75px solid {LINE}; }}
  .th-d {{ text-align: left; }}  .th-q {{ text-align: center; }}  .th-a {{ text-align: right; }}
  .li-d {{ font-size: 8.5pt; color: {INK}; padding: 7px 6px; border-bottom: 0.5px solid #efefef; }}
  .li-sub {{ font-size: 7pt; color: #6b6a63; font-style: italic; }}
  .li-q {{ font-size: 8pt; color: #2a2a2a; padding: 7px 6px; text-align: center;
           border-bottom: 0.5px solid #efefef; }}
  .li-a {{ font-size: 8.5pt; color: {INK}; padding: 7px 6px; text-align: right;
           border-bottom: 0.5px solid #efefef; }}

  .tt {{ width: 45%; margin-left: 55%; margin-top: 2px; }}
  .tt-k {{ font-size: 8pt; color: #555; padding: 3px 6px; text-align: right; }}
  .tt-v {{ font-size: 8pt; color: {INK}; padding: 3px 6px; text-align: right; width: 3.2cm; }}
  .tt-total .tt-k, .tt-total .tt-v {{ font-family: Georgia, serif; font-size: 10pt;
       font-weight: bold; color: {INK}; border-top: 1.25px solid {INK};
       border-bottom: 1.25px solid {INK}; padding: 6px; }}
  .tt-paid .tt-k, .tt-paid .tt-v {{ font-size: 8pt; color: {PINE}; padding-top: 6px; }}

  .note {{ font-size: 7.5pt; color: #6b6a63; margin-top: 14px; line-height: 1.5; }}
  .note-em {{ font-family: Georgia, serif; font-style: italic; }}
  .footer-line {{ font-size: 6.5pt; color: #999; text-align: center; }}
</style></head><body>

  <table class="hdr"><tr>
    <td><span class="brand-aruvi">Aruvi</span><span class="brand-dot">.</span>
        <span class="brand-studio">LESSON STUDIO</span><br/>
        <span class="brand-ncf">NCF 2023 aligned</span>{gstin}</td>
    <td><div class="doc-t">Invoice</div>
        <div class="doc-n">{_esc(inv.number)}<br/>{_date(inv.issued_at)}</div></td>
  </tr></table>
  <table class="rule-tbl"><tr><td></td></tr></table>

  <table class="amount-band"><tr>
    <td><div class="ab-k">AMOUNT PAID</div>
        <div class="ab-v">&#8377;{rupees(inv.amount_paid)}</div></td>
    <td class="ab-r">{_esc(inv.payment_method)}<br/>Paid {_date(inv.issued_at)}</td>
  </tr></table>

  <div class="section-head">Billed to</div>
  <table class="kv-table">{bill_rows}</table>

  <div class="section-head">What you bought</div>
  <table class="li-table">
    <tr><th class="th-d" width="64%">Subscription</th>
        <th class="th-q" width="10%">Qty</th>
        <th class="th-a" width="26%">Amount</th></tr>
    {rows}
  </table>

  <table class="tt">
    <tr><td class="tt-k">Subtotal</td><td class="tt-v">&#8377;{rupees(inv.subtotal)}</td></tr>
    {tax_row}
    <tr class="tt-total"><td class="tt-k">Total</td>
        <td class="tt-v">&#8377;{rupees(inv.total)}</td></tr>
    <tr class="tt-paid"><td class="tt-k">Amount paid</td>
        <td class="tt-v">&#8377;{rupees(inv.amount_paid)}</td></tr>
  </table>

  <p class="note">{_esc(inv.tax_note)}
  Each subscription above covers its subject and stage for the dates shown — every class
  in that stage, every section you teach, unlimited lesson plans.
  <span class="note-em">Questions about this invoice? Reply to the email it came with.</span></p>

  <div id="footerContent" class="footer-line">Aruvi · Lesson Studio &nbsp;·&nbsp; {_esc(inv.number)}</div>
</body></html>"""


def export_invoice_pdf(inv: Invoice) -> bytes:
    """Render one invoice to PDF bytes via xhtml2pdf (pure-Python, no system libs)."""
    from io import BytesIO
    from xhtml2pdf import pisa
    buf = BytesIO()
    result = pisa.CreatePDF(render_invoice_html(inv), dest=buf, encoding="utf-8")
    if result.err:
        raise RuntimeError(f"xhtml2pdf failed with {result.err} error(s)")
    return buf.getvalue()
