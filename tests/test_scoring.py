"""Tests for shared strict score utilities."""

from releaseops_env.scoring import format_score, is_strict_score, normalize_score


def test_normalize_score_clamps_boundaries():
    assert normalize_score(0.0) == 0.001
    assert normalize_score(1.0) == 0.999
    assert normalize_score(-5.0) == 0.001
    assert normalize_score(5.0) == 0.999


def test_normalize_score_handles_non_finite_values():
    assert normalize_score(float("nan")) == 0.001
    assert normalize_score(float("-inf")) == 0.001
    assert normalize_score(float("inf")) == 0.999


def test_is_strict_score():
    assert is_strict_score(0.001) is True
    assert is_strict_score(0.999) is True
    assert is_strict_score(0.0) is False
    assert is_strict_score(1.0) is False


def test_format_score_uses_normalized_value():
    assert format_score(1.0) == "0.999"
    assert format_score(0.0) == "0.001"
