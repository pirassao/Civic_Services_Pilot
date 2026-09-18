from dotenv import load_dotenv
import os

load_dotenv()  

MODEL_NAME: str = os.getenv("MODEL_NAME", "openai/gpt-5-mini")
PHOENIX_PROJECT_NAME: str = os.getenv(
    "PHOENIX_PROJECT_NAME", "civic-services-pilot"
)
PHOENIX_COLLECTOR_ENDPOINT: str = os.getenv(
    "PHOENIX_COLLECTOR_ENDPOINT",
    "http://localhost:6006/v1/traces",
)