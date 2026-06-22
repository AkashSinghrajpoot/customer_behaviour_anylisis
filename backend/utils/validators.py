"""
Input validation module for customer data.

This module provides comprehensive validation for customer input data,
ensuring data quality before processing and prediction.
"""

from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_numeric_range(
    value: float,
    field_name: str,
    min_val: float = 0,
    max_val: float = float('inf')
) -> Tuple[bool, str]:
    """
    Validate numeric field is within acceptable range.

    Args:
        value: Value to validate
        field_name: Field name for error messages
        min_val: Minimum acceptable value
        max_val: Maximum acceptable value

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        val = float(value)
        if val < min_val or val > max_val:
            return False, f"{field_name} must be between {min_val} and {max_val}"
        return True, ""
    except (TypeError, ValueError):
        return False, f"{field_name} must be a number"


def validate_non_negative(value: float, field_name: str) -> Tuple[bool, str]:
    """Validate value is non-negative."""
    return validate_numeric_range(value, field_name, 0)


def validate_customer_input(data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate complete customer input data.

    Args:
        data: Dictionary containing customer data

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Check for missing required fields
    required_fields = [
        'spending', 'advance_payments', 'current_balance',
        'credit_limit', 'min_payment_amt', 'max_spent_in_single_shopping'
    ]

    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            errors.append(f"Missing required field: {field}")

    if errors:
        return False, errors

    # Validate numeric ranges
    validations = [
        (data.get('spending'), 'Spending', 0, 1000),
        (data.get('advance_payments'), 'Advance Payments', 0, 1000),
        (data.get('current_balance'), 'Current Balance', 0, 100),
        (data.get('credit_limit'), 'Credit Limit', 0, 100),
        (data.get('min_payment_amt'), 'Min Payment Amount', 0, 50),
        (data.get('max_spent_in_single_shopping'), 'Max Spent in Single Shopping', 0, 100),
    ]

    for value, field_name, min_val, max_val in validations:
        valid, error = validate_numeric_range(value, field_name, min_val, max_val)
        if not valid:
            errors.append(error)

    return len(errors) == 0, errors
