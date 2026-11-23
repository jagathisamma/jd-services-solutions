#!/usr/bin/env python3
"""Dependency-free smoke checks for JD's public website conversion paths."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_DISPLAY = "8940454260"
EXPECTED_E164 = "+918940454260"
EXPECTED_WHATSAPP = "918940454260"
LEGACY_CONTACTS = ("8940454360", "+918940454360", "918940454360")
SOURCE_FILES = (
    "index.html",
    "README.md",
    "AGENTS.md",
    "docs/BRAND_GUIDE.md",
    "data/config/site.yml",
    "data/config/brand.yml",
)
REQUIRED_SECTIONS = {
    "home",
    "services",
    "how-it-works",
    "service-options",
    "faq",
    "contact",
}


class PublicSiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.hrefs = []
        self.local_assets = []
        self.has_viewport = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        element_id = attrs.get("id")
        if element_id:
            self.ids.add(element_id)

        href = attrs.get("href")
        if href:
            self.hrefs.append(href)

        src = attrs.get("src")
        if tag == "img" and src:
            self.local_assets.append(src)

        if tag == "link" and href:
            rel = (attrs.get("rel") or "").lower().split()
            if "icon" in rel:
                self.local_assets.append(href)

        if tag == "meta" and (attrs.get("name") or "").lower() == "viewport":
            self.has_viewport = True


def fail(message):
    raise SystemExit(f"PUBLIC SITE SMOKE TEST FAILED: {message}")


def main():
    contents = {}
    for relative_path in SOURCE_FILES:
        path = ROOT / relative_path
        if not path.is_file():
            fail(f"required source file is missing: {relative_path}")
        contents[relative_path] = path.read_text(encoding="utf-8")

    for relative_path, content in contents.items():
        for legacy in LEGACY_CONTACTS:
            if legacy in content:
                fail(f"superseded contact number {legacy} remains in {relative_path}")

    html = contents["index.html"]
    for expected in (EXPECTED_DISPLAY, EXPECTED_E164, EXPECTED_WHATSAPP):
        if expected not in html:
            fail(f"index.html is missing canonical contact form: {expected}")

    config_expectations = {
        "data/config/site.yml": (
            f'phoneDisplay: "{EXPECTED_DISPLAY}"',
            f'phoneE164: "{EXPECTED_E164}"',
        ),
        "data/config/brand.yml": (
            f'phone_display: "{EXPECTED_DISPLAY}"',
            f'phone_e164: "{EXPECTED_E164}"',
        ),
    }
    for relative_path, expected_values in config_expectations.items():
        for expected in expected_values:
            if expected not in contents[relative_path]:
                fail(f"{relative_path} is missing canonical setting: {expected}")

    parser = PublicSiteParser()
    parser.feed(html)
    parser.close()

    missing_sections = REQUIRED_SECTIONS - parser.ids
    if missing_sections:
        fail("required page sections are missing: " + ", ".join(sorted(missing_sections)))

    if not parser.has_viewport:
        fail("responsive viewport meta tag is missing")

    fragments = {href[1:] for href in parser.hrefs if href.startswith("#") and len(href) > 1}
    broken_fragments = fragments - parser.ids
    if broken_fragments:
        fail("internal links target missing IDs: " + ", ".join(sorted(broken_fragments)))

    tel_links = [href for href in parser.hrefs if href.startswith("tel:")]
    if not tel_links:
        fail("no click-to-call link was found")
    if any(href != f"tel:{EXPECTED_E164}" for href in tel_links):
        fail("one or more click-to-call links use a non-canonical number")

    whatsapp_links = [
        href for href in parser.hrefs
        if urlsplit(href).hostname == "wa.me"
    ]
    if not whatsapp_links:
        fail("no WhatsApp enquiry link was found")
    if any(urlsplit(href).path != f"/{EXPECTED_WHATSAPP}" for href in whatsapp_links):
        fail("one or more WhatsApp links use a non-canonical number")

    for asset in sorted(set(parser.local_assets)):
        parsed = urlsplit(asset)
        if parsed.scheme or parsed.netloc:
            continue
        asset_path = (ROOT / parsed.path.lstrip("/")).resolve()
        if ROOT.resolve() not in asset_path.parents:
            fail(f"local asset path escapes repository root: {asset}")
        if not asset_path.is_file():
            fail(f"referenced local asset does not exist: {asset}")

    print(
        "Public site smoke checks passed: canonical contact links, "
        "required sections, internal anchors, responsive viewport and local assets."
    )


if __name__ == "__main__":
    main()
