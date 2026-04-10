"""Tests for inference output contract."""

import json

from inference import emit_task_result, make_task_result


def test_make_task_result_schema_and_bounds():
    result = make_task_result(
        task_id="easy_001",
        final_score=1.5,
        steps_taken=7,
        done=True,
        errors=[],
    )
    assert set(result.keys()) == {"task_id", "final_score", "steps_taken", "done", "errors"}
    assert result["task_id"] == "easy_001"
    assert result["steps_taken"] == 7
    assert result["done"] is True
    assert result["errors"] == []
    assert 0.0 < result["final_score"] < 1.0


def test_emit_task_result_is_json_line(capsys):
    result = make_task_result(
        task_id="easy_002",
        final_score=0.0,
        steps_taken=3,
        done=False,
        errors=["sample error"],
    )
    emit_task_result(result)
    line = capsys.readouterr().out.strip()
    payload = json.loads(line)
    assert payload["type"] == "task_result"
    assert payload["task_id"] == "easy_002"
    assert payload["errors"] == ["sample error"]
    assert 0.0 < payload["final_score"] < 1.0
