from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random
import asyncio

app = FastAPI()

REQUEST_COUNT = Counter("request_count", "Total Requests")
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency in seconds")

@app.get("/ping")
async def root():
    start_time = time.time()
    
    REQUEST_COUNT.inc()
    #time.sleep(random.random())
    await asyncio.sleep(random.random())
    REQUEST_LATENCY.observe(time.time() - start_time)

    return {"message": "Mr. Ping is alive"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
