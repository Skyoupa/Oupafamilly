"""
Advanced Monitoring and Structured Logging Configuration
"""

import structlog
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps
import time
import psutil
import traceback
from pathlib import Path

# Create logs directory
LOGS_DIR = Path("/var/log/oupafamilly")
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def configure_structured_logging():
    """Configure structured logging with JSON output"""
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    # Configure structlog
    structlog.configure(
        processors=[
            # Add timestamp
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            # JSON processor for production
            structlog.processors.JSONRenderer() if os.getenv("ENVIRONMENT") == "production" 
            else structlog.dev.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Setup file handlers for different log levels
    app_logger = logging.getLogger("oupafamilly")
    
    # Main application log (rotating)
    app_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    app_logger.addHandler(app_handler)

    # Error log (rotating)
    error_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "error.log",
        maxBytes=5242880,  # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d')
    )
    app_logger.addHandler(error_handler)

    # Security events log
    security_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "security.log",
        maxBytes=5242880,  # 5MB
        backupCount=5
    )
    security_handler.setLevel(logging.WARNING)
    security_handler.setFormatter(
        logging.Formatter('%(asctime)s - SECURITY - %(levelname)s - %(message)s')
    )
    
    security_logger = logging.getLogger("security")
    security_logger.addHandler(security_handler)
    security_logger.setLevel(logging.WARNING)

# Initialize structured logging
configure_structured_logging()

# Get structured loggers
app_logger = structlog.get_logger("oupafamilly")
security_logger = structlog.get_logger("security")
performance_logger = structlog.get_logger("performance")

class SystemMetrics:
    """System metrics collector"""
    
    @staticmethod
    def get_system_stats() -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "process_count": len(psutil.pids()),
                "boot_time": psutil.boot_time(),
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            }
        except Exception as e:
            app_logger.error("Failed to collect system metrics", error=str(e))
            return {}
    
    @staticmethod
    def get_app_metrics() -> Dict[str, Any]:
        """Get application-specific metrics"""
        try:
            process = psutil.Process()
            return {
                "memory_rss": process.memory_info().rss,
                "memory_vms": process.memory_info().vms,
                "cpu_percent": process.cpu_percent(),
                "num_threads": process.num_threads(),
                "num_fds": process.num_fds() if hasattr(process, 'num_fds') else 0,
                "create_time": process.create_time(),
                "status": process.status()
            }
        except Exception as e:
            app_logger.error("Failed to collect app metrics", error=str(e))
            return {}

def log_performance(operation: str, threshold_ms: float = 1000):
    """Decorator to log slow operations"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            operation_id = f"{func.__module__}.{func.__name__}"
            
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                
                if duration_ms > threshold_ms:
                    performance_logger.warning(
                        "Slow operation detected",
                        operation=operation,
                        operation_id=operation_id,
                        duration_ms=round(duration_ms, 2),
                        threshold_ms=threshold_ms
                    )
                else:
                    performance_logger.info(
                        "Operation completed",
                        operation=operation,
                        operation_id=operation_id,
                        duration_ms=round(duration_ms, 2)
                    )
                
                return result
                
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                performance_logger.error(
                    "Operation failed",
                    operation=operation,
                    operation_id=operation_id,
                    duration_ms=round(duration_ms, 2),
                    error=str(e),
                    traceback=traceback.format_exc()
                )
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            operation_id = f"{func.__module__}.{func.__name__}"
            
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                
                if duration_ms > threshold_ms:
                    performance_logger.warning(
                        "Slow operation detected",
                        operation=operation,
                        operation_id=operation_id,
                        duration_ms=round(duration_ms, 2),
                        threshold_ms=threshold_ms
                    )
                else:
                    performance_logger.info(
                        "Operation completed",
                        operation=operation,
                        operation_id=operation_id,
                        duration_ms=round(duration_ms, 2)
                    )
                
                return result
                
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                performance_logger.error(
                    "Operation failed",
                    operation=operation,
                    operation_id=operation_id,
                    duration_ms=round(duration_ms, 2),
                    error=str(e),
                    traceback=traceback.format_exc()
                )
                raise
        
        return async_wrapper if hasattr(func, '__code__') and func.__code__.co_flags & 0x80 else sync_wrapper
    return decorator

def log_security_event(event_type: str, user_id: str = None, details: Dict[str, Any] = None):
    """Log security-related events"""
    security_logger.warning(
        f"Security event: {event_type}",
        event_type=event_type,
        user_id=user_id,
        details=details or {},
        timestamp=datetime.utcnow().isoformat()
    )

def log_user_action(user_id: str, action: str, details: Dict[str, Any] = None):
    """Log user actions for audit trail"""
    app_logger.info(
        f"User action: {action}",
        user_id=user_id,
        action=action,
        details=details or {},
        timestamp=datetime.utcnow().isoformat()
    )

class HealthChecker:
    """Advanced health check utilities"""
    
    @staticmethod
    async def check_database_health() -> Dict[str, Any]:
        """Check database connectivity and performance"""
        from database import db
        
        start_time = time.time()
        try:
            # Simple ping
            await db.command("ping")
            ping_duration = (time.time() - start_time) * 1000
            
            # Check collections
            collections = await db.list_collection_names()
            
            return {
                "status": "healthy",
                "ping_duration_ms": round(ping_duration, 2),
                "collections_count": len(collections),
                "responsive": ping_duration < 100  # Less than 100ms is good
            }
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            app_logger.error("Database health check failed", error=str(e), duration_ms=duration)
            return {
                "status": "unhealthy",
                "error": str(e),
                "duration_ms": round(duration, 2)
            }
    
    @staticmethod
    def check_cache_health() -> Dict[str, Any]:
        """Check Redis cache health"""
        from cache import cache
        
        if not cache.enabled:
            return {"status": "disabled"}
        
        start_time = time.time()
        try:
            # Test set/get operation
            test_key = "health_check_test"
            cache.set(test_key, "test_value", 10)
            result = cache.get(test_key)
            cache.delete(test_key)
            
            duration = (time.time() - start_time) * 1000
            
            return {
                "status": "healthy" if result == "test_value" else "degraded",
                "operation_duration_ms": round(duration, 2),
                "responsive": duration < 50
            }
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            app_logger.error("Cache health check failed", error=str(e), duration_ms=duration)
            return {
                "status": "unhealthy",
                "error": str(e),
                "duration_ms": round(duration, 2)
            }
    
    @staticmethod
    def check_disk_space() -> Dict[str, Any]:
        """Check available disk space"""
        try:
            usage = psutil.disk_usage('/')
            free_percent = (usage.free / usage.total) * 100
            
            return {
                "status": "healthy" if free_percent > 10 else "warning" if free_percent > 5 else "critical",
                "free_percent": round(free_percent, 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "total_gb": round(usage.total / (1024**3), 2)
            }
        except Exception as e:
            app_logger.error("Disk space check failed", error=str(e))
            return {"status": "unknown", "error": str(e)}

# Middleware for request logging
class RequestLoggingMiddleware:
    """Middleware to log all API requests"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            
            # Log request
            app_logger.info(
                "Request started",
                method=scope["method"],
                path=scope["path"],
                query_string=scope.get("query_string", b"").decode(),
                user_agent=dict(scope.get("headers", [])).get(b"user-agent", b"").decode()
            )
            
            # Process request
            response_status = 500  # Default to error
            
            async def send_wrapper(message):
                nonlocal response_status
                if message["type"] == "http.response.start":
                    response_status = message["status"]
                await send(message)
            
            try:
                await self.app(scope, receive, send_wrapper)
            except Exception as e:
                app_logger.error(
                    "Request failed with exception",
                    method=scope["method"],
                    path=scope["path"],
                    error=str(e),
                    traceback=traceback.format_exc()
                )
                raise
            finally:
                duration_ms = (time.time() - start_time) * 1000
                
                # Log response
                log_level = "info" if response_status < 400 else "warning" if response_status < 500 else "error"
                getattr(app_logger, log_level)(
                    "Request completed",
                    method=scope["method"],
                    path=scope["path"],
                    status_code=response_status,
                    duration_ms=round(duration_ms, 2)
                )
        else:
            await self.app(scope, receive, send)

# Export monitoring utilities
metrics = SystemMetrics()
health = HealthChecker()