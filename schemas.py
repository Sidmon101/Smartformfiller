# schemas.py

from validators import (
    validate_required,
    validate_date,
    validate_date_range,
    validate_yes_no,
    validate_amount,
    parse_date_yyyy_mm_dd,
    parse_text,
    parse_amount,
    parse_yes_no,
)

FORM_TYPES = {
    "Leave Request": {
        "title": "Leave Request",
        "fields": {
            "employee_name": {
                "question": "What is your full name?",
                "parser": parse_text,
                "validators": [validate_required],
            },
            "start_date": {
                "question": "Start date of leave (YYYY-MM-DD)",
                "parser": parse_date_yyyy_mm_dd,
                "validators": [validate_required, validate_date],
            },
            "end_date": {
                "question": "End date of leave (YYYY-MM-DD)",
                "parser": parse_date_yyyy_mm_dd,
                "validators": [
                    validate_required,
                    validate_date,
                    validate_date_range("start_date", "end_date"),
                ],
            },
            "is_paid_leave": {
                "question": "Is this a paid leave? (yes/no)",
                "parser": parse_yes_no,
                "validators": [validate_yes_no],
            },
        },
    },

    "Expense Claim": {
        "title": "Expense Claim",
        "fields": {
            "employee_id": {
                "question": "Enter your employee ID",
                "parser": parse_text,
                "validators": [validate_required],
            },
            "expense_date": {
                "question": "Expense date (YYYY-MM-DD)",
                "parser": parse_date_yyyy_mm_dd,
                "validators": [validate_required, validate_date],
            },
            "amount": {
                "question": "Expense amount",
                "parser": parse_amount,
                "validators": [validate_required, validate_amount],
            },
            "description": {
                "question": "Expense description",
                "parser": parse_text,
                "validators": [validate_required],
            },
        },
    },
}
