"""
Monitoring and metrics utilities for SBOMAI AI Microservice
"""

import logging
import time
from typing import Dict, Any, Optional
from functools import wraps
from prometheus_client import Counter, Histogram, Gauge, Summary, generate_latest, CONTENT_TYPE_LATEST
import structlog

from ..config import get_config

logger = structlog.get_logger()

# Prometheus metrics
REQUEST_COUNT = Counter(
    'sbomai_ai_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'sbomai_ai_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

MODEL_PREDICTION_COUNT = Counter(
    'sbomai_ai_model_predictions_total',
    'Total number of model predictions',
    ['model_type', 'model_name', 'status']
)

MODEL_PREDICTION_DURATION = Histogram(
    'sbomai_ai_model_prediction_duration_seconds',
    'Model prediction duration in seconds',
    ['model_type', 'model_name']
)

AI_API_CALLS = Counter(
    'sbomai_ai_api_calls_total',
    'Total number of AI API calls',
    ['provider', 'model', 'status']
)

AI_API_DURATION = Histogram(
    'sbomai_ai_api_duration_seconds',
    'AI API call duration in seconds',
    ['provider', 'model']
)

CACHE_HITS = Counter(
    'sbomai_ai_cache_hits_total',
    'Total number of cache hits',
    ['cache_type']
)

CACHE_MISSES = Counter(
    'sbomai_ai_cache_misses_total',
    'Total number of cache misses',
    ['cache_type']
)

ACTIVE_REQUESTS = Gauge(
    'sbomai_ai_active_requests',
    'Number of active requests',
    ['endpoint']
)

MODEL_LOAD_TIME = Summary(
    'sbomai_ai_model_load_time_seconds',
    'Time taken to load models',
    ['model_type', 'model_name']
)

ERROR_COUNT = Counter(
    'sbomai_ai_errors_total',
    'Total number of errors',
    ['error_type', 'endpoint']
)

MEMORY_USAGE = Gauge(
    'sbomai_ai_memory_bytes',
    'Memory usage in bytes',
    ['type']
)

CPU_USAGE = Gauge(
    'sbomai_ai_cpu_percent',
    'CPU usage percentage'
)


def monitor_request(method: str, endpoint: str):
    """Decorator to monitor request metrics"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            ACTIVE_REQUESTS.labels(endpoint=endpoint).inc()
            
            try:
                result = await func(*args, **kwargs)
                REQUEST_COUNT.labels(method=method, endpoint=endpoint, status="success").inc()
                return result
            except Exception as e:
                REQUEST_COUNT.labels(method=method, endpoint=endpoint, status="error").inc()
                ERROR_COUNT.labels(error_type=type(e).__name__, endpoint=endpoint).inc()
                raise
            finally:
                duration = time.time() - start_time
                REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
                ACTIVE_REQUESTS.labels(endpoint=endpoint).dec()
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            ACTIVE_REQUESTS.labels(endpoint=endpoint).inc()
            
            try:
                result = func(*args, **kwargs)
                REQUEST_COUNT.labels(method=method, endpoint=endpoint, status="success").inc()
                return result
            except Exception as e:
                REQUEST_COUNT.labels(method=method, endpoint=endpoint, status="error").inc()
                ERROR_COUNT.labels(error_type=type(e).__name__, endpoint=endpoint).inc()
                raise
            finally:
                duration = time.time() - start_time
                REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
                ACTIVE_REQUESTS.labels(endpoint=endpoint).dec()
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def monitor_model_prediction(model_type: str, model_name: str):
    """Decorator to monitor model prediction metrics"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                MODEL_PREDICTION_COUNT.labels(
                    model_type=model_type, 
                    model_name=model_name, 
                    status="success"
                ).inc()
                return result
            except Exception as e:
                MODEL_PREDICTION_COUNT.labels(
                    model_type=model_type, 
                    model_name=model_name, 
                    status="error"
                ).inc()
                raise
            finally:
                duration = time.time() - start_time
                MODEL_PREDICTION_DURATION.labels(
                    model_type=model_type, 
                    model_name=model_name
                ).observe(duration)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                MODEL_PREDICTION_COUNT.labels(
                    model_type=model_type, 
                    model_name=model_name, 
                    status="success"
                ).inc()
                return result
            except Exception as e:
                MODEL_PREDICTION_COUNT.labels(
                    model_type=model_type, 
                    model_name=model_name, 
                    status="error"
                ).inc()
                raise
            finally:
                duration = time.time() - start_time
                MODEL_PREDICTION_DURATION.labels(
                    model_type=model_type, 
                    model_name=model_name
                ).observe(duration)
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def monitor_ai_api_call(provider: str, model: str):
    """Decorator to monitor AI API call metrics"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                AI_API_CALLS.labels(provider=provider, model=model, status="success").inc()
                return result
            except Exception as e:
                AI_API_CALLS.labels(provider=provider, model=model, status="error").inc()
                raise
            finally:
                duration = time.time() - start_time
                AI_API_DURATION.labels(provider=provider, model=model).observe(duration)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                AI_API_CALLS.labels(provider=provider, model=model, status="success").inc()
                return result
            except Exception as e:
                AI_API_CALLS.labels(provider=provider, model=model, status="error").inc()
                raise
            finally:
                duration = time.time() - start_time
                AI_API_DURATION.labels(provider=provider, model=model).observe(duration)
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class MetricsCollector:
    """Collector for system metrics"""
    
    def __init__(self):
        self.config = get_config()
        self.start_time = time.time()
    
    def collect_system_metrics(self):
        """Collect system metrics"""
        try:
            import psutil
            
            # Memory metrics
            memory = psutil.virtual_memory()
            MEMORY_USAGE.labels(type="total").set(memory.total)
            MEMORY_USAGE.labels(type="available").set(memory.available)
            MEMORY_USAGE.labels(type="used").set(memory.used)
            MEMORY_USAGE.labels(type="percent").set(memory.percent)
            
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            CPU_USAGE.set(cpu_percent)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            MEMORY_USAGE.labels(type="disk_total").set(disk.total)
            MEMORY_USAGE.labels(type="disk_used").set(disk.used)
            MEMORY_USAGE.labels(type="disk_free").set(disk.free)
            
        except ImportError:
            logger.warning("psutil not available, skipping system metrics")
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
    
    def get_uptime(self) -> float:
        """Get service uptime in seconds"""
        return time.time() - self.start_time
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        return {
            "uptime_seconds": self.get_uptime(),
            "total_requests": REQUEST_COUNT._value.sum(),
            "total_errors": ERROR_COUNT._value.sum(),
            "active_requests": ACTIVE_REQUESTS._value.sum(),
            "total_predictions": MODEL_PREDICTION_COUNT._value.sum(),
            "total_api_calls": AI_API_CALLS._value.sum(),
            "cache_hits": CACHE_HITS._value.sum(),
            "cache_misses": CACHE_MISSES._value.sum(),
        }


class CacheMonitor:
    """Monitor cache performance"""
    
    @staticmethod
    def record_cache_hit(cache_type: str):
        """Record a cache hit"""
        CACHE_HITS.labels(cache_type=cache_type).inc()
    
    @staticmethod
    def record_cache_miss(cache_type: str):
        """Record a cache miss"""
        CACHE_MISSES.labels(cache_type=cache_type).inc()
    
    @staticmethod
    def get_cache_hit_rate(cache_type: str) -> float:
        """Calculate cache hit rate"""
        hits = CACHE_HITS.labels(cache_type=cache_type)._value.sum()
        misses = CACHE_MISSES.labels(cache_type=cache_type)._value.sum()
        total = hits + misses
        return hits / total if total > 0 else 0.0


class ModelMonitor:
    """Monitor model performance"""
    
    @staticmethod
    def record_model_load_time(model_type: str, model_name: str, load_time: float):
        """Record model load time"""
        MODEL_LOAD_TIME.labels(model_type=model_type, model_name=model_name).observe(load_time)
    
    @staticmethod
    def get_model_stats(model_type: str, model_name: str) -> Dict[str, Any]:
        """Get model statistics"""
        predictions = MODEL_PREDICTION_COUNT.labels(
            model_type=model_type, 
            model_name=model_name
        )._value.sum()
        
        errors = MODEL_PREDICTION_COUNT.labels(
            model_type=model_type, 
            model_name=model_name, 
            status="error"
        )._value.sum()
        
        success_rate = (predictions - errors) / predictions if predictions > 0 else 0.0
        
        return {
            "total_predictions": predictions,
            "errors": errors,
            "success_rate": success_rate,
            "avg_prediction_time": MODEL_PREDICTION_DURATION.labels(
                model_type=model_type, 
                model_name=model_name
            )._sum.sum() / predictions if predictions > 0 else 0.0
        }


def get_metrics_response():
    """Get Prometheus metrics response"""
    return generate_latest(), CONTENT_TYPE_LATEST


def setup_monitoring():
    """Setup monitoring configuration"""
    config = get_config()
    
    if config.service.enable_metrics:
        logger.info("Monitoring enabled")
        
        # Start metrics collection
        metrics_collector = MetricsCollector()
        
        # Schedule periodic metrics collection
        import threading
        import time
        
        def collect_metrics_periodically():
            while True:
                try:
                    metrics_collector.collect_system_metrics()
                    time.sleep(60)  # Collect every minute
                except Exception as e:
                    logger.error(f"Error in periodic metrics collection: {e}")
                    time.sleep(60)
        
        metrics_thread = threading.Thread(target=collect_metrics_periodically, daemon=True)
        metrics_thread.start()
        
        return metrics_collector
    else:
        logger.info("Monitoring disabled")
        return None 