"""Starter module for the golden-template sample assignment.

Students implement the three functions below. The signatures, docstrings, and
error contracts are given; the bodies are not.

================================================================================
FACULTY: what to change, and what not to
================================================================================

CHANGE FREELY
    The exercise itself. Descriptive statistics is a placeholder chosen because
    every discipline recognizes it. Swap in your own course content.

KEEP
    1. A module under `src/` that imports cleanly even when unimplemented.
       The autograder's first check is `import src.stats`. If a student can
       break the import, every downstream test errors instead of failing, and
       the feedback they get is a stack trace rather than a score.

    2. Stub bodies that RAISE, rather than `pass` or `return None`.
       This is the single most important line in this file. A `pass` stub
       returns None, and `assert mean([1,2]) == 1.5` fails with
       "None != 1.5" — indistinguishable from a wrong implementation. The
       explicit NotImplementedError makes "hasn't started" and "got it wrong"
       two different signals in the gradebook.

    3. Docstrings that state the EDGE CASE, not just the happy path. The empty
       input contract below is testable precisely because it is written down.
       Students are graded on it, so it has to be specified, not implied.

WHY THE FUNCTIONS ARE SMALL AND PURE
    Each takes a sequence and returns a value: no I/O, no globals, no clock, no
    network. That is what makes them gradeable by a declarative `tests` block
    instead of a hand-written autograder.py. The moment an assignment needs
    stdin parsing or file fixtures, you have moved from the `python` test type
    into `io` tests — doable, but more to maintain. Prefer pure functions when
    the pedagogy allows it.

A NOTE ON TIE-BREAKING (see `mode` below)
    "On a tie, return the value that appears first" is deliberate. The obvious
    implementation, `Counter(values).most_common(1)`, happens to satisfy this
    on CPython 3.7+ by insertion order, but that is an implementation detail
    students should not be leaning on. Specifying the tie rule turns an
    accidental pass into a deliberate one. When you write your own exercise,
    look for the place where the naive answer is right by luck, and pin it
    down in the spec.
"""


def mean(values):
    """Return the arithmetic mean of a non-empty sequence of numbers.

    Raises ValueError when `values` is empty.
    """
    # FACULTY: raise, don't `pass` — see the module docstring. An unimplemented
    # stub must be distinguishable from a wrong answer in the score report.
    raise NotImplementedError("implement mean()")


def median(values):
    """Return the median of a non-empty sequence of numbers.

    For an even-length sequence, return the mean of the two middle values.
    Raises ValueError when `values` is empty.
    """
    # FACULTY: the even-length rule is stated because it is genuinely ambiguous
    # — "the middle" has no single meaning for an even count, and students will
    # otherwise pick one and be marked wrong for a spec gap that is ours.
    raise NotImplementedError("implement median()")


def mode(values):
    """Return the most frequent value in a non-empty sequence.

    On a tie, return the value that appears first in `values`.
    Raises ValueError when `values` is empty.
    """
    raise NotImplementedError("implement mode()")
