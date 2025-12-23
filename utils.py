# utils.py
import json
from typing import Any, Dict

def normalize_for_export(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert all non-serializable objects in form data to strings.
    Ensures JSON export works without errors.
    """
    normalized = {}
    for key, value in data.items():
        try:
            json.dumps({key: value})  # Test if serializable
            normalized[key] = value
        except (TypeError, OverflowError):
            normalized[key] = str(value)
    return normalized

def json_dumps_safe(data: Any, indent: int = 2) -> str:
    """
    Safely dump data to JSON string.
    Handles non-serializable objects.
    """
    try:
        return json.dumps(data, indent=indent)
    except (TypeError, OverflowError):
        # Fallback: convert non-serializable values to string
        def convert(obj):
            try:
                json.dumps(obj)
                return obj
            except (TypeError, OverflowError):
                return str(obj)
        if isinstance(data, dict):
            safe_data = {k: convert(v) for k, v in data.items()}
        elif isinstance(data, list):
            safe_data = [convert(v) for v in data]
        else:
            safe_data = str(data)
        return json.dumps(safe_data, indent=indent)
