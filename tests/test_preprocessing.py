"""
Test suite for preprocessing module.

Tests data preprocessing, feature engineering, and metric generation.
"""

import unittest
import pandas as pd
from backend.services.preprocessing import DataPreprocessor


class TestPreprocessing(unittest.TestCase):
    """Test data preprocessing functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.preprocessor = DataPreprocessor()
        self.sample_data = {
            'spending': 19.94,
            'advance_payments': 16.92,
            'current_balance': 6.675,
            'credit_limit': 3.763,
            'min_payment_amt': 3.252,
            'max_spent_in_single_shopping': 6.55
        }

    def test_normalize_numeric_fields(self):
        """Test numeric normalization."""
        result = self.preprocessor._normalize_numeric_fields(self.sample_data)

        # Check normalized fields exist
        self.assertIn('spending_normalized', result)
        self.assertIn('advance_payments', result)

        # Check values are in valid range
        for key, value in result.items():
            if 'normalized' in key:
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 1)

    def test_engineer_features(self):
        """Test feature engineering."""
        normalized = self.preprocessor._normalize_numeric_fields(self.sample_data)
        engineered = self.preprocessor._engineer_features(normalized)

        # Check engineered features exist
        self.assertIn('spending_efficiency', engineered)
        self.assertIn('payment_discipline', engineered)
        self.assertIn('balance_utilization', engineered)
        self.assertIn('spending_consistency', engineered)

    def test_generate_business_metrics(self):
        """Test business metrics generation."""
        normalized = self.preprocessor._normalize_numeric_fields(self.sample_data)
        engineered = self.preprocessor._engineer_features(normalized)
        metrics = self.preprocessor._generate_business_metrics(engineered)

        # Check required metrics exist
        self.assertIn('engagement_score', metrics)
        self.assertIn('relationship_score', metrics)
        self.assertIn('customer_segment', metrics)
        self.assertIn('offer_priority', metrics)
        self.assertIn('customer_health', metrics)

        # Check score ranges
        self.assertGreaterEqual(metrics['engagement_score'], 0)
        self.assertLessEqual(metrics['engagement_score'], 100)
        self.assertGreaterEqual(metrics['relationship_score'], 0)
        self.assertLessEqual(metrics['relationship_score'], 100)

        # Check segment values
        valid_segments = ['Premium', 'Growth', 'At Risk', 'Dormant']
        self.assertIn(metrics['customer_segment'], valid_segments)

    def test_full_preprocessing_pipeline(self):
        """Test complete preprocessing pipeline."""
        result = self.preprocessor.preprocess_customer_data(self.sample_data)

        # Check all expected fields
        expected_fields = [
            'engagement_score', 'relationship_score', 'customer_segment',
            'offer_priority', 'customer_health'
        ]
        for field in expected_fields:
            self.assertIn(field, result)


if __name__ == '__main__':
    unittest.main()
