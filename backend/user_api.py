import db_manager
import api_api
import validator

from flask import Blueprint, request, session, jsonify
import bcrypt
import datetime
import requests
import threading
import traceback

def user_api_constructor(db):
    user_api = Blueprint("user_api", __name__)

    @user_api.route("/create", methods=['POST'])
    def create_user():
        user_data = request.json
        try:
            username = user_data['username']
            email = user_data['email']
            passw = user_data['password']
        except KeyError as e:
            traceback.print_exc()
            return "User form data invalid", 400 # Missing or invalid data format in request

        if (not validator.validate_email(email) or
            not validator.validate_password(passw) or
            not validator.validate_username(username)):
            return "Invalid credential format", 400 # Form data does not validate

        password = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())

        if not db.check_existing_user(email):
            db.create_user(username, email, password)
            return "", 200
        else:
            return "Email already exists", 409


    @user_api.route("/login", methods=['POST'])
    def login_user():
        user_data = request.json
        
        try:
            email = user_data['email']
            password = user_data['password']
        except Exception as e:
            traceback.print_exc()
            return "User form data invalid", 400 # Missing or invalid data format in request

        if (not validator.validate_email(email) or
            not validator.validate_password(password)):
            return "Invalid credential format", 400 # Form data does not validate

        user_id = db.check_credentials(email, password)

        if user_id:
            session['user_id'] = user_id
            session.permanent = True
            return session['user_id'], 200
        else:
            return "Wrong credentials", 401


    @user_api.route("/current", methods=['GET'])
    def get_current_user():
        if user_id := session.get('user_id'):
            if user_obj := db.get_user_fromid(user_id):
                timer_limit = user_obj["lastdbupdate"] + datetime.timedelta(minutes = 5)

                if timer_limit < datetime.datetime.now() and user_obj["zoezi_id"]:
                    #Replace request to match API for gym system(own config)
                    res = requests.get("https://ipstudenter.zoezi.se/api/workoutBooking/getEarlierForMember",
                                        params={"member"  : str(user_obj["zoezi_id"]),
                                                "session" : user_obj["zoezi_session"]})
                    zoezi_success = False
                    if res.status_code == 200:
                        zoezi_success = True
                        workouts = res.json()
                        workouts.reverse()

                        zoezi_thread = threading.Thread(target = db.zoezi_workouts_refresh, args = (user_id, workouts))
                        zoezi_thread.start()
                    else:
                        print("ERROR: User permissions for Workout Booking API not set")

                    if user_obj['fitbit_connected']:
                        fitbit_thread = threading.Thread(target = api_api.f_refresh_data_procedure, args = (db, user_id))
                        fitbit_thread.start()
                    
                    if user_obj['google_connected']:
                        google_thread = threading.Thread(target = api_api.g_refresh_data_procedure, args = (db, user_id))
                        google_thread.start()

                    db.update_time(user_id)
                    
                    if zoezi_success:
                        zoezi_thread.join()
                    if user_obj['fitbit_connected']:
                        fitbit_thread.join()
                    if user_obj['google_connected']:
                        google_thread.join()

                user_obj['is_connected_zoezi'] = user_obj["zoezi_id"] != ""

                del user_obj["lastdbupdate"]
                del user_obj['zoezi_id']
                del user_obj["zoezi_session"]

                return jsonify(user_obj), 200
            else:
                return f"User not found", 404 # Should not happen, broken database or modified session cookie
        else:
            return "Not logged in", 401


    @user_api.route("/logged_in", methods=['GET'])
    def logged_in():
        if user_id := session.get('user_id'):
            return "", 200
        else:
            return "", 401


    @user_api.route("/logout", methods=['POST'])
    def logout_user():
        if session.get('user_id'):
            session.clear()
            return "", 200
        else:
            return "Not logged in", 401


    @user_api.route("/removecurrent", methods=['DELETE'])
    def remove_user():
        if user_id := session.get('user_id'):
            if db.remove_user_by_id(user_id):
                session.clear()
                return "", 200
            else:
                return f"User not found", 404 # Should not happen, broken database or modified session cookie

        else:
            return "Not logged in", 401


    @user_api.route("/add_zoezi_id", methods=['POST'])
    def add_zoezi_id():
        if user_id := session.get('user_id'):
            try:
                zoezi_id = request.json['id']
                zoezi_session = request.json['session']
            except KeyError as e:
                return "Invalid data", 400

            if(db.add_zoezi_id(zoezi_id, zoezi_session, user_id)):
                add_workout_types_zoezi(db, zoezi_session, user_id)
                return "", 200
            else:
                return "Database update failed", 500


    @user_api.route("/get_user_steps", methods=['GET'])
    def get_user_steps():
        if user_id := session.get('user_id'):
            steps = db.get_user_steps(user_id)
            return steps

        else:
            return "Unauthorized", 401

    return user_api


def add_workout_types_zoezi(db, zoezi_session, user_id):
    """
        Fetches workout types from zoezi and inserts in database.

        Parameters:
        db (DBM): Global database manager object
        zoezi_session(str) : Logged-in zoezi session
        user_id (str) : MongoDB unique Object_ID

        Returns:
        None
        """
                    #Replace request to match API for gym system(own config)
    r = requests.get("https://ipstudenter.zoezi.se/api/schedule/workout/type/get/all", params={"session":zoezi_session})
    if r.status_code == 200:
        for obj in r.json():
            db.add_workout_type(user_id, (obj['name']))
