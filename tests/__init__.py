from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

resource = Resource(attributes={SERVICE_NAME: "test-exporter"})
provider = TracerProvider(resource=resource)
span_exporter = InMemorySpanExporter()
processor = SimpleSpanProcessor(span_exporter)
provider.add_span_processor(processor)

trace.set_tracer_provider(provider)
