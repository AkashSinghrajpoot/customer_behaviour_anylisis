"""
Main application entry point.

Usage:
    python run.py develop   # Development mode
    python run.py produce   # Production mode
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from backend.app import create_app
from backend.utils import setup_logger
import pandas as pd
from backend.services import DataPreprocessor, PredictionEngine

logger = setup_logger(__name__)


def train_models():
    """Train ML models on available data."""
    try:
        logger.info("Loading training data...")
        df = pd.read_csv('data/bank_marketing_part1_Data.csv')

        logger.info(f"Dataset shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")

        # Preprocess training data
        preprocessor = DataPreprocessor()

        # Add engineering features for each row
        engineered_rows = []
        for idx, row in df.iterrows():
            data_dict = row.to_dict()
            processed = preprocessor.preprocess_customer_data(data_dict)
            engineered_rows.append(processed)

        processed_df = pd.DataFrame(engineered_rows)

        # Train models
        logger.info("Training prediction models...")
        engine = PredictionEngine()
        result = engine.train_models(processed_df)

        logger.info(f"Training complete: {result}")
        return True

    except FileNotFoundError:
        logger.warning("Training data not found. Models will use defaults.")
        return False
    except Exception as e:
        logger.error(f"Training failed: {str(e)}", exc_info=True)
        return False


def main():
    """Main entry point."""
    mode = sys.argv[1] if len(sys.argv) > 1 else 'develop'

    logger.info(f"Starting application in {mode} mode...")

    # Train models if not already present
    if not os.path.exists('backend/models/random_forest.pkl'):
        logger.info("Models not found. Training new models...")
        train_models()

    # Create and run app
    app = create_app(mode)

    if mode == 'develop':
        logger.info("Running in development mode on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        logger.info("Running in production mode on http://0.0.0.0:5000")
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)


if __name__ == '__main__':
    main()
