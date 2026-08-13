# Writing tests

How to express "is this submission correct?" as a declarative `tests` block.

Assumes you've been through [Getting started](getting-started.md).

---

## The three test types

Every test is one of three shapes. Pick by *what you are checking*, not by what
language the assignment is in.

| Type | Checks | Reach for it when |
|---|---|---|
| `run` | A command's **exit code** | Does it compile? Does it import? Does it exit 0? |
| `io` | A command's **stdout** against expected text | Program reads input, prints output |
| `python` | A **pytest suite**, points split per case | You have real unit tests |

### `run` — does the command succeed?

The simplest and most underrated. Exit code 0 passes.

```sh
gh teacher assignment test add <org> <classroom> <slug> \
    --name "compiles" --type run \
    --run "gcc -o hello hello.c" --points 1
```

Require a *specific* exit code with `--exit-code`:

```sh
    --name "exits 42" --type run \
    --run "./prog --selftest" --exit-code 42 --points 1
```

**Lead with a cheap `run` test**: "it compiles," "it imports." When a student
breaks the build, that test names the actual problem instead of letting twelve
downstream tests fail with noise.

### `io` — does it print the right thing?

For programs that read stdin and print stdout.

```sh
gh teacher assignment test add <org> <classroom> <slug> \
    --name "greets Alice" --type io \
    --run "python3 greet.py" \
    --input "Alice" \
    --expected "hello, Alice!" \
    --comparison included --points 2
```

`--comparison` is **required** for `io` and is the whole game:

| Comparison | Passes when | Use for |
|---|---|---|
| `included` | Expected appears **somewhere** in stdout | **Start here.** Tolerates prompts and extra newlines. |
| `exact` | Output matches **exactly** | Output format is itself being assessed |
| `regex` | Expected (a regex) matches stdout | Flexible whitespace, varying numbers |

> [!TIP]
> **Choose `included` unless you mean to grade formatting.** `exact` fails a
> correct program that printed `Enter a name: ` first, and students cannot tell
> a logic error from a trailing-space error. If you *are* grading output format,
> say so in the assignment text. Otherwise it reads as a gotcha.

For long fixtures, use files bundled next to the tests instead of inline
strings: `--input-file names.txt --expected-file expected.txt`.

### `python` — run a pytest suite

```sh
gh teacher assignment test add <org> <classroom> <slug> \
    --name "pytest suite" --type python \
    --setup "python3 -m pip install --quiet -r requirements.txt" \
    --run "python3 -m pytest -q tests/test_stats.py" \
    --timeout 120 --points 12
```

The runner installs `pytest` and `pytest-json-report` if missing, then **splits
the points across the reported cases**. 9 of 12 passing scores 9.

---

## Weighting is by case count

This surprises people, so state it plainly:

> [!IMPORTANT]
> A `python` test carries **one** point value for the **whole suite**. The
> runner divides it across however many cases pytest reports.

So four tests on `mean` and one on `mode` makes `mean` worth **four times** as
much, not because you weighted it but because you wrote more tests. Count
deliberately.

**Corollary: split your assertions.** Each case is one line of feedback. A test
asserting five things reports as one failure and hides the other four, so a
student who fixed three sees no movement. Split them and the score becomes a
gradient instead of a cliff.

---

## Fields at a glance

| Flag | Applies to | Notes |
|---|---|---|
| `--name` | all | Unique within the assignment. Shown to students, so write it as feedback: "handles empty input", not "test 3". |
| `--type` | all | `run` \| `io` \| `python` |
| `--run` | all | The command |
| `--setup` | all | Runs first: compile, install deps. A failure here fails the test. |
| `--points` | all | Defaults to 0 = informational, runs but doesn't score |
| `--timeout` | all | Seconds, 1–600. Default 10. Raise for anything installing packages. |
| `--exit-code` | `run` | Required exit code |
| `--input` / `--input-file` | `io` | stdin, inline or fixture |
| `--expected` / `--expected-file` | `io` | Expected stdout |
| `--comparison` | `io` | **Required.** `included` \| `exact` \| `regex` |

Managing them:

```sh
gh teacher assignment test list <org> <classroom> <slug>          # names
gh teacher assignment test list <org> <classroom> <slug> --json   # full specs
gh teacher assignment test remove <org> <classroom> <slug> <name>
```

### Setting the whole block at once

Adding tests one at a time is fine for two or three. For a suite you keep under
version control, `--tests` takes a JSON file (or `-` for stdin) holding a bare
array of specs and sets the block in one shot:

```sh
gh teacher assignment add <org> <classroom> <slug> --name "..." --tests tests.json
gh teacher assignment test list <org> <classroom> <slug> --json > tests.json   # round-trips
```

Handy when you want the test definitions reviewed in a pull request rather than
typed at a terminal. Mutually exclusive with a per-assignment `autograder.py`.

---

## A worked set

The suite behind this template. A cheap import guard plus the real suite:

```sh
gh teacher assignment test add Giacalone-CECS cecs-378-fa26 lab-01-stats \
    --name "module imports" --type run \
    --run 'python3 -c "import src.stats"' --points 1

gh teacher assignment test add Giacalone-CECS cecs-378-fa26 lab-01-stats \
    --name "pytest suite" --type python \
    --setup "python3 -m pip install --quiet -r requirements.txt" \
    --run "python3 -m pytest -q tests/test_stats.py" \
    --timeout 120 --points 12
```

13 points. A student who breaks the import loses 1 and is told exactly that; a
student whose logic is wrong loses proportionally across the 12.

---

## Traps

**A broken import scores all-or-nothing.** If pytest can't collect, it reports
zero cases and the runner falls back to exit-code scoring. The whole 12 points
vanish together. The 1-point import test is what turns this from a mystery into
a labeled failure.

**Points default to 0.** Omit `--points` and the test runs, reports, and scores
nothing. Occasionally what you want; usually not.

**The default timeout is 10 seconds.** Anything doing `pip install` needs more.
A timeout reads to students as a wrong answer.

**Tests run in a fresh container per submission.** No network guarantees beyond
package installs, no persistence between tests, no clock or randomness without a
fixed seed. A flaky test is a grade appeal.

> [!CAUTION]
> **Never put secrets in a test command.** These run inside the student's repo,
> and a student can print anything the job can read.

---

## When declarative tests aren't enough

Reach for a hand-written autograder when you need partial credit inside a single
test, to inspect files rather than run them, or to hide the tests entirely.

Drop an `autograder.py` at `<classroom>/autograders/<slug>/` in your
organization's `classroom50` config repo. It takes precedence over the `tests`
block for that assignment. A classroom-wide default goes in via
`gh teacher autograder set-default`.

See the [Autograders wiki](https://github.com/foundation50/classroom50/wiki/Autograders).

**Hidden tests, specifically:** don't add secret cases to the suite in the
template, because students receive that repo. Put them in `autograder.py` in the
config repo, which is never distributed. Weigh the cost: hidden tests move
failures from "I can reproduce this locally" to "I have to guess," which is a
real teaching decision, not just a technical one.

---

## Before you hand it to students

> [!CAUTION]
> Whatever you wrote, **push a deliberately wrong submission and confirm it
> comes back red.** A green run is exactly what an assignment with no tests at
> all produces.
> See [Getting started, step 7](getting-started.md#step-7--prove-it-actually-grades).
