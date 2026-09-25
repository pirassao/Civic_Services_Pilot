from openai import OpenAI
from .config import MODEL_NAME

client = OpenAI()  # reads the API key and base URL from the environment


def call_model_json(
    instructions: str,
    user_input: str,
) -> str:
    """Return a syntactically valid JSON object string."""
    # JSON object mode requires the word JSON in the model input.
    #qui aggiunge Respond in JSON. solo se non c'è nel testo!!!!
    if "json" not in user_input.lower():
        user_input = f"{user_input}\n\nRespond in JSON."

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=instructions,
        input=user_input,
        text={"format": {"type": "json_object"}},
    )
    return response.output_text.strip()



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