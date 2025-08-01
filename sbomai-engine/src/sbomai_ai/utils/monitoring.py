"""
Monitoring utilities for SBOMAI.
"""

import functools
import time
from typing import Callable, Any
from prometheus_client import (
    Counter, Histogram, Gauge,
    generate_latest, CONTENT_TYPE_LATEST,
    CollectorRegistry
)

# Create custom registry
REGISTRY = CollectorRegistry()

# Request metrics
REQUEST_DURATION = Histogram(
    'sbomai_request_duration_seconds',
    'Request duration in seconds',
    ['method'],
    registry=REGISTRY
)

REQUEST_COUNT = Counter(
    'sbomai_request_total',
    'Total number of requests',
    ['method', 'status'],
    registry=REGISTRY
)

# Model metrics
MODEL_LATENCY = Histogram(
    'sbomai_model_latency_seconds',
    'Model inference latency in seconds',
    ['model'],
    registry=REGISTRY
)

MODEL_CALLS = Counter(
    'sbomai_model_calls_total',
    'Total number of model calls',
    ['model'],
    registry=REGISTRY
)

MODEL_ERRORS = Counter(
    'sbomai_model_errors_total',
    'Total number of model errors',
    ['model', 'error_type'],
    registry=REGISTRY
)

# Cache metrics
CACHE_HITS = Counter(
    'sbomai_cache_hits_total',
    'Total number of cache hits',
    ['cache_type'],
    registry=REGISTRY
)

CACHE_MISSES = Counter(
    'sbomai_cache_misses_total',
    'Total number of cache misses',
    ['cache_type'],
    registry=REGISTRY
)

CACHE_SIZE = Gauge(
    'sbomai_cache_size_bytes',
    'Current cache size in bytes',
    ['cache_type'],
    registry=REGISTRY
)

def track_request_duration(func: Callable) -> Callable:
    """Track request duration using Prometheus histogram"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        method = func.__name__
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            REQUEST_COUNT.labels(
                method=method,
                status='success'
            ).inc()
            return result
        
        except Exception as e:
            REQUEST_COUNT.labels(
                method=method,
                status='error'
            ).inc()
            raise e
        
        finally:
            duration = time.time() - start_time
            REQUEST_DURATION.labels(method=method).observe(duration)
    
    return wrapper

def record_model_metrics(model: str, latency: float):
    """Record model metrics"""
    MODEL_LATENCY.labels(model=model).observe(latency)
    MODEL_CALLS.labels(model=model).inc()

def record_model_error(model: str, error_type: str):
    """Record model error"""
    MODEL_ERRORS.labels(
        model=model,
        error_type=error_type
    ).inc()

def record_cache_hit(cache_type: str):
    """Record cache hit"""
    CACHE_HITS.labels(cache_type=cache_type).inc()

def record_cache_miss(cache_type: str):
    """Record cache miss"""
    CACHE_MISSES.labels(cache_type=cache_type).inc()

def update_cache_size(cache_type: str, size: int):
    """Update cache size gauge"""
    CACHE_SIZE.labels(cache_type=cache_type).set(size)

def get_metrics() -> bytes:
    """Get current metrics in Prometheus format"""
    return generate_latest(REGISTRY)