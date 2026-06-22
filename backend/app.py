"""
Main Flask application for Customer Relationship Analytics Dashboard.

Initializes the Flask app, configures CORS, registers blueprints, and sets up logging.
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import logging
import os
from backend.utils import setup_logger
from backend.routes import predict_bp

# Setup logging
logger = setup_logger(__name__, 'logs/app.log')


def create_app(config: str = 'production') -> Flask:
    """
    Application factory function.

    Args:
        config: Configuration mode ('development' or 'production')

    Returns:
        Configured Flask application instance
    """
    # Get project root (go up one level from backend/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_folder = os.path.join(project_root, 'frontend', 'templates')
    static_folder = os.path.join(project_root, 'frontend', 'static')
    
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    # Configure application
    app.config['JSON_SORT_KEYS'] = False
    if config == 'development':
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
        logger.setLevel(logging.DEBUG)
    else:
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        logger.setLevel(logging.INFO)

    # Enable CORS
    CORS(app)
    logger.info("CORS enabled for all routes")

    # Register blueprints
    app.register_blueprint(predict_bp)
    logger.info("Blueprints registered")

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found', 'message': str(e)}), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.error(f"Server error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

    # Routes
    @app.route('/')
    def index():
        """Serve dashboard homepage."""
        return render_template('dashboard.html')

    @app.route('/api/status')
    def status():
        """Return application status."""
        return jsonify({
            'status': 'running',
            'version': '1.0.0',
            'environment': config
        }), 200

    logger.info(f"Flask app created in {config} mode")
    return app


if __name__ == '__main__':
    app = create_app('development')
    logger.info("Starting Flask development server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
