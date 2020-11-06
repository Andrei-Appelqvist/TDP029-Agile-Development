import api_api
import db_manager

from flask import Blueprint, request, session, jsonify
import bcrypt
import bson
import traceback

def workout_api_constructor(db):
    workout_api = Blueprint("workout_api", __name__)
        
    @workout_api.route("/get_workouts", methods=['GET'])
    def get_workouts():
        if user_id := session.get('user_id'):
            year = request.args.get("year")
            week = request.args.get("week")
            wk = db.get_week_workouts(year, week, user_id)
            return jsonify(wk)
        else:
            return "Unauthorized", 401
    
    
    @workout_api.route("/add_workout", methods=['POST'])
    def add_workout():
        if user_id := session.get('user_id'):
            workout = request.json
            try:
                db.create_manual_workout(user_id, workout)
            except KeyError as e:
                traceback.print_exc()
                return "Missing required values", 400
        else:
            return "Unauthorized", 401

        return "", 200


    @workout_api.route("/add_workout_type", methods=['POST'])
    def add_workout_type():
        if user_id := session.get('user_id'):
            workout_type = request.json['workout_type']
            try:
                db.add_workout_type(user_id, workout_type)
            except KeyError as e:
                traceback.print_exc()
                return "Missing required values", 400
        else:
            return "Unauthorized", 401

        return "", 200


    @workout_api.route("/get_workout_types", methods=['GET'])
    def get_workout_types():
        if user_id := session.get('user_id'):
            types = db.get_workout_types(user_id)
        else:
            return "Unauthorized", 401

        return jsonify(types), 200


    @workout_api.route("/get_week_stats", methods=['GET'])
    def get_week_stats():
        if user_id := session.get('user_id'):
            year = request.args.get("year")
            week = request.args.get("week")
            stats = db.get_week_stats(year, week, user_id)
        else:
            return "Unauthorized", 401
        
        return jsonify(stats), 200


    return workout_api