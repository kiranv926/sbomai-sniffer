#!/usr/bin/env python3
"""
SBOMAI AI Microservice - gRPC Server

Advanced AI/ML microservice for intelligent, explainable, and predictive SBOM analysis.
Provides gRPC endpoints for risk explanation, prediction, remediation suggestions, and explainable chains.
"""

import os
import sys
import time
import signal
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import grpc
from grpc import aio
import structlog

from src.sbomai_ai import SbomaiAiService
from src.sbomai_ai.config import get_config, validate_config
from src.sbomai_ai.utils.monitoring import setup_monitoring, get_metrics_response
from src.sbomai_ai.utils.exceptions import SbomaiAiError

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


class MetricsServer:
    """HTTP server for Prometheus metrics"""
    
    def __init__(self, port: int = 9090):
        self.port = port
        self.server = None
    
    async def start(self):
        """Start the metrics server"""
        from aiohttp import web
        
        async def metrics_handler(request):
            """Handle metrics requests"""
            metrics_data, content_type = get_metrics_response()
            return web.Response(body=metrics_data, content_type=content_type)
        
        async def health_handler(request):
            """Handle health check requests"""
            return web.json_response({
                "status": "healthy",
                "timestamp": time.time(),
                "service": "sbomai-ai"
            })
        
        app = web.Application()
        app.router.add_get('/metrics', metrics_handler)
        app.router.add_get('/health', health_handler)
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        self.server = web.TCPSite(runner, '0.0.0.0', self.port)
        await self.server.start()
        
        logger.info(f"Metrics server started on port {self.port}")
    
    async def stop(self):
        """Stop the metrics server"""
        if self.server:
            await self.server.stop()
            logger.info("Metrics server stopped")


class SbomaiAiServer:
    """Main gRPC server for SBOMAI AI Microservice"""
    
    def __init__(self):
        self.config = get_config()
        self.grpc_server = None
        self.metrics_server = None
        self.service = None
        self.executor = ThreadPoolExecutor(max_workers=self.config.service.grpc_max_workers)
        self.start_time = time.time()
    
    async def start(self):
        """Start the gRPC server"""
        try:
            # Validate configuration
            config_issues = validate_config()
            if config_issues:
                logger.error("Configuration validation failed:")
                for issue in config_issues:
                    logger.error(f"  - {issue}")
                raise SbomaiAiError("Invalid configuration")
            
            # Setup monitoring
            if self.config.service.enable_metrics:
                setup_monitoring()
                self.metrics_server = MetricsServer(self.config.service.metrics_port)
                await self.metrics_server.start()
            
            # Create gRPC server
            self.grpc_server = aio.server(
                self.executor,
                options=[
                    ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50MB
                    ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50MB
                    ('grpc.max_concurrent_streams', self.config.service.grpc_max_concurrent_rpcs),
                ]
            )
            
            # Initialize service
            self.service = SbomaiAiService()
            await self.service.initialize()
            
            # Add service to server
            from src.sbomai_ai import sbomai_ai_pb2_grpc
            sbomai_ai_pb2_grpc.add_SbomaiAiServiceServicer_to_server(self.service, self.grpc_server)
            
            # Start server
            listen_addr = f"{self.config.service.grpc_host}:{self.config.service.grpc_port}"
            self.grpc_server.add_insecure_port(listen_addr)
            await self.grpc_server.start()
            
            logger.info(f"SBOMAI AI Microservice started on {listen_addr}")
            logger.info(f"Service capabilities: {self.service.get_capabilities()}")
            
            # Keep server running
            await self.grpc_server.wait_for_termination()
            
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise
    
    async def stop(self):
        """Stop the gRPC server"""
        try:
            if self.grpc_server:
                await self.grpc_server.stop(grace=30)  # 30 second grace period
                logger.info("gRPC server stopped")
            
            if self.metrics_server:
                await self.metrics_server.stop()
            
            if self.service:
                await self.service.cleanup()
            
            self.executor.shutdown(wait=True)
            logger.info("Server shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during server shutdown: {e}")
    
    def get_uptime(self) -> float:
        """Get server uptime in seconds"""
        return time.time() - self.start_time


async def main():
    """Main entry point"""
    server = SbomaiAiServer()
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        asyncio.create_task(server.stop())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
    finally:
        await server.stop()


def run_server():
    """Run the server with proper error handling"""
    try:
        # Set up logging
        logging.basicConfig(
            level=getattr(logging, get_config().service.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Log startup information
        logger.info("Starting SBOMAI AI Microservice")
        logger.info(f"Environment: {get_config().environment}")
        logger.info(f"Debug mode: {get_config().debug}")
        logger.info(f"gRPC port: {get_config().service.grpc_port}")
        logger.info(f"Metrics enabled: {get_config().service.enable_metrics}")
        
        # Run the server
        asyncio.run(main())
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_server() 