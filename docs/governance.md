# Governance protocol

How a course forks this template for its own needs **without** the departmental
standard dissolving one fork at a time.

RFP-1 asks for "a clear implementation strategy and documentation that enables
faculty to fork the framework for course-specific needs without compromising
the integrity of the Core Standard." This document is that contract. The
[`Core Standard` workflow](../.github/workflows/core-standard.yml) enforces it.

> [!IMPORTANT]
> **The standard is enforced, not requested.** A repository that breaks the
> Core Standard gets a red build. Governance that nothing verifies is a
> statement of intent — and this whole template exists because an unverified
> claim of correctness reads exactly like a verified one.

---

## The bargain

**Faculty autonomy over content. Departmental consistency of structure.**

You should never have to ask permission to teach your course your way. What you
teach, in what language, weighted how you like, is yours. What a *student*
encounters structurally — where the instructions live, that their work is
tested automatically, that AI assistance is disclosed — should be the same in
CECS 174 and CECS 478.

That is the entire trade. Everything below follows from it.

## The Core Standard — five rules

| ID | Rule | What it protects |
|---|---|---|
| **CS-1** | `VERIFICATION-LOG.md` exists, with its Tools / Verification / Attestation sections | The AI-assistance audit trail RFP-1 makes mandatory. Without it there is no consistent record of how students used AI. |
| **CS-2** | `tests/` contains real, discoverable test files | An empty suite reports success. This is the failure the template was built to fix. |
| **CS-3** | A workflow triggers on `push` or `pull_request` | The student feedback loop. A `workflow_dispatch`-only repo gives students nothing. |
| **CS-4** | `docs/` contains student-facing instructions | An assignment with no instructions is not an assignment. |
| **CS-5** | `README.md` exists and is more than a stub | Orientation. A one-line README helps nobody — this repo's config half started that way. |

Each rule checks that a load-bearing piece **exists**. None inspects your course
content, and none ever will.

## What you are free to change

Everything else. Explicitly:

- **The exercise.** Replace `src/` and `tests/` wholesale.
- **The language.** Python is the sample, not the standard. Node, Java, C, Go —
  the grading contract is "a command that exits non-zero on failure."
- **The number of tests and their weighting.** Case count is your rubric.
- **Performance thresholds**, or dropping the perf check entirely for
  assignments with no service.
- **Due dates, repo naming, branch policy, all prose.**
- **Adding** anything: linters, type checks, extra workflows, more docs.

> [!TIP]
> The Core Standard is a floor, not a ceiling. It has nothing to say about what
> you add — only about what you remove.

## Forking a course from the template

1. **Use this template** on
   [cecs-golden-template-python](https://github.com/Giacalone-CECS/cecs-golden-template-python).
2. Replace `src/`, `tests/`, and `docs/assignment.md` with your content.
3. Keep `VERIFICATION-LOG.md`. Reword it freely; don't delete it or gut its
   sections.
4. Push. **The Core Standard check runs automatically.** Green means your fork
   is still departmentally conformant.
5. Wire up grading — see [Getting started](getting-started.md).

Run it locally before pushing:

```sh
python3 .github/scripts/check_core_standard.py
python3 .github/scripts/check_core_standard.py --json   # machine-readable
```

## If a rule genuinely doesn't fit your course

Some course really will have a legitimate reason to break one of these. When
that happens:

> [!CAUTION]
> **Raise it with the curriculum committee. Do not delete the check.**
>
> A standard that any repo can silently opt out of is not a standard, it is a
> suggestion with extra steps. Deleting the workflow removes the signal without
> removing the divergence — which is precisely the failure mode catalogued in
> [troubleshooting](troubleshooting.md#everything-passes-including-work-that-should-fail).

The productive move is usually to **amend the standard for everyone** rather
than carve out an exception for one course. If a rule doesn't fit your course,
there is a decent chance it doesn't fit three others either.

Amending: propose the change, have it reviewed, then update **both**
`.github/scripts/check_core_standard.py` and this document in the same change.
They are two halves of one contract and must not drift.

## Sustaining it

RFP-1 provides for an annual **Tech Review** each May. That review is the right
moment to ask:

- Has a rule become busywork? Retire it. A rule nobody believes in teaches
  people to route around the check.
- Is something now load-bearing that isn't yet a rule?
- Do the CI actions, toolchain pins, and thresholds still reflect current
  practice?

Adoption path: **UGCC approval → Fall pilot with volunteer faculty → departmental
adoption for Spring 2027.** The pilot is where rules that sounded reasonable
meet courses that didn't fit them, and it should be treated as the real test of
this document rather than a formality.

> [!NOTE]
> **Where this lives is a committee question.** The template currently sits in
> an individual faculty member's teaching organization. That is fine for the
> MVP, but a departmental standard should end up in a departmental
> organization with more than one administrator — otherwise its continuity
> depends on one person's account. Worth settling before Spring 2027 adoption.

## What this protocol does *not* do

- **It does not review your course content.** Not the exercise, not the
  difficulty, not the grading scheme.
- **It does not prevent forking.** It makes divergence *visible*, which is the
  opposite of preventing it.
- **It does not run in student repositories as a grading input.** It checks
  repository structure; it has no effect on any score. (It will flag a student
  who deletes `VERIFICATION-LOG.md` — arguably a feature.)
