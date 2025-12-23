from dataclasses import dataclass
from typing import Callable, Optional, Dict, Any
from validators import (
    parse_text, parse_date_yyyy_mm_dd, parse_amount,
    validate_required, validate_date, validate_amount
)

@dataclass(frozen=True)
class FieldSpec:
    name: str
    label: str
    required: bool
    parser: Callable[[str], Any]
    validator: Callable[[Any, Dict[str, Any]], Optional[str]]
    hint: str = ""

FORM_TYPES = ["Leave Request", "Expense Claim"]

FORM_SPECS = {
    "Leave Request": {
        "employee_name": FieldSpec("employee_name", "Employee Name", True, parse_text, validate_required, "Full name"),
        "start_date": FieldSpec("start_date", "Start Date", True, parse_date_yyyy_mm_dd, validate_date, "YYYY-MM-DD"),
        "end_date": FieldSpec("end_date", "End Date", True, parse_date_yyyy_mm_dd, validate_date, "YYYY-MM-DD"),
        "reason": FieldSpec("reason", "Reason for Leave", True, parse_text, validate_required, "Short explanation"),
    },
    "Expense Claim": {
        "expense_date": FieldSpec("expense_date", "Expense Date", True, parse_date_yyyy_mm_dd, validate_date, "YYYY-MM-DD"),
        "amount": FieldSpec("amount", "Amount", True, parse_amount, validate_amount, "Numeric value"),
        "description": FieldSpec("description", "Description", True, parse_text, validate_required, "Expense details"),
    }
}
