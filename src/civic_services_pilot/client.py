from openai import OpenAI
from .config import MODEL_NAME

client = OpenAI()  # reads the API key and base URL from the environment


def call_model(
    instructions: str,
    user_input: str,
) -> str:
    """Send query and response"""
    response = client.responses.create(
        model=MODEL_NAME,
        instructions=instructions,
        input=user_input,
        #max_output_tokens=150,
    )
    return response.output_text.strip()