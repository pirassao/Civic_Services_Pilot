# src/civic_services_pilot/contracts/contract.py
"""Output contract validator for the
classify-and-summarise prompt."""
#from phoenix.experiments.evaluators import create_evaluator
import json


# --- Contract constants ---

MAX_SUMMARY_WORDS = 50
REQUIRED_OUTSIDE_KEYS = {
    "answer", "fields", "urgency_level", "urgency_rationale"
}
REQUIRED_INSIDE_KEYS={
    "person_name", "reference_number", "amount", "date"
}
EMERGENCY_LEVELS = {"routine", "urgent", "emergency"}


#@create_evaluator(name="contract_valid", kind="CODE")
def validate(raw_response: str) -> dict:
    """Validate a raw model response against the
    output contract. Returns a dict with a 'valid'
    boolean and a list of 'violations'."""
    violations: list[str] = []

    # 1. Must be parseable JSON.
    stripped = raw_response.strip()
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        return {
            "valid": False,
            "violations": [
                "Response is not valid JSON"
            ],
        }

    # 2. Must be a dict (not a list or scalar).
    if not isinstance(parsed, dict):
        return {
            "valid": False,
            "violations": [
                "Response is not a JSON object"
            ],
        }

    # 3. Must contain exactly the required keys.
    actual_keys = set(parsed.keys())
    if actual_keys != REQUIRED_OUTSIDE_KEYS:
        missing = REQUIRED_OUTSIDE_KEYS - actual_keys
        extra = actual_keys - REQUIRED_OUTSIDE_KEYS
        if missing:
            violations.append(
                f"Missing keys: {missing}"
            )
        if extra:
            violations.append(
                f"Extra keys: {extra}"
            )

    # 4. "fields" must be a JSON object containing
    # exactly the required inner keys.
    fields = parsed.get("fields")

    #is a dict?
    if not isinstance(fields, dict):
        violations.append(
        "'fields' is not a JSON object"
    )
    else:
        actual_inside_keys = set(fields.keys())

    #forgotten keys
    if actual_inside_keys != REQUIRED_INSIDE_KEYS:
        missing = REQUIRED_INSIDE_KEYS - actual_inside_keys
        extra = actual_inside_keys - REQUIRED_INSIDE_KEYS

        if missing:
            violations.append(
                f"Missing fields keys: {missing}"
            )

        if extra:
            violations.append(
                f"Extra fields keys: {extra}"
            )


    # 5. Every value inside "fields" must be null.
    fields = parsed.get("fields", {})

    for key, value in fields.items():
        if value is not None:
            violations.append(
            f"Field '{key}' must be null"
        )

    # 6. "urgency_level" must be one of EMERGENCY_LEVELS
    urgency_level = parsed.get("urgency_level")
    if urgency_level not in EMERGENCY_LEVELS:
        violations.append(
            f"Invalid urgency level: '{urgency_level}'"
        )

    # 7. "answer" must be a string of at most
    # 20 words.
    answer = parsed.get("answer", "")
    if isinstance(answer, str):
        word_count = len(answer.split())
        if word_count == 0:
            violations.append("Answer is empty")
        elif word_count > MAX_SUMMARY_WORDS:
            violations.append(
                f"Answer has {word_count} words "
                f"(max {MAX_SUMMARY_WORDS})"
            )
    else:
        violations.append(
            "Answer is not a string"
        )

    #8. "urgency_rationale" must be a string
    urgency_rationale = parsed.get("urgency_rationale", "")
    if not isinstance(urgency_rationale, str):
        violations.append(
            "Urgency rationale is not a string"
        )   


    return {
        "valid": len(violations) == 0,
        "violations": violations,
    }