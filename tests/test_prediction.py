"""
Test suite for prediction engine.

Tests model training, prediction, and comparison functionality.
"""

import unittest
import pandas as pd
import numpy as np
from backend.services.prediction import PredictionEngine, ModelComparison


class TestPredictionEngine(unittest.TestCase):
    """Test prediction engine functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Create sample dataset
        np.random.seed(42)
        n_samples = 100

        self.df = pd.DataFrame({
            'spending_normalized': np.random.uniform(0, 1, n_samples),
            'advance_payments': np.random.uniform(0, 20, n_samples),
            'current_balance': np.random.uniform(0, 10, n_samples),
            'credit_limit': np.random.uniform(0, 5, n_samples),
            'min_payment_amt': np.random.uniform(0, 5, n_samples),
            'max_spent_in_single_shopping': np.random.uniform(0, 10, n_samples),
            'spending_efficiency': np.random.uniform(0, 1, n_samples),
            'payment_discipline': np.random.uniform(0, 1, n_samples),
            'balance_utilization': np.random.uniform(0, 1, n_samples),
            'spending_consistency': np.random.uniform(0, 1, n_samples),
            'probability_of_full_payment': np.random.randint(0, 2, n_samples)
        })

        self.engine = PredictionEngine()

    def test_engine_initialization(self):
        """Test engine initialization."""
        self.assertIsNotNone(self.engine.comparison)
        self.assertIsNone(self.engine.best_model_name)

    def test_model_comparison(self):
        """Test model comparison tracking."""
        comparison = ModelComparison()

        # Add models
        model1_metrics = {'accuracy': 0.85, 'f1': 0.82}
        model2_metrics = {'accuracy': 0.88, 'f1': 0.86}

        comparison.add_model('model1', None, model1_metrics)
        comparison.add_model('model2', None, model2_metrics)

        # Check best model
        best_name, _ = comparison.get_best_model()
        self.assertEqual(best_name, 'model2')

    def test_evaluate_model(self):
        """Test model evaluation."""
        from sklearn.linear_model import LogisticRegression

        # Create simple model
        model = LogisticRegression(random_state=42)
        X = self.df[['spending_normalized', 'advance_payments', 'current_balance']]
        y = self.df['probability_of_full_payment']

        model.fit(X, y)

        # Evaluate
        metrics = self.engine._evaluate_model(model, X, y, 'Test Model')

        # Check metrics exist
        self.assertIn('accuracy', metrics)
        self.assertIn('precision', metrics)
        self.assertIn('recall', metrics)
        self.assertIn('f1', metrics)

        # Check metric ranges
        for key, value in metrics.items():
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 1)


if __name__ == '__main__':
    unittest.main()
