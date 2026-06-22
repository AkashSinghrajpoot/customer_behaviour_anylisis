"""
Test suite for validation module.

Tests input validation, error handling, and edge cases.
"""

import unittest
from backend.utils.validators import validate_customer_input, validate_numeric_range


class TestValidation(unittest.TestCase):
    """Test validation functions."""

    def test_valid_customer_input(self):
        """Test valid customer input."""
        data = {
            'spending': 19.94,
            'advance_payments': 16.92,
            'current_balance': 6.675,
            'credit_limit': 3.763,
            'min_payment_amt': 3.252,
            'max_spent_in_single_shopping': 6.55
        }
        is_valid, errors = validate_customer_input(data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_missing_fields(self):
        """Test missing required fields."""
        data = {
            'spending': 19.94,
            'advance_payments': 16.92
        }
        is_valid, errors = validate_customer_input(data)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)

    def test_negative_values(self):
        """Test negative input values."""
        data = {
            'spending': -19.94,
            'advance_payments': 16.92,
            'current_balance': 6.675,
            'credit_limit': 3.763,
            'min_payment_amt': 3.252,
            'max_spent_in_single_shopping': 6.55
        }
        is_valid, errors = validate_customer_input(data)
        self.assertFalse(is_valid)

    def test_numeric_range_validation(self):
        """Test numeric range validation."""
        valid, msg = validate_numeric_range(50, 'Age', 0, 100)
        self.assertTrue(valid)

        valid, msg = validate_numeric_range(150, 'Age', 0, 100)
        self.assertFalse(valid)

    def test_invalid_numeric_type(self):
        """Test invalid numeric types."""
        valid, msg = validate_numeric_range('abc', 'Amount', 0, 100)
        self.assertFalse(valid)
        self.assertIn('must be a number', msg)


if __name__ == '__main__':
    unittest.main()
