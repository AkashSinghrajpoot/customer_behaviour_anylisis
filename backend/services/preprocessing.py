"""
Data preprocessing and feature engineering module.

This module handles data cleaning, normalization, feature engineering,
and generation of derived metrics (engagement_score, relationship_score, etc.).
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Any
import logging
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Handles all data preprocessing and feature engineering tasks."""

    def __init__(self):
        """Initialize the preprocessor."""
        self.scaler = StandardScaler()
        self.numeric_features = [
            'spending', 'advance_payments', 'current_balance',
            'credit_limit', 'min_payment_amt', 'max_spent_in_single_shopping'
        ]
        self.feature_ranges = None

    def preprocess_customer_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess a single customer's data for prediction.

        Args:
            data: Raw customer input data

        Returns:
            Preprocessed data with engineered features
        """
        logger.info(f"Preprocessing customer data")

        # Create a copy to avoid modifying original
        processed_data = data.copy()

        # Normalize numeric fields
        processed_data = self._normalize_numeric_fields(processed_data)

        # Engineer new features
        processed_data = self._engineer_features(processed_data)

        # Generate business metrics
        business_metrics = self._generate_business_metrics(processed_data)
        processed_data.update(business_metrics)

        logger.info(f"Preprocessing complete. Generated metrics: {list(business_metrics.keys())}")
        return processed_data

    def _normalize_numeric_fields(self, data: Dict) -> Dict:
        """
        Normalize numeric fields to 0-1 range.

        Args:
            data: Input data dictionary

        Returns:
            Data with normalized numeric fields
        """
        normalized_data = data.copy()

        # Define normalization ranges based on data characteristics
        normalization_map = {
            'spending': (0, 1000),
            'advance_payments': (0, 1000),
            'current_balance': (0, 100),
            'credit_limit': (0, 100),
            'min_payment_amt': (0, 50),
            'max_spent_in_single_shopping': (0, 100),
        }

        for field, (min_val, max_val) in normalization_map.items():
            if field in normalized_data:
                value = float(normalized_data[field])
                normalized_value = (value - min_val) / (max_val - min_val)
                normalized_value = max(0, min(1, normalized_value))  # Clip to [0, 1]
                normalized_data[f'{field}_normalized'] = normalized_value

        return normalized_data

    def _engineer_features(self, data: Dict) -> Dict:
        """
        Engineer derived features from raw data.

        Args:
            data: Preprocessed data

        Returns:
            Data with engineered features
        """
        engineered_data = data.copy()

        # Spending Efficiency Ratio (spending / credit_limit)
        spending = float(data.get('spending', 0))
        credit_limit = float(data.get('credit_limit', 1))
        engineered_data['spending_efficiency'] = spending / credit_limit if credit_limit > 0 else 0

        # Payment Discipline (min_payment_amt / spending)
        min_payment = float(data.get('min_payment_amt', 0))
        engineered_data['payment_discipline'] = min_payment / spending if spending > 0 else 0

        # Balance Utilization (current_balance / credit_limit)
        current_balance = float(data.get('current_balance', 0))
        engineered_data['balance_utilization'] = current_balance / credit_limit if credit_limit > 0 else 0

        # Spending Variability (max_spent / avg_spent proxy)
        max_spent = float(data.get('max_spent_in_single_shopping', 0))
        engineered_data['spending_consistency'] = 1 - (max_spent / spending if spending > 0 else 1)

        return engineered_data

    def _generate_business_metrics(self, data: Dict) -> Dict[str, Any]:
        """
        Generate business-relevant metrics for recommendations.

        Args:
            data: Processed customer data

        Returns:
            Dictionary of business metrics
        """
        metrics = {}

        # Engagement Score (0-100)
        # Based on spending and payment behavior
        spending_norm = data.get('spending_normalized', 0)
        payment_discipline = data.get('payment_discipline', 0)
        spending_consistency = data.get('spending_consistency', 0)

        engagement_score = (
            (spending_norm * 0.4) +
            (payment_discipline * 0.3) +
            (spending_consistency * 0.3)
        ) * 100
        metrics['engagement_score'] = min(100, max(0, engagement_score))

        # Relationship Score (0-100)
        # Based on balance utilization and spending efficiency
        balance_util = data.get('balance_utilization', 0)
        spending_eff = data.get('spending_efficiency', 0)

        relationship_score = (
            (balance_util * 0.5) +
            (spending_eff * 0.5)
        ) * 100
        metrics['relationship_score'] = min(100, max(0, relationship_score))

        # Customer Segment classification
        engagement = metrics['engagement_score']
        relationship = metrics['relationship_score']

        if engagement >= 70 and relationship >= 70:
            metrics['customer_segment'] = 'Premium'
        elif engagement >= 50 and relationship >= 50:
            metrics['customer_segment'] = 'Growth'
        elif engagement >= 30 or relationship >= 30:
            metrics['customer_segment'] = 'At Risk'
        else:
            metrics['customer_segment'] = 'Dormant'

        # Offer Priority (1-5 scale)
        priority = (engagement + relationship) / 200  # 0-1 scale
        metrics['offer_priority'] = max(1, min(5, int(priority * 5) + 1))

        # Customer Health (0-100)
        # Composite of all positive metrics
        health = (engagement * 0.4 + relationship * 0.6)
        metrics['customer_health'] = min(100, max(0, health))

        return metrics

    def fit(self, df: pd.DataFrame) -> None:
        """
        Fit scaler on training data.

        Args:
            df: Training DataFrame
        """
        numeric_cols = [col for col in df.columns if col in self.numeric_features]
        if numeric_cols:
            self.scaler.fit(df[numeric_cols])
            logger.info(f"Scaler fitted on {len(numeric_cols)} numeric features")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform DataFrame using fitted scaler.

        Args:
            df: DataFrame to transform

        Returns:
            Transformed DataFrame
        """
        df_copy = df.copy()
        numeric_cols = [col for col in df_copy.columns if col in self.numeric_features]
        if numeric_cols:
            df_copy[numeric_cols] = self.scaler.transform(df_copy[numeric_cols])
        return df_copy
