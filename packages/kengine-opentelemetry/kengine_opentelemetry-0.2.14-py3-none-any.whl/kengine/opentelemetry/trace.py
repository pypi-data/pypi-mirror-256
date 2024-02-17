from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    BatchSpanProcessor,
    ConsoleSpanExporter
)

from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPSpanExporter
)

from kengine.opentelemetry.options import KengineOptions

def create_tracer_provider(
    options: KengineOptions,
    resource: Resource
) -> TracerProvider:
    """
    Configures and returns a new TracerProvider to send traces telemetry.

    Args:
        options (KengineOptions): the Kengine options to configure with
        resource (Resource): the resource to use with the new tracer provider

    Returns:
        TracerProvider: the new tracer provider
    """

    exporter = HTTPSpanExporter(
        endpoint=options.get_traces_endpoint(),
        headers=options.get_trace_headers(),
    )
    trace_provider = TracerProvider(
        resource=resource,
    )

    trace_provider.add_span_processor(
        BatchSpanProcessor(
            exporter
        )
    )
    if options.export_console:
        trace_provider.add_span_processor(
            SimpleSpanProcessor(
                ConsoleSpanExporter()
            )
        )
    return trace_provider