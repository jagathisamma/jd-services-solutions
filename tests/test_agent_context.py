"""Tests for deterministic and privacy-safe AGENTS.md context generation."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "sync_agent_context.py"
)
SPEC = importlib.util.spec_from_file_location("sync_agent_context", SCRIPT_PATH)
GENERATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GENERATOR)

SYNTHETIC_SENTINEL = "SYNTHETIC-SECRET-MUST-NOT-APPEAR"


class AgentContextGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative_path in GENERATOR.SOURCE_DOCS:
            path = self.root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f"# {relative_path}\n## First section\n## Second section\n",
                encoding="utf-8",
            )

        (self.root / "docs").mkdir(exist_ok=True)
        agents = (
            "# Agent instructions\n\nHuman-authored policy stays here.\n\n"
            f"{GENERATOR.BEGIN_MARKER}\nplaceholder\n{GENERATOR.END_MARKER}\n"
            "\n## Human-authored closing policy\nKeep this text unchanged.\n"
        )
        (self.root / "AGENTS.md").write_text(agents, encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_sync_is_idempotent_and_check_passes(self):
        self.assertTrue(GENERATOR.sync(self.root))
        generated_once = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertFalse(GENERATOR.sync(self.root))
        self.assertEqual(
            generated_once,
            (self.root / "AGENTS.md").read_text(encoding="utf-8"),
        )
        self.assertFalse(GENERATOR.sync(self.root, check=True))

    def test_inventory_and_source_order_are_stable(self):
        (self.root / "tests").mkdir()
        (self.root / "assets").mkdir()
        (self.root / "data" / "records").mkdir(parents=True)
        block = GENERATOR.build_generated_block(self.root)
        self.assertLess(block.index("- assets/"), block.index("- data/records/"))
        self.assertLess(block.index("- data/records/"), block.index("- tests/"))
        self.assertLess(
            block.index("docs/ARCHITECTURE.md"),
            block.index("docs/FILE_DATABASE.md"),
        )

    def test_private_file_contents_and_unapproved_paths_are_excluded(self):
        private_dir = self.root / "data" / "records"
        private_dir.mkdir(parents=True)
        (private_dir / "synthetic-private-record.json").write_text(
            SYNTHETIC_SENTINEL,
            encoding="utf-8",
        )
        (self.root / ".env").write_text(SYNTHETIC_SENTINEL, encoding="utf-8")
        (self.root / "private").mkdir()
        (self.root / "private" / "credentials.txt").write_text(
            SYNTHETIC_SENTINEL,
            encoding="utf-8",
        )

        block = GENERATOR.build_generated_block(self.root)
        self.assertNotIn(SYNTHETIC_SENTINEL, block)
        self.assertNotIn(".env", block)
        self.assertNotIn("synthetic-private-record.json", block)
        self.assertNotIn("credentials.txt", block)

    def test_human_authored_sections_are_preserved(self):
        original = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        GENERATOR.sync(self.root)
        updated = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertTrue(updated.startswith(original.split(GENERATOR.BEGIN_MARKER)[0]))
        self.assertTrue(updated.endswith(original.split(GENERATOR.END_MARKER, 1)[1]))
        self.assertIn("Human-authored closing policy", updated)

    def test_check_mode_rejects_stale_generated_content(self):
        GENERATOR.sync(self.root)
        path = self.root / "AGENTS.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "Generated project context",
                "Stale generated project context",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(SystemExit, "is stale"):
            GENERATOR.sync(self.root, check=True)

    def test_missing_source_is_rejected(self):
        (self.root / GENERATOR.SOURCE_DOCS[0]).unlink()
        with self.assertRaisesRegex(SystemExit, "is missing"):
            GENERATOR.build_generated_block(self.root)

    def test_missing_or_duplicate_markers_are_rejected(self):
        with self.assertRaisesRegex(SystemExit, "exactly one pair"):
            GENERATOR.replace_generated_block("no markers", "generated")
        duplicated = (
            GENERATOR.BEGIN_MARKER
            + "\n"
            + GENERATOR.END_MARKER
            + "\n"
            + GENERATOR.BEGIN_MARKER
            + "\n"
            + GENERATOR.END_MARKER
        )
        with self.assertRaisesRegex(SystemExit, "exactly one pair"):
            GENERATOR.replace_generated_block(duplicated, "generated")


if __name__ == "__main__":
    unittest.main()
