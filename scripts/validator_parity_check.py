#!/usr/bin/env python3
"""Validator-parity checks for score bounds and output contract."""

from __future__ import annotations

import json
from pathlib import Path

from releaseops_env.models import ReleaseAction
from releaseops_env.scoring import is_strict_score
from server.releaseops_environment import ReleaseOpsEnvironment

TASKS_DIR = Path(__file__).resolve().parents[1] / "tasks"


def run_reference_episode(task_id: str) -> float:
    env = ReleaseOpsEnvironment()
    obs = env.reset(task_id=task_id)

    with open(TASKS_DIR / task_id / "ground_truth.json") as f:
        gt = json.load(f)

    evidence_actions = [
        ReleaseAction(action_type="inspect_change", section="diff"),
        ReleaseAction(action_type="inspect_change", section="tests"),
        ReleaseAction(action_type="inspect_change", section="approvals"),
        ReleaseAction(action_type="inspect_dependencies"),
        ReleaseAction(action_type="search_incidents", keywords=["retry", "timeout", "latency"]),
        ReleaseAction(action_type="check_policy"),
    ]

    for action in evidence_actions:
        obs = env.step(action)
        if obs.done:
            break

    if not obs.done:
        obs = env.step(
            ReleaseAction(
                action_type="submit_decision",
                final_decision=gt.get("optimal_decision", "block"),
                reason_codes=gt.get("required_reason_codes", []),
            )
        )

    score = obs.final_score
    if score is None or not is_strict_score(score):
        raise SystemExit(f"[FAIL] {task_id}: out-of-range final_score={score}")
    print(f"[OK] {task_id}: final_score={score:.3f}")
    return score


def main() -> None:
    task_ids = sorted(p.name for p in TASKS_DIR.iterdir() if p.is_dir())
    if not task_ids:
        raise SystemExit("[FAIL] No tasks found")

    scores = [run_reference_episode(task_id) for task_id in task_ids]
    avg = sum(scores) / len(scores)
    if not is_strict_score(avg):
        raise SystemExit(f"[FAIL] Average score out-of-range: {avg}")
    print(f"[OK] average_score={avg:.3f}")
    print("[OK] validator parity checks passed")


if __name__ == "__main__":
    main()
