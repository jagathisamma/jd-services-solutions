"""Regression tests for public-site SEO and accessibility metadata guards."""

import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "scripts"
    / "check_public_site.py"
)
SPEC = importlib.util.spec_from_file_location("check_public_site", SCRIPT_PATH)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

VALID_DOCUMENT = """<!doctype html>
<html lang="en">
<head>
  <title>JD Services &amp; Solutions | Repair in Erode</title>
  <meta name="description" content="Repair support in Erode.">
  <meta property="og:title" content="JD Services &amp; Solutions">
  <meta property="og:description" content="Repair support in Erode.">
</head>
<body>
  <h1>Repair made simpler</h1>
  <img src="decorative.svg" alt="">
</body>
</html>
"""


def parse_document(markup):
    parser = CHECKER.PublicSiteParser()
    parser.feed(markup)
    parser.close()
    return parser


class PublicSiteMetadataTests(unittest.TestCase):
    def assert_metadata_rejected(self, markup, message):
        with self.assertRaisesRegex(SystemExit, message):
            CHECKER.validate_document_metadata(parse_document(markup))

    def test_complete_metadata_is_accepted(self):
        CHECKER.validate_document_metadata(parse_document(VALID_DOCUMENT))

    def test_missing_document_language_is_rejected(self):
        self.assert_metadata_rejected(
            VALID_DOCUMENT.replace('<html lang="en">', "<html>"),
            "language attribute",
        )

    def test_missing_or_empty_title_is_rejected(self):
        self.assert_metadata_rejected(
            VALID_DOCUMENT.replace(
                "<title>JD Services &amp; Solutions | Repair in Erode</title>",
                "<title>   </title>",
            ),
            "document title",
        )

    def test_missing_description_is_rejected(self):
        self.assert_metadata_rejected(
            VALID_DOCUMENT.replace(
                '<meta name="description" content="Repair support in Erode.">',
                "",
            ),
            'meta name="description"',
        )

    def test_empty_description_is_rejected(self):
        self.assert_metadata_rejected(
            VALID_DOCUMENT.replace(
                'content="Repair support in Erode."',
                'content=""',
                1,
            ),
            'meta name="description"',
        )

    def test_empty_open_graph_values_are_rejected(self):
        empty_title = VALID_DOCUMENT.replace(
            'property="og:title" content="JD Services &amp; Solutions"',
            'property="og:title" content=""',
        )
        self.assert_metadata_rejected(empty_title, "og:title")

        empty_description = VALID_DOCUMENT.replace(
            'property="og:description" content="Repair support in Erode."',
            'property="og:description" content=""',
        )
        self.assert_metadata_rejected(empty_description, "og:description")

    def test_missing_open_graph_title_is_rejected(self):
        self.assert_metadata_rejected(
            VALID_DOCUMENT.replace(
                '<meta property="og:title" content="JD Services &amp; Solutions">',
                "",
            ),
            "og:title",
        )

    def test_missing_open_graph_description_is_rejected(self):
        self.assert_metadata_rejected(
            VALID_DOCUMENT.replace(
                '<meta property="og:description" content="Repair support in Erode.">',
                "",
            ),
            "og:description",
        )

    def test_zero_primary_headings_is_rejected(self):
        self.assert_metadata_rejected(
            VALID_DOCUMENT.replace("<h1>Repair made simpler</h1>", ""),
            "found 0",
        )

    def test_multiple_primary_headings_are_rejected(self):
        self.assert_metadata_rejected(
            VALID_DOCUMENT.replace(
                "</h1>",
                "</h1><h1>Another heading</h1>",
            ),
            "found 2",
        )

    def test_image_without_alt_attribute_is_rejected(self):
        self.assert_metadata_rejected(
            VALID_DOCUMENT.replace('alt=""', ""),
            "missing an alt attribute",
        )

    def test_empty_alt_attribute_is_allowed_for_decorative_images(self):
        CHECKER.validate_document_metadata(parse_document(VALID_DOCUMENT))


if __name__ == "__main__":
    unittest.main()
