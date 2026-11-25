#!/usr/bin/env python3
"""Generate the safe, deterministic repository-context block in AGENTS.md."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

BEGIN_MARKER = "<!-- BEGIN GENERATED PROJECT CONTEXT -->"
END_MARKER = "<!-- END GENERATED PROJECT CONTEXT -->"

SOURCE_DOCS = (
    "docs/ARCHITECTURE.md",
    "docs/FILE_DATABASE.md",
    "docs/OPERATING_MODEL.md",
    "docs/PRODUCT_ROADMAP.md",
    "docs/RELEASE_RUNBOOK.md",
)

INVENTORY_DIRS = (
    ".github/ISSUE_TEMPLATE",
    ".github/scripts",
    ".github/workflows",
    "assets",
    "content",
    "data/config",
    "data/records",
    "data/schema",
    "docs",
    "docs/diagrams",
    "apps/admin",
    "apps/api",
    "scripts",
    "tests",
)

HEADING_PATTERN = re.compile(r"^#{1,2}\s+(.+?)\s*$")


def extract_headings(root: Path, relative_path: str) -> list[str]:
    """Read only Markdown heading lines from an approved documentation file."""
    path = root / relative_path
    if not path.is_file():
        raise SystemExit(f"Required context source is missing: {relative_path}")

    headings: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_PATTERN.match(line)
        if match:
            headings.append(match.group(1).strip())

    if not headings:
        raise SystemExit(f"Required context source has no Markdown headings: {relative_path}")
    return headings


def build_generated_block(root: Path) -> str:
    lines = [
        BEGIN_MARKER,
        "## Generated project context",
        "",
        "Generated from approved local documentation and a fixed directory allowlist. "
        "Re-run the generator after changing these sources.",
        "",
        "### Approved local references",
        "",
    ]

    for relative_path in SOURCE_DOCS:
        headings = extract_headings(root, relative_path)
        lines.append(f"- {relative_path}: {'; '.join(headings)}")

    lines.extend(["", "### Repository directory inventory", ""])
    existing_dirs = sorted(
        relative_path
        for relative_path in INVENTORY_DIRS
        if (root / relative_path).is_dir()
    )
    lines.extend(f"- {relative_path}/" for relative_path in existing_dirs)

    lines.extend(
        [
            "",
            "### Privacy guardrails",
            "",
            "- Only headings from approved Markdown documents are emitted; document body text is not copied.",
            "- The directory inventory uses a fixed allowlist and records directory names only; it never enumerates files.",
            "- The generator never reads JSON/YAML records, environment files, credentials, secrets or private runtime/customer data.",
            "- GitHub Issues/PRs and Render service/deploy state are live external sources; inspect them during each run instead of freezing volatile status here.",
            END_MARKER,
        ]
    )
    return "\n".join(lines)


def replace_generated_block(document: str, generated: str) -> str:
    if document.count(BEGIN_MARKER) != 1 or document.count(END_MARKER) != 1:
        raise SystemExit("AGENTS.md must contain exactly one pair of generated-context markers.")

    start = document.index(BEGIN_MARKER)
    end_marker_start = document.index(END_MARKER)
    end = end_marker_start + len(END_MARKER)
    if start >= end_marker_start:
        raise SystemExit("Generated-context markers are out of order.")

    return document[:start] + generated + document[end:]


def sync(root: Path, check: bool = False) -> bool:
    agents_path = root / "AGENTS.md"
    if not agents_path.is_file():
        raise SystemExit("AGENTS.md is missing.")

    current = agents_path.read_text(encoding="utf-8")
    generated = build_generated_block(root)
    updated = replace_generated_block(current, generated)

    if check:
        if updated != current:
            raise SystemExit("Generated AGENTS.md context is stale; run python3 scripts/sync_agent_context.py.")
        return False

    if updated != current:
        agents_path.write_text(updated, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail without writing when the generated AGENTS.md block is stale",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    changed = sync(root, check=args.check)

    if args.check:
        print("Generated AGENTS.md context is current.")
    elif changed:
        print("Updated the generated AGENTS.md context.")
    else:
        print("Generated AGENTS.md context is already current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
