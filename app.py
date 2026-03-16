from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.coach_routes import coach_bp
from routes.user_routes import user_bp
from dotenv import load_dotenv
import os
app = Flask(__name__)
CORS(app)

# DB Config
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'

db = SQLAlchemy(app)

app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(coach_bp)
app.register_blueprint(user_bp)

@app.route('/test-db')
def test_db():
    try:
        # We use db.text() to run a raw SQL 'ping'
        result = db.session.execute(db.text("SELECT 1")).fetchone()
        return jsonify({
            "status": "success",
            "message": "Flask is talking to MySQL!",
            "result": result[0]
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Get all coach data
@app.route('/coach-data', methods=['GET'])
def get_coach_data():
    try:
        # Main Query to get coach data
        query = """SELECT c_p.coach_id, u.user_id, u_p.first_name, u_p.last_name, c_b.bio, c_p.is_nutritionist, c_p.is_active, c_p.pricing FROM coach_profiles as c_p
        JOIN coach_bios as c_b ON c_p.bio_id = c_b.bio_id
        JOIN users AS u ON c_p.user_id = u.user_id
        JOIN user_profiles AS u_p ON u.user_ID = u_p.user_id"""
        coaches = db.session.execute(db.text(query)).fetchall()
        coach_list = [{"Coach ID": c[0], "User ID": c[1], "First Name": c[2], "Last Name": c[3], "bio": c[4], "is_nutritionist": c[5], "is_active": c[6], "pricing": c[7]} for c in coaches]
        return jsonify({
            "status": "success",
            "data": coach_list
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
# Get one coach data
@app.route('/coach-data/<int:coach_id>', methods=['GET'])
def get_one_coach_data(coach_id):
    try:
        # Main Query to get a single coach data
        query = """SELECT c_p.coach_id, u.user_id, u_p.first_name, u_p.last_name, c_b.bio, c_p.is_nutritionist, c_p.is_active, c_p.pricing FROM coach_profiles as c_p
        JOIN coach_bios as c_b ON c_p.bio_id = c_b.bio_id
        JOIN users AS u ON c_p.user_id = u.user_id
        JOIN user_profiles AS u_p ON u.user_ID = u_p.user_id
        WHERE c_p.coach_id = :coach_id"""
        coach = db.session.execute(db.text(query), {"coach_id": coach_id}).fetchone()
        if coach:
            coach_data = {"Coach ID": coach[0], "User ID": coach[1], "First Name": coach[2], "Last Name": coach[3], "bio": coach[4], "is_nutritionist": coach[5], "is_active": coach[6], "pricing": coach[7]}
            return jsonify({
                "status": "success",
                "data": coach_data
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Coach not found"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='localhost')
