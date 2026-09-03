"""Tests for the Notifier port, its file adapter, and the subscription-confirmation copy.

Stdlib only, like every other suite here: `python3 tests/test_notifier.py`.

What is deliberately NOT tested: SmtpNotifier's actual delivery. It needs a live server
and credentials, so the contract that matters — "never raises, reports what happened" —
is asserted against its unconfigured path instead.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aruvi_core.adapters.file_notifier import FileNotifier          # noqa: E402
from aruvi_core.adapters.smtp_notifier import SmtpNotifier          # noqa: E402
from aruvi_core.ports import EmailMessage, Notifier                 # noqa: E402
from api import mail_templates                                      # noqa: E402


def test_adapters_satisfy_the_port():
    assert isinstance(FileNotifier("/tmp"), Notifier)
    assert isinstance(SmtpNotifier("", 587, "", ""), Notifier)
    print("✓ both adapters satisfy the Notifier protocol")


def test_file_notifier_writes_a_readable_message():
    with tempfile.TemporaryDirectory() as d:
        n = FileNotifier(d, from_addr="sender@example.com")
        r = n.send(EmailMessage(to="teacher@example.com", subject="Hello",
                                text="Body line", reply_to="reply@example.com"))
        assert r["status"] == "written", r
        with open(r["path"]) as f:
            body = f.read()
        for expected in ("From: sender@example.com", "To: teacher@example.com",
                         "Reply-To: reply@example.com", "Subject: Hello", "Body line"):
            assert expected in body, f"missing {expected!r} in\n{body}"
    print("✓ file notifier writes a complete, readable message")


def test_no_recipient_is_skipped_not_an_error():
    """A teacher who never gave an email must not produce an error path."""
    with tempfile.TemporaryDirectory() as d:
        r = FileNotifier(d).send(EmailMessage(to="", subject="x", text="y"))
        assert r["status"] == "skipped", r
    print("✓ a missing address is skipped, not an error")


def test_notifier_never_raises_on_transport_failure():
    """THE contract: a subscription must never fail because mail failed."""
    r = FileNotifier("/proc/nonexistent-cannot-mkdir").send(
        EmailMessage(to="a@b.com", subject="x", text="y"))
    assert r["status"] in ("error", "written"), r
    r2 = SmtpNotifier("", 587, "", "").send(EmailMessage(to="a@b.com", subject="x", text="y"))
    assert r2["status"] == "skipped", r2
    r3 = SmtpNotifier("smtp.invalid.example", 587, "u", "p", timeout=1).send(
        EmailMessage(to="a@b.com", subject="x", text="y"))
    assert r3["status"] == "error", r3
    print("✓ no transport failure ever raises")


def test_confirmation_names_what_she_bought():
    m = mail_templates.subscription_confirmation(
        "meera krishnan", ["social_sciences/middle", "english/middle"],
        1000, "2027-08-26", "9876543210")
    t = m["text"]
    assert m["subject"] == "Your Meyy subscriptions are active", m["subject"]
    assert "Hello Meera," in t                       # first name only, capitalised
    assert "Social Sciences · Middle" in t
    assert "English · Middle" in t
    assert "Classes 6, 7 and 8" in t
    assert "₹1,000" in t
    assert "26-Aug-2027" in t
    assert "9876543210" in t                         # her sign-in, in writing
    print("✓ confirmation names the scopes, amount, validity and sign-in")


def test_confirmation_singular_and_enterprise():
    one = mail_templates.subscription_confirmation(
        "ravi", ["science/secondary"], 500, "2027-01-01", "9000000000")
    assert one["subject"] == "Your Meyy subscription is active"
    assert "Class 9 (Class 10 coming soon)" in one["text"]
    star = mail_templates.subscription_confirmation("", ["*"], 5000, "2027-01-01", "9000000000")
    assert "All subjects · All stages" in star["text"]
    assert "Hello," in star["text"]                  # no name → no awkward blank
    print("✓ singular, secondary-class wording and the '*' grant all read correctly")


def test_copy_never_claims_certification():
    """CLAUDE.md / the subscription model: 'NCF aligned', never 'certified'.
    Checked in BOTH parts — an HTML body is a second place for copy to drift."""
    body = mail_templates.subscription_confirmation(
        "a", ["maths/middle"], 500, "2027-01-01", "9000000000")
    for part in (body["text"].lower(), body.get("html", "").lower()):
        assert "certified" not in part
        assert "certification" not in part
    print("✓ copy says aligned, never certified (text and HTML)")


def test_html_part_says_everything_the_text_does():
    """★ The HTML body (2026-08-26) is styling, never information. A client that refuses
    HTML — or a screen reader taking the text part — must lose nothing, so every FACT is
    asserted in both halves. It is also built for mail clients, not browsers: tables,
    inline styles, no <style> block (Gmail strips it), no web fonts."""
    body = mail_templates.subscription_confirmation(
        name="Kumar", scopes=["english/middle", "science/middle"], amount_inr=500,
        valid_until="2027-08-26", mobile="1000000000",
        scope_valid_until={"english/middle": "2027-02-01",
                           "science/middle": "2027-08-26"},
        added=["science/middle"], invoice_number="ARV/2026-27/0009",
        unit_amount=500, has_attachment=True)
    html = body["html"]
    assert html.lstrip().startswith("<!DOCTYPE html>")
    for fact in ("Kumar", "Science", "English", "1000000000", "ARV/2026-27/0009", "500"):
        assert fact in html, fact
        assert fact in body["text"], fact
    # The holding block dates every row — that is the whole reason it exists.
    assert "26-Aug-2027" in html and "01-Feb-2027" in html
    assert "<style" not in html.lower(), "inline styles only — Gmail strips <style>"
    assert "flex" not in html.lower() and "grid-template" not in html.lower()
    assert "@import" not in html and "fonts.googleapis" not in html
    print("✓ The HTML part carries every fact the text does, in mail-client markup")


def test_letterhead_wordmark_travels_inline_by_cid():
    """★ THE LETTERHEAD IS THE MEYY WORDMARK (2026-09-03), and it must ARRIVE. Both HTML
    frames reference it as `cid:`; `mail_templates.inline_images()` is the matching
    image; SmtpNotifier embeds it as a multipart/related part of the HTML alternative
    (the one inline form Gmail renders — data: URIs are stripped, and there is no host
    yet for a URL). Three things are pinned: (a) every frame that references the cid is
    paired with the image; (b) the built MIME message really is
    alternative[text, related[html, image/png with that Content-ID]]; (c) the image is
    NOT an attachment — a plain-text client must not receive a stray PNG, and the
    invoice count in test_invoice stays honest."""
    from aruvi_core import brand
    from aruvi_core.ports import Attachment

    sub = mail_templates.subscription_confirmation(
        name="Kumar", scopes=["english/middle"], amount_inr=500, valid_until="2027-08-26",
        mobile="1000000000", scope_valid_until={"english/middle": "2027-08-26"},
        added=None, invoice_number="", unit_amount=500, has_attachment=False)
    sup = mail_templates.support_acknowledgement(
        name="Kumar", reference="ARV-S-742", category="problem", message="It broke.",
        reply_days=2, received_on="2026-09-03", context={})
    cid = f"cid:{brand.EMAIL_CID}"
    for html in (sub["html"], sup["html"]):
        assert cid in html, "frame references the wordmark by cid"
        assert "Meyy</span>" not in html, "the typeset name is gone from the letterhead"
        assert 'alt="Meyy"' in html, "images-off clients still read the name"
    imgs = mail_templates.inline_images()
    assert len(imgs) == 1 and isinstance(imgs[0], Attachment)
    assert imgs[0].content_id == brand.EMAIL_CID and imgs[0].mime_type == "image/png"
    assert imgs[0].content[:8] == b"\x89PNG\r\n\x1a\n", "a real PNG, from the shipped raster"

    # (b) + (c): build the MIME message exactly as SmtpNotifier does, capturing instead
    # of sending. smtplib is patched at the module the adapter imported it into.
    import smtplib
    from aruvi_core.adapters import smtp_notifier as mod
    captured = {}

    class _FakeSMTP:
        def __init__(self, *a, **k): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def ehlo(self): pass
        def starttls(self, context=None): pass
        def login(self, u, p): pass
        def send_message(self, m): captured["msg"] = m

    real = mod.smtplib.SMTP
    mod.smtplib.SMTP = _FakeSMTP
    try:
        r = SmtpNotifier("smtp.example.com", 587, "u", "p", from_addr="a@example.com").send(
            EmailMessage(to="t@example.com", subject="s", text="plain", html=sub["html"],
                         attachments=[Attachment("Meyy-invoice-1.pdf", b"%PDF-1.4")],
                         inline=imgs))
    finally:
        mod.smtplib.SMTP = real
    assert r["status"] == "sent", r
    m = captured["msg"]
    assert m.get_content_type() == "multipart/mixed", m.get_content_type()
    alt = m.get_payload()[0]
    assert alt.get_content_type() == "multipart/alternative"
    text_part, html_holder = alt.get_payload()
    assert text_part.get_content_type() == "text/plain"
    assert html_holder.get_content_type() == "multipart/related", html_holder.get_content_type()
    html_part, img_part = html_holder.get_payload()
    assert html_part.get_content_type() == "text/html"
    assert img_part.get_content_type() == "image/png"
    assert img_part["Content-ID"] == f"<{brand.EMAIL_CID}>"
    # the invoice is the ONLY thing attached; the wordmark is not one of her files
    attached = [p for p in m.iter_attachments()]
    assert [p.get_filename() for p in attached] == ["Meyy-invoice-1.pdf"], \
        [p.get_filename() for p in attached]
    # and a mail with NO html part carries no orphan image at all
    mod.smtplib.SMTP = _FakeSMTP
    try:
        SmtpNotifier("smtp.example.com", 587, "u", "p").send(
            EmailMessage(to="t@example.com", subject="s", text="plain", inline=imgs))
    finally:
        mod.smtplib.SMTP = real
    assert captured["msg"].get_content_type() == "text/plain"
    print("✓ The wordmark rides inline by cid inside the HTML part — never as an attachment")


if __name__ == "__main__":
    test_adapters_satisfy_the_port()
    test_file_notifier_writes_a_readable_message()
    test_no_recipient_is_skipped_not_an_error()
    test_notifier_never_raises_on_transport_failure()
    test_confirmation_names_what_she_bought()
    test_confirmation_singular_and_enterprise()
    test_copy_never_claims_certification()
    test_html_part_says_everything_the_text_does()
    test_letterhead_wordmark_travels_inline_by_cid()
    print("\n✅ All notifier tests passed!")
