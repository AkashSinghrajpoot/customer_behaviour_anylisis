"""
Machine Learning prediction engine.

This module trains and manages both Logistic Regression and Random Forest models,
compares their performance, and automatically selects the best model for predictions.
"""

import pandas as pd
import numpy as np
import pickle
import os
import logging
from typing import Dict, Tuple, Any, Optional
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import json

logger = logging.getLogger(__name__)


class ModelComparison:
    """Stores and compares multiple model performances."""

    def __init__(self):
        """Initialize comparison tracker."""
        self.models = {}
        self.metrics = {}
        self.best_model_name = None
        self.best_score = 0

    def add_model(self, name: str, model: Any, metrics: Dict[str, float]) -> None:
        """
        Add a trained model and its metrics.

        Args:
            name: Model name
            model: Trained model object
            metrics: Performance metrics dictionary
        """
        self.models[name] = model
        self.metrics[name] = metrics

        # Track best model by F1 score
        f1 = metrics.get('f1', 0)
        if f1 > self.best_score:
            self.best_score = f1
            self.best_model_name = name
            logger.info(f"New best model: {name} (F1: {f1:.4f})")

    def get_best_model(self) -> Tuple[str, Any]:
        """
        Get the best performing model.

        Returns:
            Tuple of (model_name, model_object)
        """
        if self.best_model_name is None:
            raise ValueError("No models have been trained yet")
        return self.best_model_name, self.models[self.best_model_name]

    def get_comparison_report(self) -> Dict[str, Dict[str, float]]:
        """Get performance comparison across all models."""
        return self.metrics.copy()


class PredictionEngine:
    """Main prediction engine handling model training and inference."""

    def __init__(self, model_dir: str = 'backend/models'):
        """
        Initialize prediction engine.

        Args:
            model_dir: Directory to save/load models
        """
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.comparison = ModelComparison()
        self.feature_names = None
        self.target_name = 'probability_of_full_payment'

    def train_models(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict[str, Dict]:
        """
        Train and compare Logistic Regression and Random Forest models.

        Args:
            df: Training DataFrame
            test_size: Train-test split ratio

        Returns:
            Dictionary of training results
        """
        logger.info("Starting model training pipeline")

        # Prepare features and target
        feature_cols = [
            'spending_normalized', 'advance_payments',
            'current_balance', 'credit_limit',
            'min_payment_amt', 'max_spent_in_single_shopping',
            'spending_efficiency', 'payment_discipline',
            'balance_utilization', 'spending_consistency'
        ]

        # Filter to available columns
        available_cols = [col for col in feature_cols if col in df.columns]
        logger.info(f"Using {len(available_cols)} features: {available_cols}")

        X = df[available_cols].fillna(0)
        y = df[self.target_name].fillna(0)

        # Convert continuous target to binary classification using median threshold
        # This ensures we have both classes for training
        threshold = y.median()
        y = (y >= threshold).astype(int)
        logger.info(f"Converted continuous target to binary classes using threshold {threshold:.4f}. Distribution: {y.value_counts().to_dict()}")

        self.feature_names = available_cols

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        logger.info(f"Data split: {len(X_train)} train, {len(X_test)} test")

        # Train Logistic Regression
        logger.info("Training Logistic Regression...")
        lr_model = LogisticRegression(max_iter=1000, random_state=42)
        lr_model.fit(X_train, y_train)
        lr_metrics = self._evaluate_model(lr_model, X_test, y_test, 'Logistic Regression')
        self.comparison.add_model('logistic_regression', lr_model, lr_metrics)

        # Train Random Forest
        logger.info("Training Random Forest...")
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf_model.fit(X_train, y_train)
        rf_metrics = self._evaluate_model(rf_model, X_test, y_test, 'Random Forest')
        self.comparison.add_model('random_forest', rf_model, rf_metrics)

        # Save best model
        best_name, best_model = self.comparison.get_best_model()
        self._save_model(best_model, best_name)

        logger.info(f"Best model selected: {best_name}")

        return {
            'status': 'success',
            'best_model': best_name,
            'comparison': self.comparison.get_comparison_report()
        }

    def _evaluate_model(
        self,
        model: Any,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        model_name: str
    ) -> Dict[str, float]:
        """
        Evaluate model performance.

        Args:
            model: Trained model
            X_test: Test features
            y_test: Test target
            model_name: Model name for logging

        Returns:
            Dictionary of metrics
        """
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'auc': roc_auc_score(y_test, y_pred_proba)
        }

        logger.info(
            f"{model_name} - Accuracy: {metrics['accuracy']:.4f}, "
            f"F1: {metrics['f1']:.4f}, AUC: {metrics['auc']:.4f}"
        )

        return metrics

    def predict(self, features_dict: Dict[str, float]) -> Dict[str, Any]:
        """
        Make prediction on new customer data.

        Args:
            features_dict: Dictionary of feature values

        Returns:
            Prediction results including probability and confidence
        """
        best_name, best_model = self.comparison.get_best_model()

        # Prepare features in correct order
        feature_vector = np.array([
            features_dict.get(fname, 0) for fname in self.feature_names
        ]).reshape(1, -1)

        # Get prediction and probability
        prediction = best_model.predict(feature_vector)[0]
        probability = best_model.predict_proba(feature_vector)[0][1]

        result = {
            'prediction': int(prediction),
            'subscription_probability': float(probability * 100),
            'model_used': best_name,
            'confidence': 'High' if 0.7 <= probability <= 0.95 else
                        'Very High' if probability > 0.95 else
                        'Low'
        }

        logger.info(f"Prediction made: {result}")
        return result

    def _save_model(self, model: Any, name: str) -> None:
        """
        Save model to disk.

        Args:
            model: Model to save
            name: Model name
        """
        model_path = os.path.join(self.model_dir, f'{name}.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Model saved to {model_path}")

    def load_model(self, name: str) -> Any:
        """
        Load model from disk.

        Args:
            name: Model name

        Returns:
            Loaded model
        """
        model_path = os.path.join(self.model_dir, f'{name}.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Model loaded from {model_path}")
        return model
