# tests/test_smoke.py
import json
from pathlib import Path

import pytest
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)
from civic_services_pilot.staff_assistant import *

SMOKE_INPUTS: list[str] = json.loads(
    (Path(__file__).parent / "smoke_inputs.json").read_text()
)


@pytest.mark.parametrize("message", SMOKE_INPUTS)
def test_assistant_returns_not_empty(message: str) -> None:
    """The function returns a non-empty string."""
    result = staff_assistant_reply(
        message=message,
        ticket_id="3",
        role="staff",
    )

    assert result != "", (
        f"Empty output for input: {message!r}"
    )
    


def test_assistant_emits_a_span(
    span_exporter: InMemorySpanExporter,
) -> None:
    span_exporter.clear()

    staff_assistant_reply(
        message=SMOKE_INPUTS[0],
        ticket_id="3",
        role="staff",
    )

    spans = span_exporter.get_finished_spans()

    assert len(spans) > 0, (
        "No spans exported after staff_assistant_reply call"
    )

    span_names = [s.name for s in spans]

    assert "staff_assistant_reply" in span_names, (
        f"Expected 'staff_assistant_reply' span. "
        f"Spans found: {span_names}"
    )