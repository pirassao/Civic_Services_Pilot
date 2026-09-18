from .client import call_model
from .prompts.loader import load_prompt
from .tracing import get_tracer

tracer = get_tracer(__name__)

def staff_assistant_reply(
        message: str,
        ticket_id: str,
        role: str
) -> str:
    """A staff assistant, replies technical information."""
    
    instructions = load_prompt(f"{role}_assistant")

    with tracer.start_as_current_span(
        "staff_assistant"
    ) as span:
        span.set_attribute("ticket_id", ticket_id)
        answer = call_model(
            instructions=instructions,
            user_input=message,
        )
        return answer