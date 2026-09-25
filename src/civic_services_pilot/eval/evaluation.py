# src/civic_services_pilot/eval/evaluation.py
import json
from pathlib import Path
from civic_services_pilot.tracing import setup_tracing
from civic_services_pilot.client import call_model_json
from civic_services_pilot.prompts.loader import load_prompt
from civic_services_pilot.eval.contracts.contract import (
    validate,
)

PROMPT_NAME = "municipal_assistant"
PROMPT_VERSION = "v0"
TEST_SET = "civic_services_v0"


def load_test_cases(name: str) -> list[dict]:
    """Load test cases from the src/civic_services_pilot/eval/cases/
    directory."""
    path = (
        Path(__file__).parent
        / "cases"
        / f"{name}.json"
    )
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def civic_services_prompt(text: str) -> str:
    """Run the civic services prompt.
    Returns the raw JSON string."""
    instructions = load_prompt(PROMPT_NAME, PROMPT_VERSION)
    return call_model_json(
        instructions=instructions,
        user_input=text,
    )


def run_eval() -> None:
    setup_tracing()
    """Run contract validation then semantic
    checks on every test case."""
    cases = load_test_cases(TEST_SET)
    contract_pass = 0
    semantic_pass = 0
    total = len(cases)

    print(
        f"Eval: prompt={PROMPT_NAME} "
        f"test_set={TEST_SET} cases={total}"
    )
    print("-" * 50)

    for case in cases:
        raw = civic_services_prompt(case["input"])
        result = validate(raw)

        if not result["valid"]:
            print(
                f"  {case['id']}: CONTRACT FAIL "
                f"({result['violations']})"
            )
            continue

        contract_pass += 1
        #json del risultato
        parsed = json.loads(raw.strip())
        urgency_ok = (
            parsed["urgency_level"]
            == case["expected_urgency_level"]
        )

        if urgency_ok:
            semantic_pass += 1
        status = (
            "PASS" if urgency_ok
            else "SEMANTIC FAIL"
        )

        detail = ""
        if not urgency_ok:
            detail += f"{parsed['urgency_level']}"
        if detail:
            detail = f" ({detail.strip()})"
        print(f"  {case['id']}: {status}{detail}")

    print("-" * 50)
    print(
        f"Contract: {contract_pass}/{total} | "
        f"Semantic: {semantic_pass}/{total}"
    )


if __name__ == "__main__":
    run_eval()