import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from backend.app import create_app
from backend.utils import setup_logger

logger = setup_logger(__name__)

MODE = os.environ.get("MODE", "production")

app = create_app(MODE)

def main():
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting server on port {port}")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )

if __name__ == "__main__":
    main()
