"""Tests for deterministic, privacy-safe AGENTS.md project context generation."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "scripts"
    / "sync_agent_context.py"
)
SPEC = importlib.util.spec_from_file_location("sync_agent_context", SCRIPT)
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)

SOURCE_FILES = {
    "README.md": (
        "# JD Services & Solutions\n\n"
        "## Deployment\n"
        "The Render Static Site tracks the GitHub main branch and auto-deploys commits.\n"
    ),
    "docs/ARCHITECTURE.md": "# Architecture\n\n## Current runtime\n## Target architecture\n",
    "docs/FILE_DATABASE.md": "# File database\n\n## Directory contract\n## Privacy boundary\n",
    "docs/OPERATING_MODEL.md": "# Operating model\n\n## Decision authority\n## Delivery loop\n",
    "docs/RELEASE_RUNBOOK.md": "# Release runbook\n\n## Release states\n## Verification\n",
    "docs/PRODUCT_ROADMAP.md": (
        "# Roadmap\n\n"
        "| JD issue | JD capability | Source | Status |\n"
        "|---|---|---|---|\n"
        "| #2 | Operating platform | Internal | Open |\n"
        "| #11 | Agent context sync | Internal | Open |\n"
    ),
}


def make_root():
    temporary = tempfile.TemporaryDirectory()
    root = Path(temporary.name)
    for relative, content in SOURCE_FILES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    (root / "AGENTS.md").write_text(
        "# Human policy\n\nKeep this paragraph unchanged.\n",
        encoding="utf-8",
    )
    (root / ".github" / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "diagrams").mkdir(parents=True, exist_ok=True)
    return temporary, root


class AgentContextTests(unittest.TestCase):
    def test_sync_is_idempotent_and_preserves_human_policy(self):
        temporary, root = make_root()
        self.addCleanup(temporary.cleanup)
        self.assertEqual(SYNC.main(["--sync"], root), 0)
        first = (root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(SYNC.main(["--sync"], root), 0)
        second = (root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(first, second)
        self.assertTrue(second.startswith("# Human policy\n\nKeep this paragraph unchanged."))
        self.assertIn(SYNC.BEGIN_MARKER, second)
        self.assertIn(SYNC.END_MARKER, second)

    def test_check_fails_when_generated_block_is_stale(self):
        temporary, root = make_root()
        self.addCleanup(temporary.cleanup)
        self.assertEqual(SYNC.main(["--check"], root), 1)
        self.assertEqual(SYNC.main(["--sync"], root), 0)
        self.assertEqual(SYNC.main(["--check"], root), 0)

    def test_missing_source_fails(self):
        temporary, root = make_root()
        self.addCleanup(temporary.cleanup)
        (root / "docs" / "ARCHITECTURE.md").unlink()
        self.assertEqual(SYNC.run("check", root), 1)

    def test_malformed_roadmap_fails(self):
        temporary, root = make_root()
        self.addCleanup(temporary.cleanup)
        (root / "docs" / "PRODUCT_ROADMAP.md").write_text(
            "# Roadmap\n\nNo issue table here.\n", encoding="utf-8"
        )
        self.assertEqual(SYNC.run("check", root), 1)

    def test_duplicate_roadmap_issue_fails(self):
        temporary, root = make_root()
        self.addCleanup(temporary.cleanup)
        roadmap = root / "docs" / "PRODUCT_ROADMAP.md"
        roadmap.write_text(
            SOURCE_FILES["docs/PRODUCT_ROADMAP.md"]
            + "| #2 | Duplicate issue | Internal | Open |\n",
            encoding="utf-8",
        )
        self.assertEqual(SYNC.run("check", root), 1)

    def test_inventory_is_sorted_and_excludes_private_or_sensitive_paths(self):
        temporary, root = make_root()
        self.addCleanup(temporary.cleanup)
        for relative in (
            "docs/zeta",
            "docs/alpha",
            "data/records",
            "data/private",
            "runtime/uploads",
            "secrets",
        ):
            (root / relative).mkdir(parents=True, exist_ok=True)
        (root / ".env").write_text("API_KEY_SENTINEL", encoding="utf-8")
        (root / "data" / "records" / "customer.json").write_text(
            "CUSTOMER_PII_SENTINEL", encoding="utf-8"
        )
        (root / "data" / "private" / "secret.json").write_text(
            "PRIVATE_DATA_SENTINEL", encoding="utf-8"
        )
        generated = SYNC.render_context(root)
        self.assertLess(generated.index("docs/alpha/"), generated.index("docs/zeta/"))
        for forbidden in (
            "API_KEY_SENTINEL",
            "CUSTOMER_PII_SENTINEL",
            "PRIVATE_DATA_SENTINEL",
            "data/records",
            "data/private",
            "runtime/",
            "secrets/",
        ):
            self.assertNotIn(forbidden, generated)

    def test_marker_errors_are_rejected(self):
        with self.assertRaises(SYNC.ContextError):
            SYNC.replace_generated_block(
                "# Human\n\n" + SYNC.BEGIN_MARKER,
                SYNC.BEGIN_MARKER + "\n" + SYNC.END_MARKER,
            )

    def test_roadmap_order_is_numeric_and_deterministic(self):
        entries = SYNC.extract_roadmap_entries(
            "| #11 | Agent context | Source | Open |\n"
            "| #2 | Platform | Source | Open |\n"
        )
        self.assertEqual(entries, [("#2", "Platform"), ("#11", "Agent context")])


if __name__ == "__main__":
    unittest.main()
