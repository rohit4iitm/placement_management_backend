from flask import Flask, jsonify
from models import db
from routes import api
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app)
jwt = JWTManager(app)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register routes
app.register_blueprint(api, url_prefix='/api')

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    logger.info("Database tables created")

# Error handling for 404 and 500 errors
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
