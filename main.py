from fastapi import FastAPI, Request
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
import time
import random
import asyncio
import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource

# Configure tracing
resource = Resource(attributes={
    "service.name": "fastapi-dummy-service"
})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter to send to Tempo
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

#logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

registry = CollectorRegistry() #doing this makes the boilerplate promethues metrics not generate
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "http_status"],
    registry=registry
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
    registry=registry
)
@app.get("/ping")
async def root(request: Request):
    with tracer.start_as_current_span("ping_endpoint") as span:
        start_time = time.time()
        logger.info(f"Received {request.method} request to /ping")
        
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        
        # Simulate some work with a child span
        with tracer.start_as_current_span("simulate_work"):
            sleep_time = random.random()
            span.set_attribute("work.sleep_time", sleep_time)
            await asyncio.sleep(sleep_time)
        
        latency = time.time() - start_time
        
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint="/ping",
            http_status=200
        ).inc()
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint="/ping"
        ).observe(latency)
        
        span.set_attribute("http.status_code", 200)
        span.set_attribute("response.latency", latency)
        
        logger.info(f"Request completed in {latency:.3f}s")
        return {"message": "Mr. Ping is alive"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)
