"""
Helper utilities for SBOMAI AI Engine
"""

import re
import json
import hashlib
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone

def generate_cache_key(*args: Any, **kwargs: Any) -> str:
    """Generate cache key from arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    key_str = "|".join(key_parts)
    return hashlib.sha256(key_str.encode()).hexdigest()

def parse_version(version: str) -> Tuple[List[int], str]:
    """Parse version string into components"""
    # Extract numeric parts and suffix
    parts = re.split(r'([0-9]+)', version)
    numbers = [int(p) for p in parts if p.isdigit()]
    suffix = ''.join(p for p in parts if not p.isdigit())
    return numbers, suffix

def compare_versions(version1: str, version2: str) -> int:
    """Compare two version strings"""
    v1_nums, v1_suffix = parse_version(version1)
    v2_nums, v2_suffix = parse_version(version2)
    
    # Compare numeric parts
    for n1, n2 in zip(v1_nums, v2_nums):
        if n1 < n2:
            return -1
        if n1 > n2:
            return 1
    
    # If numeric parts are equal, compare lengths
    if len(v1_nums) < len(v2_nums):
        return -1
    if len(v1_nums) > len(v2_nums):
        return 1
    
    # Compare suffixes
    if v1_suffix < v2_suffix:
        return -1
    if v1_suffix > v2_suffix:
        return 1
    
    return 0

def normalize_component_name(name: str) -> str:
    """Normalize component name for consistent comparison"""
    # Remove special characters and whitespace
    name = re.sub(r'[^a-zA-Z0-9]+', '-', name.lower())
    # Remove leading/trailing hyphens
    return name.strip('-')

def normalize_license(license_str: str) -> str:
    """Normalize license string"""
    # Remove whitespace and convert to uppercase
    license_str = re.sub(r'\s+', '', license_str.upper())
    # Handle common variations
    replacements = {
        'APACHE2': 'APACHE-2.0',
        'APACHE-2': 'APACHE-2.0',
        'MIT': 'MIT',
        'GPL2': 'GPL-2.0',
        'GPL3': 'GPL-3.0',
        'LGPL2': 'LGPL-2.1',
        'LGPL3': 'LGPL-3.0'
    }
    return replacements.get(license_str, license_str)

def parse_datetime(date_str: str) -> Optional[datetime]:
    """Parse datetime string in various formats"""
    formats = [
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    
    return None

def format_datetime(dt: datetime) -> str:
    """Format datetime in ISO format"""
    return dt.astimezone(timezone.utc).isoformat()

def calculate_checksum(content: str, algorithm: str = 'sha256') -> str:
    """Calculate checksum of content"""
    if algorithm == 'sha256':
        return hashlib.sha256(content.encode()).hexdigest()
    elif algorithm == 'md5':
        return hashlib.md5(content.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'

def extract_urls(text: str) -> List[str]:
    """Extract URLs from text"""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe filesystem usage"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Remove control characters
    filename = "".join(char for char in filename if ord(char) >= 32)
    return filename.strip()

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"

def parse_json_safe(json_str: str) -> Optional[Dict[str, Any]]:
    """Safely parse JSON string"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None

def format_duration(seconds: float) -> str:
    """Format duration in human readable format"""
    if seconds < 0.001:
        return f"{seconds*1000000:.0f}µs"
    elif seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds / 60)
        seconds = seconds % 60
        return f"{minutes}m {seconds:.1f}s" 