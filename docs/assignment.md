# Sample Assignment — Descriptive Statistics

*Instructors: replace this file with your own assignment instructions.*

## What to do

Implement three functions in `src/stats.py`. Each one currently raises
`NotImplementedError`; replace the body with a working implementation.

| Function | Returns | Edge case |
|---|---|---|
| `mean(values)` | arithmetic mean | `ValueError` on empty input |
| `median(values)` | middle value; mean of the middle two when even-length | `ValueError` on empty input |
| `mode(values)` | most frequent value | on a tie, the one appearing first in `values`; `ValueError` on empty input |

Do not change the function names or signatures — the tests import them
directly.

## How you are graded

The autograder runs `tests/test_stats.py`, the same suite you can run
yourself:

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest -q
```

There are no hidden tests in this sample. What you see is what is scored.

## Before you push

Fill in `VERIFICATION-LOG.md`. If you used an AI tool at any point, say so and
say how you checked its output. If you did not, say that instead — an empty
log is not the same as "I did not use one."
