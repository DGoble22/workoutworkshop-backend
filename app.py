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

# DB Config
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT', '24183')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'change-me-in-production')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 280,   # Refresh connections every 280 seconds
    "pool_pre_ping": True  # Test connection health before sending queries
}

db = SQLAlchemy(app)

app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(coach_bp)
app.register_blueprint(user_bp)
app.register_blueprint(workout_bp)

register_chat_events(socketio, app)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='https://workoutworkshop-backend.onrender.com')