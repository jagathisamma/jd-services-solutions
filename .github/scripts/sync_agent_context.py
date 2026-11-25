#!/usr/bin/env python3
"""Generate the managed project-context section in AGENTS.md deterministically."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BEGIN_MARKER = "<!-- BEGIN GENERATED JD PROJECT CONTEXT -->"
END_MARKER = "<!-- END GENERATED JD PROJECT CONTEXT -->"

REQUIRED_FILES = (
    "README.md",
    "docs/ARCHITECTURE.md",
    "docs/FILE_DATABASE.md",
    "docs/OPERATING_MODEL.md",
    "docs/PRODUCT_ROADMAP.md",
    "docs/RELEASE_RUNBOOK.md",
    "data/config/site.yml",
    "data/config/brand.yml",
)
INVENTORY_ROOTS = (
    ".github/scripts",
    ".github/workflows",
    "assets",
    "content",
    "data/config",
    "data/schema",
    "docs",
    "scripts",
    "tests",
)
EXCLUDED_DIRECTORY_NAMES = {
    ".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build",
    "runtime", "private", "uploads", "backups", "secrets", "credentials",
    "records",
}
SENSITIVE_NAME = re.compile(
    r"(^\.env(?:$|\.)|secret|credential|customer|technician|payment|invoice|"
    r"private|runtime|upload|backup|token|key)",
    re.IGNORECASE,
)
ISSUE_ROW = re.compile(r"^\|\s*(#\d+)\s*\|\s*([^|]+?)\s*\|")


class ContextError(ValueError):
    """Raised when an approved source is missing or malformed."""


def read_required_files(root: Path) -> dict[str, str]:
    contents: dict[str, str] = {}
    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            raise ContextError(f"required source is missing: {relative}")
        try:
            contents[relative] = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise ContextError(f"cannot read required source {relative}: {exc}") from exc
    return contents


def extract_project_title(readme: str) -> str:
    for line in readme.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            if title:
                return title
            break
    raise ContextError("README.md must begin with a non-empty H1 project title")


def extract_headings(markdown: str, relative: str) -> list[str]:
    headings = [
        line[3:].strip()
        for line in markdown.splitlines()
        if line.startswith("## ") and line[3:].strip()
    ]
    if not headings:
        raise ContextError(f"{relative} has no level-two headings")
    return headings


def validate_deployment_contract(readme: str) -> None:
    match = re.search(
        r"(?ms)^## Deployment\s*\n(.*?)(?=^## |\Z)",
        readme,
    )
    if not match:
        raise ContextError("README.md is missing its ## Deployment section")
    deployment = match.group(1).lower()
    required_terms = ("render static site", "main", "auto-deploy")
    missing = [term for term in required_terms if term not in deployment]
    if missing:
        raise ContextError(
            "README.md deployment section is missing: " + ", ".join(missing)
        )


def validate_business_and_safety(contents: dict[str, str]) -> None:
    required_site_facts = (
        'name: "JD Services & Solutions"',
        'city: "Erode"',
        'state: "Tamil Nadu"',
        'phoneDisplay: "8940454260"',
        'phoneE164: "+918940454260"',
        'tagline: "Service Today... Smile Tomorrow..."',
        'hosting: "render-static-site"',
        'sourceBranch: "main"',
        'customerDataStorage: "not-configured"',
    )
    site = contents["data/config/site.yml"]
    for fact in required_site_facts:
        if fact not in site:
            raise ContextError(f"data/config/site.yml is missing canonical setting: {fact}")

    required_brand_rules = (
        "Use the official logo asset unchanged; do not redraw or crop it.",
        "Never invent prices, warranties, certifications, ratings or testimonials.",
    )
    brand = contents["data/config/brand.yml"]
    for rule in required_brand_rules:
        if rule not in brand:
            raise ContextError(f"data/config/brand.yml is missing safety rule: {rule}")

    architecture = contents["docs/ARCHITECTURE.md"]
    for rule in (
        "not a safe CRM database",
        "Do not store customer or technician personal data",
    ):
        if rule not in architecture:
            raise ContextError(f"docs/ARCHITECTURE.md is missing privacy rule: {rule}")

    operating_model = contents["docs/OPERATING_MODEL.md"]
    for rule in (
        "This repository is public.",
        "private, access-controlled and backed-up store",
    ):
        if rule not in operating_model:
            raise ContextError(f"docs/OPERATING_MODEL.md is missing safety rule: {rule}")


def extract_roadmap_entries(roadmap: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    seen: set[str] = set()
    for line in roadmap.splitlines():
        match = ISSUE_ROW.match(line)
        if not match:
            continue
        issue, capability = match.group(1), match.group(2).strip()
        if not capability:
            raise ContextError(f"roadmap row {issue} has an empty capability")
        if issue in seen:
            raise ContextError(f"roadmap contains duplicate issue row {issue}")
        seen.add(issue)
        entries.append((issue, capability))
    if not entries:
        raise ContextError(
            "docs/PRODUCT_ROADMAP.md has no rows matching '| #issue | capability |'"
        )
    return sorted(entries, key=lambda item: int(item[0][1:]))


def is_excluded_directory(name: str) -> bool:
    return name.lower() in EXCLUDED_DIRECTORY_NAMES or bool(SENSITIVE_NAME.search(name))


def directory_inventory(root: Path) -> list[str]:
    """List approved directory paths only; never read or list record file contents."""
    discovered: set[str] = set()
    for relative_root in INVENTORY_ROOTS:
        base = root / relative_root
        if not base.is_dir():
            continue
        discovered.add(relative_root)
        for current, directories, _files in os.walk(base, followlinks=False):
            directories[:] = sorted(
                name
                for name in directories
                if not is_excluded_directory(name)
                and not (Path(current) / name).is_symlink()
            )
            current_path = Path(current)
            for name in directories:
                candidate = current_path / name
                discovered.add(candidate.relative_to(root).as_posix())
    return sorted(discovered)


def script_inventory(root: Path) -> list[str]:
    """List approved script paths only; never inspect script contents."""
    discovered: set[str] = set()
    allowed_suffixes = {".py", ".sh", ".js", ".mjs", ".ts", ".tsx"}
    for relative_root in (".github/scripts", "scripts"):
        base = root / relative_root
        if not base.is_dir():
            continue
        for current, directories, files in os.walk(base, followlinks=False):
            directories[:] = sorted(
                name
                for name in directories
                if not is_excluded_directory(name)
                and not (Path(current) / name).is_symlink()
            )
            for name in files:
                candidate = Path(current) / name
                if candidate.suffix.lower() not in allowed_suffixes:
                    continue
                if SENSITIVE_NAME.search(name):
                    continue
                if candidate.is_symlink():
                    continue
                discovered.add(candidate.relative_to(root).as_posix())
    return sorted(discovered)


def render_context(root: Path) -> str:
    contents = read_required_files(root)
    project_title = extract_project_title(contents["README.md"])
    validate_deployment_contract(contents["README.md"])
    validate_business_and_safety(contents)
    architecture_headings = extract_headings(
        contents["docs/ARCHITECTURE.md"], "docs/ARCHITECTURE.md"
    )
    storage_headings = extract_headings(
        contents["docs/FILE_DATABASE.md"], "docs/FILE_DATABASE.md"
    )
    extract_headings(contents["docs/OPERATING_MODEL.md"], "docs/OPERATING_MODEL.md")
    extract_headings(contents["docs/RELEASE_RUNBOOK.md"], "docs/RELEASE_RUNBOOK.md")
    roadmap_entries = extract_roadmap_entries(contents["docs/PRODUCT_ROADMAP.md"])
    inventory = directory_inventory(root)
    scripts = script_inventory(root)

    lines = [
        BEGIN_MARKER,
        "## Generated project context",
        "",
        f"- Project: **{project_title}**.",
        "- Canonical public business facts (validated against data/config/site.yml): JD Services & Solutions; Erode, Tamil Nadu; Call & WhatsApp 8940454260; “Service Today... Smile Tomorrow...”.",
        "- Safety guardrails (validated against brand.yml and architecture docs): do not invent prices, warranties, certifications, ratings or testimonials; keep customer and technician data out of this public repository; use the official logo unchanged.",
        "- Production boundary: the public site is a Render Static Site tracking `main` with commit auto-deploy; verify live deployment state from Render before reporting a release.",
        "- Public/private boundary: this repository contains public site, catalogue, configuration and documentation only. Customer, technician, repair, payment and credential records require separate private, access-controlled persistence.",
        "- Canonical operating and release rules: `docs/OPERATING_MODEL.md`, `docs/RELEASE_RUNBOOK.md` and this file's human-authored policy sections.",
        "- Architecture topics: "
        + "; ".join(architecture_headings)
        + ".",
        "- Flat-file contract topics: "
        + "; ".join(storage_headings)
        + ".",
        "- Project inventory (approved directory paths only):",
    ]
    lines.extend(f"  - `{path}/`" for path in inventory)
    lines.append("- Repository scripts (approved code file names only):")
    lines.extend(f"  - `{path}`" for path in scripts)
    lines.append(
        "- Issue roadmap index (capability names only; always re-query GitHub for live issue/PR state):"
    )
    lines.extend(
        f"  - {issue} — {capability}"
        for issue, capability in roadmap_entries
    )
    lines.extend(
        [
            "- Agent-context maintenance:",
            "  - Sync: `python3 .github/scripts/sync_agent_context.py --sync`",
            "  - Verify: `python3 .github/scripts/sync_agent_context.py --check`",
            "  - Tests: `python3 -m unittest discover -s tests -v`",
            "- Privacy guarantee: generated content derives only from the eight approved documentation/configuration files above; AGENTS.md is read only to preserve human-authored text. Inventory lists allowlisted directory and script names only, never file contents, environment variables, customer records, uploads, backups or secrets.",
            END_MARKER,
        ]
    )
    return "\n".join(lines)


def replace_generated_block(document: str, generated: str) -> str:
    begin_count = document.count(BEGIN_MARKER)
    end_count = document.count(END_MARKER)
    if begin_count != end_count or begin_count > 1:
        raise ContextError("AGENTS.md must contain exactly one balanced generated-block marker pair")
    if begin_count == 0:
        return document.rstrip() + "\n\n" + generated + "\n"
    start = document.index(BEGIN_MARKER)
    end = document.index(END_MARKER)
    if end < start:
        raise ContextError("AGENTS.md generated-block markers are out of order")
    end += len(END_MARKER)
    return document[:start] + generated + document[end:]


def run(mode: str, root: Path = ROOT) -> int:
    try:
        generated = render_context(root)
        agents_path = root / "AGENTS.md"
        if not agents_path.is_file():
            raise ContextError("required source is missing: AGENTS.md")
        current = agents_path.read_text(encoding="utf-8")
        updated = replace_generated_block(current, generated)
        if mode == "sync":
            if updated != current:
                agents_path.write_text(updated, encoding="utf-8")
                print("AGENTS.md generated project context synchronized.")
            else:
                print("AGENTS.md generated project context is already current.")
            return 0
        if updated != current:
            print(
                "AGENTS.md generated project context is stale; run "
                "`python3 .github/scripts/sync_agent_context.py --sync`.",
                file=sys.stderr,
            )
            return 1
        print("AGENTS.md generated project context is current.")
        return 0
    except (ContextError, OSError, UnicodeError) as exc:
        print(f"AGENT CONTEXT CHECK FAILED: {exc}", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--sync", action="store_true", help="update the managed AGENTS.md block")
    group.add_argument("--check", action="store_true", help="fail if the managed block is stale")
    args = parser.parse_args(argv)
    return run("sync" if args.sync else "check", root)


if __name__ == "__main__":
    raise SystemExit(main())
