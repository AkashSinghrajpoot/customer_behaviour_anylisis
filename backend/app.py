from flask import Flask, render_template, jsonify
from flask_cors import CORS
import logging
import os
from backend.utils import setup_logger
from backend.routes import predict_bp

os.makedirs("logs", exist_ok=True)
logger = setup_logger(__name__, "logs/app.log")

def create_app(config="production"):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    app = Flask(
        __name__,
        template_folder=os.path.join(root,"frontend","templates"),
        static_folder=os.path.join(root,"frontend","static")
    )

    app.config["JSON_SORT_KEYS"] = False

    if config in ["development","develop"]:
        app.config["DEBUG"] = True
        logger.setLevel(logging.DEBUG)

    CORS(app)

    app.register_blueprint(predict_bp)

    @app.route("/")
    def index():
        return render_template("dashboard.html")

    @app.route("/api/status")
    def status():
        return jsonify(
            status="running",
            environment=config
        )

    return app
