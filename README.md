# CECS Golden Template — Python Project with Test Cases

A starting point for a CECS course assignment: a small Python package under
`src/`, a matching `pytest` suite under `tests/`, CI that runs on every push,
and a Verification Log the student fills in.

Replace the sample `stats` exercise with your own content. **Keep the shape** —
the autograder and the CI both depend on it.

> Files in this repo carry `FACULTY:` comments explaining why each piece is the
> way it is. They are written for whoever adapts this next. Students can ignore
> them, and you can strip them once your own version settles.

## Layout

| Path | What goes here |
|---|---|
| `src/` | Starter code students complete. Importable as a package. |
| `tests/` | `pytest` suite. The autograder runs this same suite. |
| `docs/` | Assignment instructions for students. |
| `VERIFICATION-LOG.md` | Required. The student's record of AI assistance. |
| `.github/workflows/ci.yml` | Runs the suite on every push, so students see pass/fail without waiting on a grade. |

---

## For students

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest -q
```

Implement the functions in `src/`, run the tests locally until they pass, then
commit and push. CI runs the same suite. Fill in `VERIFICATION-LOG.md` before
your final push — it is part of the grade.

---

## For instructors

### The one failure mode that will bite you

**An assignment with no `tests` block grades everything as a pass.**

The runner resolves a grading entrypoint in this order:

```
per-assignment autograder.py
  → per-assignment tests.json   (materialized from your `tests` block)
    → classroom-default autograder.py
      → vacuous pass
```

That last step is not an error state — it is a deliberate "no autograder
configured yet" path that returns **0/0, status success**. It looks green in
every UI. An empty submission gets the same result as a correct one.

This is exactly how this template was found broken: it pointed at a repo with
no code and had no `tests` block, so every push came back green and nothing
anywhere said otherwise.

**Therefore, once per assignment, before students see it:** push one
deliberately wrong submission and confirm it comes back **red**. A green run
proves nothing — it is what a completely unconfigured assignment also produces.
Only a red run proves the grader is wired up.

### Two things must stay in sync

1. **`tests/` must contain real tests.** An empty suite reports success.
2. **The assignment's `tests` block must match this layout.** It lives in the
   classroom config repo's `assignments.json`, not here. For this template:

   ```json
   "tests": [
     { "name": "module imports", "type": "run",
       "run": "python3 -c \"import src.stats\"", "points": 1 },
     { "name": "pytest suite", "type": "python",
       "setup": "python3 -m pip install --quiet -r requirements.txt",
       "run": "python3 -m pytest -q tests/test_stats.py",
       "timeout": 120, "points": 12 }
   ]
   ```

   The import smoke test is worth its one point: when a student breaks the
   import, it names that directly instead of reporting twelve confusing
   downstream errors.

### Adapting this to your course

Work outward from the middle:

1. Rewrite `src/` with your exercise — stubs that **raise**, not `pass`.
2. Rewrite `tests/` to match. Case count is your weighting (see the notes in
   that file).
3. Rewrite `docs/assignment.md`.
4. Update the `run` paths in the `tests` block above if you rename anything.
5. Push a wrong submission. Confirm red.

Steps 1–4 are the visible work. Step 5 is the one that actually protects you,
and it is the one people skip.

### Scope note

Python is the sample, not a requirement. A Node version is the same structure
with `npm test` in place of `pytest` — the `tests` block takes any command. The
grading contract is "a command that exits non-zero on failure," not a language.
