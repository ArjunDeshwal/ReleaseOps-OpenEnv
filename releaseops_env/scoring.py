"""Shared score utilities for strict validator-compatible score handling."""

from __future__ import annotations

import math
from typing import Any

STRICT_SCORE_MIN = 0.001
STRICT_SCORE_MAX = 0.999


def normalize_score(value: Any) -> float:
    """Return a finite score guaranteed to satisfy 0 < score < 1."""
    try:
        score = float(value)
    except (TypeError, ValueError):
        return STRICT_SCORE_MIN

    if math.isnan(score):
        return STRICT_SCORE_MIN
    if score == math.inf:
        return STRICT_SCORE_MAX
    if score == -math.inf:
        return STRICT_SCORE_MIN

    return max(STRICT_SCORE_MIN, min(STRICT_SCORE_MAX, score))


def format_score(value: Any, decimals: int = 3) -> str:
    """Format a score after strict normalization."""
    return f"{normalize_score(value):.{decimals}f}"


def is_strict_score(value: Any) -> bool:
    """Return True only when value is finite and strictly between 0 and 1."""
    try:
        score = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(score) and 0.0 < score < 1.0
