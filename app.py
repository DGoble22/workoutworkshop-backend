from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.coach_routes import coach_bp
from routes.user_routes import user_bp
from routes.workout_routes import workout_bp
from dotenv import load_dotenv
import os
from routes.chat import register_chat_events
from flask_socketio import SocketIO
from flasgger import Swagger

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*")
Swagger(app)

database_url = os.getenv('DATABASE_URL')
if not database_url:
    print("No DATABASE_URL found. Falling back to in-memory SQLite for testing.")
    database_url = 'sqlite:///:memory:'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'change-me-in-production')

if "sqlite" not in database_url:
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 280,
        "pool_pre_ping": True
    }

db = SQLAlchemy(app)

app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(coach_bp)
app.register_blueprint(user_bp)
app.register_blueprint(workout_bp)

register_chat_events(socketio, app)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host='localhost')
