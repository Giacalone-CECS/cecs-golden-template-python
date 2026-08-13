"""Unit tests for src/stats.py.

Run locally with:  python3 -m pytest -q

These are the same tests the autograder runs, deliberately. Students should be
able to reproduce their grade on their own machine before pushing.

================================================================================
FACULTY: this file IS the rubric
================================================================================

HOW POINTS ARE ASSIGNED
    The assignment's `tests` block in the classroom config repo gives the whole
    pytest suite a single point value (12 in the sample). The runner splits
    that total ACROSS CASES via pytest-json-report: 9 of 12 passing scores
    9/12 * 12. You do not assign points per test here — you control the
    weighting by choosing how many cases cover each concept.

    Practical consequence: three tests for `mean` and one for `mode` means
    `mean` is worth three times as much. Weight by counting, and count on
    purpose. The sample is deliberately even — 4 cases per function.

    If a test errors at COLLECTION time (a syntax error in this file, a bad
    import), pytest reports zero cases and the runner falls back to exit-code
    scoring: all-or-nothing. Keep this file importable.

ONE ASSERTION PER TEST, MOSTLY
    Each case is a separate line in the student's feedback. A test that asserts
    five things reports as one failure and hides the other four, so a student
    who fixed three of them sees no movement. Split them, and the score becomes
    a gradient instead of a cliff.

NO HIDDEN TESTS IN THIS SAMPLE — A DELIBERATE CHOICE
    Students can read exactly what they are graded on. That is defensible for
    an intro assignment: it teaches reading a spec, and it removes "the
    autograder is unfair" from the conversation entirely.

    If your course needs hidden tests, do NOT just add secret cases to this
    file — students receive this repo. Put them in a per-assignment
    autograder.py in the classroom config repo, which is never distributed.
    Be aware of the tradeoff: hidden tests move failures from "I can reproduce
    this locally" to "I have to guess," which generates office-hours traffic.
    Use them where the assessment genuinely requires it, not by default.

TEST THE ERROR CONTRACT, NOT JUST THE HAPPY PATH
    Every class below ends with an empty-input case. Those four cases are what
    stop a student from submitting a function that silently returns None on bad
    input and passing anyway. If your spec promises an exception, test that it
    is raised — otherwise the promise is decorative.

WHAT NOT TO DO HERE
    No network calls, no clock reads, no randomness without a fixed seed, no
    filesystem writes outside tmp_path. Grading runs in a fresh container per
    submission; a test that depends on any of those becomes a flaky grade, and
    a flaky grade is a grade appeal.
"""

import pytest

from src.stats import mean, median, mode


class TestMean:
    # FACULTY: the ordinary case first — a student who has done the work should
    # see green on line one. Failing them at an edge case before the happy path
    # even runs reads as hostile.
    def test_integers(self):
        assert mean([1, 2, 3, 4]) == 2.5

    def test_single_value(self):
        assert mean([7]) == 7

    def test_negatives(self):
        assert mean([-2, 2]) == 0

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            mean([])


class TestMedian:
    def test_odd_length(self):
        assert median([3, 1, 2]) == 2

    # FACULTY: this case is why the even-length rule is written into the
    # docstring. Without the spec line, this test is a gotcha.
    def test_even_length(self):
        assert median([4, 1, 3, 2]) == 2.5

    # FACULTY: unsorted input catches the common bug of indexing the middle of
    # `values` instead of sorting first. Worth a dedicated case — it is the
    # single most frequent wrong answer for this function.
    def test_unsorted_input(self):
        assert median([9, 1, 5]) == 5

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            median([])


class TestMode:
    def test_clear_winner(self):
        assert mode([1, 2, 2, 3]) == 2

    # FACULTY: the tie rule from the spec. See the note in src/stats.py about
    # pinning down behavior that would otherwise pass by accident.
    def test_tie_returns_first_seen(self):
        assert mode([5, 5, 7, 7]) == 5

    # FACULTY: non-numeric input confirms the student did not reach for a
    # numeric-only shortcut (sum/len, statistics.mode with a numeric
    # assumption). Cheap case, catches a real misconception.
    def test_strings(self):
        assert mode(["a", "b", "a"]) == "a"

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            mode([])
