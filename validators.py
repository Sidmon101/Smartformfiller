# validators.py
import re
from datetime import datetime, date
from typing import Any, Optional, Dict

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
EMP_RE = re.compile(r"^(EMP\d{4,6}|\d{6,10})$")

def parse_text(s: str) -> str:
    return s.strip()

def parse_email(s: str) -> str:
    return s.strip()

def parse_date_yyyy_mm_dd(s: str) -> date:
    s = s.strip()
    return datetime.strptime(s, "%Y-%m-%d").date()

def parse_amount(s: str) -> float:
    s = s.strip().replace(",", "")
    return float(s)

def parse_yes_no(s: str) -> str:
    s = s.strip().lower()
    if s in ("yes", "y", "true", "1"):
        return "yes"
    if s in ("no", "n", "false", "0"):
        return "no"
    return s

def validate_required(value: Any, _: Dict[str, Any]) -> Optional[str]:
    if value is None:
        return "This field is required."
    if isinstance(value, str) and not value.strip():
        return "This field is required."
    return None

def validate_email(value: Any, _: Dict[str, Any]) -> Optional[str]:
    if value is None:
        return "Email is required."
    if not isinstance(value, str) or not EMAIL_RE.match(value.strip()):
        return "Please enter a valid email address."
    return None

def validate_employee_id(value: Any, _: Dict[str, Any]) -> Optional[str]:
    if value is None:
        return "Employee ID is required."
    if not isinstance(value, str) or not EMP_RE.match(value.strip()):
        return "Employee ID must look like EMP1234 or 6+ digits."
    return None

def validate_date(value: Any, _: Dict[str, Any]) -> Optional[str]:
    if value is None:
        return "Date is required."
    if not isinstance(value, date):
        return "Please use YYYY-MM-DD format."
    return None

def validate_amount(value: Any, _: Dict[str, Any]) -> Optional[str]:
    if value is None:
        return "Amount is required."
    try:
        v = float(value)
    except Exception:
        return "Amount must be a number."
    if v <= 0:
        return "Amount must be greater than 0."
    return None

def validate_yes_no(value: Any, _: Dict[str, Any]) -> Optional[str]:
    if value is None:
        return "This field is required."
    if not isinstance(value, str) or value not in ("yes", "no"):
        return "Please answer yes or no."
    return None

def validate_date_range(start_key: str, end_key: str):
    def _validator(_: Any, data: Dict[str, Any]) -> Optional[str]:
        s = data.get(start_key)
        e = data.get(end_key)
        if s is None or e is None:
            return None
        if e < s:
            return f"{end_key} cannot be earlier than {start_key}."
        return None
    return _validator
