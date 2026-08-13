# Docs

Faculty guidance for Classroom 50 and for adapting this template.

The [template README](../README.md) covers this repository specifically — its
layout, its CI, and what to change when you make it yours. These guides cover
the surrounding system.

| Guide | For | Time |
|---|---|---|
| **[Getting started](getting-started.md)** | Never set up an autograder. Zero to a verified, working assignment. | ~45 min first time |
| **[Writing tests](writing-tests.md)** | Expressing "is this correct?" as a `tests` block. Test types, weighting, traps. | ~15 min |
| **[Troubleshooting](troubleshooting.md)** | Something is broken. Symptom → diagnosis → fix. | as needed |
| **[Performance sanity check](../perf/README.md)** | Load testing a service-building assignment. Opt-in. | ~10 min |
| [Sample assignment](assignment.md) | The student-facing instructions shipped with this template. Replace with your own. | — |

## If you read nothing else

> [!CAUTION]
> An assignment with no grading configured reports **0/0, status success** —
> green on every submission, including an empty one. A passing run is therefore
> not evidence that grading works; it is also exactly what a completely
> unconfigured assignment produces.
>
> **Before handing any assignment to students, push a deliberately wrong
> submission and confirm it comes back red.**

## Upstream

Classroom 50 itself is documented at
[foundation50/classroom50](https://github.com/foundation50/classroom50/wiki) —
[Installation](https://github.com/foundation50/classroom50/wiki/Installation),
[CLI Teacher Guide](https://github.com/foundation50/classroom50/wiki/CLI-Teacher-Guide),
[Autograders](https://github.com/foundation50/classroom50/wiki/Autograders).
These guides cover the parts that wiki assumes you already know, plus the
CSULB-specific setup.

> [!NOTE]
> Org-specific internals — the grading workflows, roster, and collected scores —
> live in the private `Giacalone-CECS/classroom50` config repo. Nothing in these
> guides depends on access to it.
