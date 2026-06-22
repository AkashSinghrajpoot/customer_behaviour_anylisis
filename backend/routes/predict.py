"""
Prediction API routes.

Handles HTTP endpoints for customer prediction and recommendation generation.
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Tuple, Any
import logging

logger = logging.getLogger(__name__)

# Create blueprint
predict_bp = Blueprint('predict', __name__, url_prefix='/api')


@predict_bp.route('/predict', methods=['POST'])
def predict_customer() -> Tuple[Dict[str, Any], int]:
    """
    Main prediction endpoint.

    Accepts customer data, validates, preprocesses, predicts, and generates recommendations.

    Expected JSON:
    {
        "spending": 19.94,
        "advance_payments": 16.92,
        "current_balance": 6.675,
        "credit_limit": 3.763,
        "min_payment_amt": 3.252,
        "max_spent_in_single_shopping": 6.55
    }

    Returns:
        JSON response with predictions and recommendations
    """
    from backend.utils import validate_customer_input
    from backend.services import DataPreprocessor, PredictionEngine, RecommendationEngine

    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        logger.info(f"Received prediction request: {data}")

        # Validate input
        is_valid, errors = validate_customer_input(data)
        if not is_valid:
            logger.warning(f"Validation failed: {errors}")
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        # Preprocess data
        preprocessor = DataPreprocessor()
        processed_data = preprocessor.preprocess_customer_data(data)

        # Make prediction
        engine = PredictionEngine()
        try:
            engine.comparison.best_model_name = 'random_forest'
            engine.comparison.models['random_forest'] = engine.load_model('random_forest')
            engine.feature_names = [
                'spending_normalized', 'advance_payments',
                'current_balance', 'credit_limit',
                'min_payment_amt', 'max_spent_in_single_shopping',
                'spending_efficiency', 'payment_discipline',
                'balance_utilization', 'spending_consistency'
            ]
        except FileNotFoundError:
            logger.warning("Trained models not found. Using default predictions.")
            # Use preprocessed metrics as fallback
            prediction_results = {
                'prediction': 1 if processed_data['engagement_score'] > 50 else 0,
                'subscription_probability': processed_data['engagement_score'],
                'model_used': 'fallback'
            }
        else:
            prediction_results = engine.predict(processed_data)

        # Generate recommendations
        recommender = RecommendationEngine()
        recommendations = recommender.generate_recommendations(processed_data, prediction_results)

        # Compile response
        response = {
            'status': 'success',
            'customer_metrics': {
                'engagement_score': processed_data['engagement_score'],
                'relationship_score': processed_data['relationship_score'],
                'customer_segment': processed_data['customer_segment'],
                'customer_health': processed_data['customer_health'],
                'offer_priority': processed_data['offer_priority']
            },
            'prediction': {
                'subscription_probability': prediction_results['subscription_probability'],
                'confidence': prediction_results.get('confidence', 'Medium')
            },
            'recommendation': {
                'primary_action': recommendations['primary_action'],
                'secondary_actions': recommendations['secondary_actions'],
                'priority_level': recommendations['priority_level'],
                'reasoning': recommendations['reasoning'],
                'next_steps': recommendations['next_steps']
            }
        }

        logger.info(f"Prediction successful. Probability: {prediction_results['subscription_probability']:.2f}%")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@predict_bp.route('/health', methods=['GET'])
def health_check() -> Tuple[Dict[str, str], int]:
    """
    Health check endpoint.

    Returns:
        Status and timestamp
    """
    from datetime import datetime
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200
