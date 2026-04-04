from flask import Blueprint, jsonify, current_app, request
from sqlalchemy import text

workout_bp = Blueprint('workout', __name__, url_prefix='/api/workouts')

@workout_bp.route('/exercises', methods=['GET'])
def get_exercises():
    db = current_app.extensions['sqlalchemy']

    try:
        #Grab all exercises that are available
        query = text("""
                     SELECT exercise_id, name, muscle_group, equipment_needed, video_url
                     FROM exercises 
                     WHERE is_removed = 0
                     """)

        result = db.session.execute(query).mappings().fetchall()

        # Convert result to list of dicts
        exercises = [dict(row) for row in result]

        return jsonify({'status': 'success', 'data': exercises}), 200

    except Exception as e:
        print("DATABASE ERROR:", str(e))
        return jsonify({'status': 'error', 'message': 'Failed to fetch exercises'}), 500

@workout_bp.route('/daily-plan/<int:user_id>/<DOW>', methods=['GET'])
def get_daily_plan(user_id, DOW):
    db = current_app.extensions['sqlalchemy']
    dayofweek=str(DOW)
    print(DOW)
    try:
        #Grab all exercises that are available
        query = text("""
                    select wp.plan_id, pe.exercise_id, e.name, e.video_url, e.equipment_needed, pe.sets, pe.reps, pe.weight from workout_plans wp
                    join plan_exercise pe
                    on wp.plan_id = pe.plan_id
                    join exercises e
                    on e.exercise_id = pe.exercise_id 
                    where wp.user_id = :user_id and wp.planned_date like :DOW
                    group by pe.plan_exercise_id;
                     """)

        result = db.session.execute(query, {"user_id": user_id, "DOW": dayofweek}).mappings().fetchall()

        # Convert result to list of dicts
        exercises = [dict(row) for row in result]

        return jsonify({'status': 'success', 'data': exercises}), 200

    except Exception as e:
        print("DATABASE ERROR:", str(e))
        return jsonify({'status': 'error', 'message': 'Failed to fetch exercises'}), 500


@workout_bp.route('/save', methods=['POST'])
def save_workout():
    db = current_app.extensions['sqlalchemy']

    #Get data from Payload
    data = request.get_json()

    user_id = data.get('user_id')
    planned_date = data.get('date')
    workout_name = data.get('workout_name')
    exercises = data.get('exercises', [])

    # Validates all fields are in the payload
    if not all([user_id, planned_date, exercises]):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    try:
        #Insert plan into workout_plans
        insert_plan_query = text("""
                                INSERT INTO workout_plans (user_id, planned_date, title)
                                VALUES (:user_id, :planned_date, :title)
                                """)

        result = db.session.execute(insert_plan_query, {
            "user_id": user_id,
            "planned_date": planned_date,
            "title": workout_name
        })

        # get plan_id
        plan_id = result.lastrowid

        # Insert into plan_exercise for each exercise in the workout
        insert_exercise_query = text("""
                                    INSERT INTO plan_exercise (plan_id, exercise_id, sets, reps, weight)
                                    VALUES (:plan_id, :exercise_id, :sets, :reps, :weight)
                                    """)

        for exercise in exercises:
            db.session.execute(insert_exercise_query, {
                "plan_id": plan_id,
                "exercise_id": exercise['exercise_id'],
                "sets": 0,
                "reps": 0,
                "weight": 0
            })

        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Workout saved successfully!'}), 201

    except Exception as e:
        db.session.rollback()
        print("DATABASE ERROR:", str(e))
        return jsonify({'status': 'error', 'message': 'Failed to save workout'}), 500

@workout_bp.route('/remove', methods=["POST"])
def remove_workout_from_plan():
    payload = request.get_json(silent=True) or {}

    try:
        plan_id = payload.get('plan_id')
        exercise_id = payload.get('exercise_id')

        if not all([plan_id, exercise_id]):
            return jsonify({
                'status':  'error',
                'message': 'failed to recieve plan_id or exercise_id'
            }), 400

        db  = current_app.extensions['sqlalchemy']
        session = db.session

        session.execute(
            text(
                'delete from plan_exercise where plan_id=:plan_id and exercise_id=:exercise_id'
            ),
                {'plan_id': plan_id, 'exercise_id': exercise_id}
        )

        session.commit()

        return jsonify({"message":"Exercise Removed"}), 200
        
    except:
        return jsonify({"message":"Error Removing Exercise"}), 400

@workout_bp.route('/add-workout', methods=["POST"])
def add_workout_to_plan():
    payload = request.get_json(silent=True) or {}
    
    try:
        planned_date = payload.get("planned_date")
        user_id = payload.get("user_id")
        exercise_id = payload.get("exercise_id")

        if not all([planned_date, user_id, exercise_id]):
            return jsonify({
                'status':  'error',
                'message': 'failed to recieve date or exercise_id or user_id'
            }), 400

        db  = current_app.extensions['sqlalchemy']
        session = db.session

        # check if user has a plan alrady made for that date
        query= text("""
            select * from workout_plans 
            where user_id = :user_id and planned_date like :planned_date
            """)

        result = db.session.execute(query, {"user_id": user_id, "planned_date": planned_date}).mappings().fetchall()
        if(len(result)>0):
            print("1")
            plan_id = result[0]["plan_id"]
        else:
            print("2")
            query = text("""
                insert into workout_plans (user_id, title, planned_date)
                values (:user_id, :title, :planned_date)
                """)
            result = db.session.execute(query, {"user_id":user_id, "title":planned_date, "planned_date":planned_date})
            session.commit()
            plan_id = result.lastrowid #get the id of the new row

        print("3")
        db.session.execute(
            text("""
                insert into plan_exercise (plan_id, exercise_id)
                values (:plan_id, :exercise_id)
                """),

            {"plan_id":plan_id, "exercise_id":exercise_id}
        )

        print("4")
        session.commit()
        return jsonify({"message":"Exercise Adeed"}), 200
    
    except:
        return jsonify({"message":"Error Adding Exercise"}), 403

        


