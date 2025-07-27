"""
Helper utilities for SBOMAI AI Microservice
"""

import json
import logging
import time
from typing import Dict, List, Any, Optional
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)


def timing_decorator(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"{func.__name__} executed in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {e}")
            raise
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"{func.__name__} executed in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {e}")
            raise
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """Decorator to retry functions with exponential backoff"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"All {max_retries} attempts failed")
                        raise last_exception
            
            raise last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                        time.sleep(delay)
                    else:
                        logger.error(f"All {max_retries} attempts failed")
                        raise last_exception
            
            raise last_exception
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def validate_sbom_component(component: Dict[str, Any]) -> List[str]:
    """Validate SBOM component data"""
    errors = []
    
    if not component.get("name"):
        errors.append("Component name is required")
    
    if not component.get("version"):
        errors.append("Component version is required")
    
    # Validate version format (basic check)
    version = component.get("version", "")
    if version and not _is_valid_version_format(version):
        errors.append(f"Invalid version format: {version}")
    
    return errors


def validate_vulnerability(vulnerability: Dict[str, Any]) -> List[str]:
    """Validate vulnerability data"""
    errors = []
    
    if not vulnerability.get("id"):
        errors.append("Vulnerability ID is required")
    
    cvss_score = vulnerability.get("cvss_score", 0)
    if cvss_score < 0 or cvss_score > 10:
        errors.append(f"CVSS score must be between 0 and 10, got: {cvss_score}")
    
    return errors


def _is_valid_version_format(version: str) -> bool:
    """Check if version string has valid format"""
    import re
    # Basic version format validation (semver-like)
    pattern = r'^[0-9]+\.[0-9]+(\.[0-9]+)?(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$'
    return bool(re.match(pattern, version))


def extract_component_metadata(component: Dict[str, Any]) -> Dict[str, Any]:
    """Extract useful metadata from SBOM component"""
    metadata = {
        "name_length": len(component.get("name", "")),
        "version_length": len(component.get("version", "")),
        "description_length": len(component.get("description", "")),
        "license_count": len(component.get("licenses", [])),
        "tag_count": len(component.get("tags", [])),
        "has_purl": bool(component.get("purl")),
        "has_description": bool(component.get("description")),
        "has_licenses": bool(component.get("licenses")),
    }
    
    # Add version analysis
    version = component.get("version", "")
    if version:
        metadata.update({
            "is_prerelease": any(x in version.lower() for x in ["alpha", "beta", "rc", "pre"]),
            "major_version": _extract_major_version(version),
            "minor_version": _extract_minor_version(version),
            "patch_version": _extract_patch_version(version),
        })
    
    return metadata


def _extract_major_version(version: str) -> Optional[int]:
    """Extract major version number"""
    try:
        parts = version.split(".")
        return int(parts[0]) if parts else None
    except (ValueError, IndexError):
        return None


def _extract_minor_version(version: str) -> Optional[int]:
    """Extract minor version number"""
    try:
        parts = version.split(".")
        return int(parts[1]) if len(parts) > 1 else None
    except (ValueError, IndexError):
        return None


def _extract_patch_version(version: str) -> Optional[int]:
    """Extract patch version number"""
    try:
        parts = version.split(".")
        return int(parts[2]) if len(parts) > 2 else None
    except (ValueError, IndexError):
        return None


def calculate_risk_score(vulnerabilities: List[Dict[str, Any]], component_metadata: Dict[str, Any]) -> float:
    """Calculate risk score based on vulnerabilities and component metadata"""
    base_score = 5.0
    
    # Adjust based on vulnerabilities
    if vulnerabilities:
        max_cvss = max(v.get("cvss_score", 0) for v in vulnerabilities)
        avg_cvss = sum(v.get("cvss_score", 0) for v in vulnerabilities) / len(vulnerabilities)
        base_score += max_cvss * 0.3 + avg_cvss * 0.2
    
    # Adjust based on component characteristics
    if component_metadata.get("is_prerelease"):
        base_score += 2.0
    
    if not component_metadata.get("has_licenses"):
        base_score += 1.0
    
    if component_metadata.get("major_version", 0) == 0:
        base_score += 1.5
    
    # Normalize to 0-10 range
    return min(max(base_score, 0.0), 10.0)


def format_prompt_template(template: str, **kwargs) -> str:
    """Format prompt template with provided variables"""
    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.warning(f"Missing template variable: {e}")
        # Replace missing variables with placeholders
        for key in kwargs:
            template = template.replace(f"{{{key}}}", str(kwargs[key]))
        return template


def safe_json_serialize(obj: Any) -> str:
    """Safely serialize object to JSON"""
    try:
        return json.dumps(obj, default=str, indent=2)
    except Exception as e:
        logger.error(f"Failed to serialize object to JSON: {e}")
        return str(obj)


def parse_json_safely(json_str: str) -> Optional[Dict[str, Any]]:
    """Safely parse JSON string"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return None


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dictionaries, with dict2 taking precedence"""
    result = dict1.copy()
    result.update(dict2)
    return result


def get_nested_value(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Get nested value from dictionary using dot notation"""
    keys = path.split(".")
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


def set_nested_value(data: Dict[str, Any], path: str, value: Any) -> None:
    """Set nested value in dictionary using dot notation"""
    keys = path.split(".")
    current = data
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system operations"""
    import re
    # Remove or replace unsafe characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    # Limit length
    if len(sanitized) > 255:
        sanitized = sanitized[:255]
    return sanitized or "unnamed_file"


def create_logger(name: str, level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """Create a configured logger"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger 