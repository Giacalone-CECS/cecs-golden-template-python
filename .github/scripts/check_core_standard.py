#!/usr/bin/env python3
"""Core Standard conformance check.

RFP-1 asks for governance that "enables faculty to fork the framework for
course-specific needs without compromising the integrity of the Core Standard."
This script is the enforcing half of that: docs/governance.md says what the
Core Standard is, and this decides whether a repo still meets it.

Governance that nothing verifies is a statement of intent. The whole reason
this template exists is that an unverified claim of correctness reads exactly
like a verified one — see docs/troubleshooting.md. So the Core Standard gets a
red build when it is broken, not a paragraph asking people to be careful.

The rules below ARE the contract, written as data so a faculty member can read
what is required without reading Python. Keep them in sync with
docs/governance.md; that document is the human-readable half.

Deliberately language-agnostic. A course that forks this into Node or Java must
still pass, so the test-suite rule matches common conventions across languages
rather than assuming pytest.

Usage:
    python3 .github/scripts/check_core_standard.py
    python3 .github/scripts/check_core_standard.py --json

Exit 0 = conformant. Exit 1 = the Core Standard is broken.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

# --------------------------------------------------------------------------
# THE CORE STANDARD
#
# Every rule here is a thing a course repo MUST keep. Anything not listed is
# explicitly free to change — the exercise, the language, the number of tests,
# the point weighting, the thresholds, the prose. See docs/governance.md.
# --------------------------------------------------------------------------

TEST_FILE_PATTERNS = [
    "tests/**/test_*.py", "tests/**/*_test.py",        # Python
    "tests/**/*.test.js", "tests/**/*.spec.js",        # JavaScript
    "tests/**/*.test.ts", "tests/**/*.spec.ts",        # TypeScript
    "tests/**/*Test.java", "tests/**/Test*.java",      # Java
    "tests/**/*_test.go",                              # Go
    "tests/**/test_*.c", "tests/**/*_test.c",          # C
]

VERIFICATION_LOG_SECTIONS = [
    "Tools used",
    "How you verified it",
    "Attestation",
]


def rule_verification_log() -> tuple[bool, str]:
    """CS-1: the mandatory AI-assistance audit trail.

    The one item RFP-1 calls mandatory by name. A fork may reword it or add
    sections; it may not drop it, and it may not gut the sections that make it
    an audit trail rather than a checkbox.
    """
    path = "VERIFICATION-LOG.md"
    if not os.path.isfile(path):
        return False, f"{path} is missing (RFP-1 requires it)"
    text = open(path, encoding="utf-8", errors="replace").read()
    missing = [s for s in VERIFICATION_LOG_SECTIONS if s.lower() not in text.lower()]
    if missing:
        return False, f"{path} is missing required section(s): {', '.join(missing)}"
    return True, f"{path} present with all required sections"


def rule_test_suite() -> tuple[bool, str]:
    """CS-2: a real test suite.

    An empty suite reports success, which is the failure this template was
    built to fix. Existence of the directory is not enough — there must be
    something in it that a test runner would pick up.
    """
    if not os.path.isdir("tests"):
        return False, "tests/ directory is missing"
    found = []
    for pattern in TEST_FILE_PATTERNS:
        found.extend(glob.glob(pattern, recursive=True))
    if not found:
        return False, (
            "tests/ contains no recognizable test files. Add tests, or extend "
            "TEST_FILE_PATTERNS in this script for your language."
        )
    return True, f"tests/ contains {len(found)} test file(s)"


def rule_ci_workflow() -> tuple[bool, str]:
    """CS-3: automated validation on push.

    A course repo without CI gives students no feedback loop, which is the
    'Automated CI/CD Framework' deliverable evaporating one fork at a time.
    """
    workflows = glob.glob(".github/workflows/*.yml") + glob.glob(".github/workflows/*.yaml")
    if not workflows:
        return False, ".github/workflows/ has no workflow files"
    for wf in workflows:
        text = open(wf, encoding="utf-8", errors="replace").read()
        # Strip comment-only lines FIRST. A naive substring search matches the
        # commented-out `# push:` that perf.yml ships as an opt-in hint, which
        # would let a dispatch-only repo pass this rule — a false green on the
        # exact deliverable the rule exists to protect.
        live = "\n".join(
            ln for ln in text.splitlines() if not ln.lstrip().startswith("#")
        )
        if not re.search(r"^on\s*:", live, re.M):
            continue
        if re.search(r"^\s*(push|pull_request)\s*:", live, re.M):
            return True, f"CI workflow present ({os.path.basename(wf)} triggers on push/PR)"
    return False, (
        "no workflow triggers on push or pull_request "
        "(a workflow_dispatch-only repo gives students no feedback loop)"
    )


def rule_student_instructions() -> tuple[bool, str]:
    """CS-4: the student can find out what to do.

    'Pedagogical Artifacts' means nothing if the assignment ships with no
    instructions. Any markdown under docs/ satisfies this — we are checking
    that the affordance exists, not grading the prose.
    """
    if not os.path.isdir("docs"):
        return False, "docs/ directory is missing"
    docs = glob.glob("docs/**/*.md", recursive=True)
    if not docs:
        return False, "docs/ contains no markdown files"
    return True, f"docs/ contains {len(docs)} document(s)"


def rule_readme() -> tuple[bool, str]:
    """CS-5: a README that says something.

    The 200-byte floor exists because a one-line stub is how this repo's own
    config README started, and it was useless to every reader who found it.
    """
    if not os.path.isfile("README.md"):
        return False, "README.md is missing"
    size = os.path.getsize("README.md")
    if size < 200:
        return False, f"README.md is only {size} bytes — too thin to orient anyone"
    return True, f"README.md present ({size} bytes)"


RULES = [
    ("CS-1", "Verification Log", rule_verification_log),
    ("CS-2", "Test suite", rule_test_suite),
    ("CS-3", "CI workflow", rule_ci_workflow),
    ("CS-4", "Student instructions", rule_student_instructions),
    ("CS-5", "README", rule_readme),
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Check Core Standard conformance.")
    ap.add_argument("--json", action="store_true", help="emit machine-readable results")
    args = ap.parse_args()

    results = []
    for rule_id, name, fn in RULES:
        try:
            ok, detail = fn()
        except Exception as exc:  # a crashing rule must not read as a pass
            ok, detail = False, f"rule raised {type(exc).__name__}: {exc}"
        results.append({"id": rule_id, "name": name, "passed": ok, "detail": detail})

    conformant = all(r["passed"] for r in results)

    if args.json:
        print(json.dumps({"conformant": conformant, "rules": results}, indent=2))
    else:
        print("Core Standard conformance")
        print("=" * 60)
        for r in results:
            mark = "PASS" if r["passed"] else "FAIL"
            print(f"  [{mark}] {r['id']} {r['name']}: {r['detail']}")
        print("=" * 60)
        print("CONFORMANT" if conformant else "NOT CONFORMANT — see docs/governance.md")

    return 0 if conformant else 1


if __name__ == "__main__":
    sys.exit(main())
