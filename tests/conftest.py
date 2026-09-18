import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)
from openinference.instrumentation.openai import OpenAIInstrumentor


@pytest.fixture(scope="session", autouse=True)
def span_exporter() -> InMemorySpanExporter:
    """Install a test TracerProvider before any test runs.

    Replaces the Phoenix exporter with an in-memory one so
    Phoenix does not need to be running during tests.
    scope="session" runs this once for the whole suite.
    autouse=True activates it for every test automatically.
    """
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    # Instrument the OpenAI client against the test provider
    # so model calls produce spans in the in-memory exporter.
    OpenAIInstrumentor().instrument(tracer_provider=provider)
    return exporter
