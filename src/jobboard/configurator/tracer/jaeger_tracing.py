import os

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource.create({SERVICE_NAME: os.environ.get("JAEGER_SERVICE_NAME")})
tracer = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer)

jaeger_exporter = JaegerExporter(
    agent_host_name=os.environ.get("JAEGER_AGENT_HOST"),
    agent_port=int(os.environ.get("JAEGER_AGENT_PORT"))
    if os.environ.get("JAEGER_AGENT_PORT")
    else None,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
tracer.add_span_processor(span_processor)
LoggingInstrumentor().instrument(set_logging_format=True)
