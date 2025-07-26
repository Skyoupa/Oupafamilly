"""
Monitoring and Health Check Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from datetime import datetime
from monitoring import health, metrics, app_logger
import psutil
import os

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Comprehensive health check endpoint"""
    
    app_logger.info("Health check requested")
    
    # Run all health checks
    database_health = await health.check_database_health()
    cache_health = health.check_cache_health()
    disk_health = health.check_disk_space()
    system_stats = metrics.get_system_stats()
    app_stats = metrics.get_app_metrics()
    
    # Determine overall status
    checks = {
        "database": database_health,
        "cache": cache_health,
        "disk_space": disk_health,
        "system": system_stats,
        "application": app_stats
    }
    
    # Overall health assessment
    critical_issues = []
    warnings = []
    
    if database_health["status"] != "healthy":
        critical_issues.append("database")
    
    if cache_health["status"] == "unhealthy":
        warnings.append("cache")
    
    if disk_health["status"] in ["critical", "warning"]:
        if disk_health["status"] == "critical":
            critical_issues.append("disk_space")
        else:
            warnings.append("disk_space")
    
    # CPU and memory warnings
    if system_stats.get("cpu_percent", 0) > 80:
        warnings.append("high_cpu")
    
    if system_stats.get("memory_percent", 0) > 85:
        warnings.append("high_memory")
    
    # Determine overall status
    if critical_issues:
        overall_status = "unhealthy"
    elif warnings:
        overall_status = "degraded"
    else:
        overall_status = "healthy"
    
    response = {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks,
        "issues": {
            "critical": critical_issues,
            "warnings": warnings
        }
    }
    
    # Log health status
    if overall_status != "healthy":
        app_logger.warning(
            f"Health check shows {overall_status} status",
            critical_issues=critical_issues,
            warnings=warnings
        )
    else:
        app_logger.info("Health check passed - all systems healthy")
    
    return response

@router.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get detailed system and application metrics"""
    
    app_logger.info("Metrics requested")
    
    system_stats = metrics.get_system_stats()
    app_stats = metrics.get_app_metrics()
    
    # Additional application metrics
    from database import db
    
    try:
        # Database metrics
        db_stats = await db.command("serverStatus")
        db_metrics = {
            "connections_current": db_stats.get("connections", {}).get("current", 0),
            "connections_available": db_stats.get("connections", {}).get("available", 0),
            "operations_per_sec": db_stats.get("opcounters", {})
        }
    except Exception as e:
        app_logger.error("Failed to get database metrics", error=str(e))
        db_metrics = {"error": "Unable to fetch database metrics"}
    
    # Cache metrics
    from cache import cache
    cache_metrics = {
        "enabled": cache.enabled,
        "default_ttl": cache.default_ttl if cache.enabled else None
    }
    
    if cache.enabled and cache.client:
        try:
            info = cache.client.info()
            cache_metrics.update({
                "used_memory": info.get("used_memory", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "connected_clients": info.get("connected_clients", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            })
        except Exception as e:
            cache_metrics["error"] = f"Unable to fetch cache metrics: {str(e)}"
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "system": system_stats,
        "application": app_stats,
        "database": db_metrics,
        "cache": cache_metrics,
        "environment": {
            "python_version": os.sys.version,
            "platform": os.uname() if hasattr(os, 'uname') else "unknown",
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    }

@router.get("/logs/recent")
async def get_recent_logs(
    level: str = "INFO",
    limit: int = 100
) -> Dict[str, Any]:
    """Get recent application logs (admin only)"""
    
    # This would require authentication check in real implementation
    # For now, returning basic structure
    
    app_logger.info("Recent logs requested", level=level, limit=limit)
    
    try:
        # In a real implementation, you'd read from log files
        # For now, returning a placeholder
        return {
            "logs": [
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "level": "INFO",
                    "message": "Application is running normally",
                    "module": "oupafamilly.monitoring"
                }
            ],
            "total": 1,
            "level_filter": level,
            "limit": limit
        }
    except Exception as e:
        app_logger.error("Failed to retrieve logs", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve logs"
        )

@router.post("/logs/rotate")
async def rotate_logs() -> Dict[str, str]:
    """Manually trigger log rotation (admin only)"""
    
    app_logger.info("Manual log rotation requested")
    
    try:
        # Trigger log rotation for all handlers
        import logging
        for handler in logging.getLogger().handlers:
            if hasattr(handler, 'doRollover'):
                handler.doRollover()
        
        app_logger.info("Log rotation completed successfully")
        return {"message": "Log rotation completed successfully"}
        
    except Exception as e:
        app_logger.error("Log rotation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Log rotation failed: {str(e)}"
        )

@router.get("/status/simple")
async def simple_status() -> Dict[str, str]:
    """Simple status check for load balancers"""
    
    # Quick database ping
    try:
        from database import db
        await db.command("ping")
        return {"status": "ok"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable"
        )