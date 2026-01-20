# dummy-service

A minimal FastAPI service instrumented for full observability: metrics, logs, and distributed traces.

---

## Development Notes

This project was built as an interview assignment to demonstrate end-to-end observability in a small, self-contained service. The focus was on instrumentation and integration rather than business logic or production hardening.

The code is intentionally minimal and exists mainly as a reference implementation.

---

## What It Does

- Exposes a `/ping` endpoint that simulates work with random latency
- Exposes a `/metrics` endpoint for Prometheus scraping
- Generates distributed traces using OpenTelemetry
  - Includes nested spans to demonstrate trace structure
- Exports traces via OTLP to Grafana Tempo
- Records custom Prometheus metrics:
  - Request count
  - Request latency
- Uses structured logging
  - Logs to both console and file

---

## Observability Stack (Docker Compose)

The project includes a local Docker Compose setup providing a full observability backend:

- **Prometheus** — metrics collection
- **Grafana** — visualization and dashboards
- **Loki** — log aggregation
- **Promtail** — log shipping
- **Tempo** — distributed tracing

All components run locally and are preconfigured to integrate with each other, allowing correlated exploration of metrics, logs, and traces for the FastAPI service.

---

## Usage

- Start the observability stack and service using Docker Compose
- Send requests to:
  /ping
- Inspect:
- Metrics in Prometheus / Grafana
- Logs in Loki via Grafana
- Traces in Tempo via Grafana

---

## Status

Not actively maintained.  
Kept as an interview assignment and observability reference project.
