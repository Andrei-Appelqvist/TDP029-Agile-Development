import db_manager

from flask import Blueprint, request, session, jsonify
import requests
import json
import datetime
import traceback

def api_api_constructor(db):
    api_api = Blueprint("api_api", __name__)

    @api_api.route("/authorize_fitbit", methods=['POST'])
    def authorize_fitbit():
        if user_id := session.get('user_id'):
            if code := request.args.get('code'):
                if refresh_token := f_get_refresh_token(code):
                    db.add_fitbit_refresh(refresh_token,user_id)
                    if result := f_get_data(db, refresh_token, user_id):
                        db.fitbit_steps_refresh(user_id, result)
                        return "", 200
                    else:
                        return "Failed to fetch Fitbit steps", 500 # should not happen
                else:
                    return "Failed to fetch Fitbit refresh token", 500 # should not happen
            else:
                return "Invalid params", 400 # Missing Fitbit auth code, this route should only be called from Fitbit auth servers
        else:
            return "Not logged in", 401
  
    
    @api_api.route("/auth_google_fit", methods=['POST'])
    def connect_google_fit():
        if user_id := session.get('user_id'):
            if auth_code := request.args.get('code'):
                if refresh_token := g_get_refresh_token(auth_code):
                    if not db.update_google_refresh_token(user_id, refresh_token): # STORE IN DB
                        return "Failed to insert to db", 500 # should not happen
                    if access_token := g_get_access_token(refresh_token):
                        if result := g_get_data(access_token):
                            db.google_steps_refresh(user_id, result)
                            return "", 200
                        else:
                            return "Failed to fetch Google steps", 500 # should not happen
                    else:
                        return "Failed to fetch Google access token", 500 # should not happen
                else:
                    return "Failed to fetch Google refresh token", 500 # should not happen. App already authorized, user must revoke privileges from Google manually
            else:
                return "Invalid params", 400 # Missing Google auth code, this route should only be called from Google auth servers
        else:
            return "Not logged in", 401

    return api_api


def g_refresh_data_procedure(db, user_id):
    """
    Procedure of function calls that handle fetching data from Google's API
    Get refresh token -> get access token -> get data -> store to database

    Parameters:
    db (DBM): Global database manager object
    user_id (str): MongoDB unique Object_ID

    Returns:
    bool : Success
    """
    refresh_token = db.get_google_refresh_token(user_id)
    if refresh_token:
        access_token = g_get_access_token(refresh_token)
        if access_token:
            steps_dict = g_get_data(access_token)
            db.google_steps_refresh(user_id, steps_dict)
            return True
    return False


def g_get_refresh_token(code):
    """
    Gets new refresh token from Google API

    Parameters:
    code (str): Authentication code from Google Auth Servers

    Returns:
    str: Refresh token, False if fail.
    """
    AT = {
        "code":code,
        "redirect_uri":"<url to frontend>/google", # Replace with own config, keep /google path
        "client_id":"", # Fill in with own config
        "client_secret":"", # Fill in with own config
        "scope":"",
        "grant_type":"authorization_code",
        "access_type":"offline"
    }

    try:
        r = requests.post("https://oauth2.googleapis.com/token", data=AT).json()
        refresh_token = r["refresh_token"]
    except Exception as e:
        traceback.print_exc()
        return False

    return refresh_token


def g_get_access_token(refresh_token):
    """
    Gets access token from Google API for use with data fetch

    Parameters:
    refresh_token (str): Google refresh token

    Returns:
    str: Access token, False if fail.
    """
    AT = {
        "refresh_token":refresh_token,
        "client_id":"", # Fill in with own config
        "client_secret":"", # Fill in with own config
        "scope":None,
        "grant_type":"refresh_token"
    }

    try:
        r = requests.post("https://www.googleapis.com/oauth2/v4/token", data=AT).json()
        access_token = r["access_token"]
    except Exception as e:
        traceback.print_exc()
        return False

    return access_token


def g_get_data(access_token):
    """
    Fetches and parses user data (steps & distance) from Google API.
    Data is from 30 days back until today.

    Parameters:
    access_token (str): Google access token

    Returns:
    dict: Dictionary with keys per day, each day contains dict with steps and distance variables. False if fail.
    """
    next_midnight = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.datetime.min.time()) # Datetime for next midnight
    one_month_ago = next_midnight - datetime.timedelta(days=31) # Datetime for midnight one month back
    AGG = {
    "aggregateBy": [{
        "dataTypeName": "com.google.step_count.delta",
        "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
    }, 
    {
        "dataTypeName": "com.google.distance.delta",
        "dataSourceId": "derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta"
    }],
    "bucketByTime": { "durationMillis": 86400000 },
    "startTimeMillis": int(one_month_ago.timestamp())*1000,
    "endTimeMillis":   int(next_midnight.timestamp())*1000
  }

    try:
        r = requests.post("https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate", headers={'Authorization': f"Bearer {access_token}"}, json=AGG).json()
        stats_past_month = {}

        for day in r["bucket"]:
            steps = 0
            distance = 0
            
            # ---- Extract Steps ---- #
            if pt := next(iter(day["dataset"][0]["point"]), 0):
                steps = pt["value"][0]["intVal"]
            
            # ---- Extract Distance ---- #
            if pt := next(iter(day["dataset"][1]["point"]), 0):
                distance = pt["value"][0]["fpVal"]

            stats_past_month[str(datetime.datetime.fromtimestamp(int(day["startTimeMillis"])/1000).date())] = {"steps":steps, "distance":distance}
    except Exception as e:
        traceback.print_exc()
        return False
    return stats_past_month


def f_refresh_data_procedure(db, user_id):
    """
    Procedure of function calls that handle fetching data from Fitbit's API
    Get refresh token -> get data -> store to database

    Parameters:
    db (DBM): Global database manager object
    user_id (str): MongoDB unique Object_ID

    Returns:
    bool: Success
    """
    refresh_token = db.get_fitbit_refresh(user_id)
    if refresh_token:
        steps = f_get_data(db, refresh_token, user_id)
        if steps:
            db.fitbit_steps_refresh(user_id, steps)
            return True
    return False


def f_get_refresh_token(code):
    """
    Gets new refresh token from Fitbit API

    Parameters:
    code (str): Authentication code from Fitbit Auth Servers

    Returns:
    str: Refresh token, False if fail.
    """
    headers = {
        'Authorization': 'Basic xxxxxxx', #replace with new token
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
    'clientId': '', # Replace with own config
    'grant_type': 'authorization_code',
    'redirect_uri': '', # Replace with own config
    'code': code
    }

    try:
        response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data).json()
        refresh_token = response['refresh_token']
    except Exception as e:
        traceback.print_exc()
        return False
        
    return refresh_token


def f_get_access_token(db, refresh_token, user_id):
    """
    Gets access token from Fitbit API for use with data fetch.
    Updates database with new refresh token.


    Parameters:
    db (DBM): Global database manager object
    refresh_token (str): Fitbit refresh token
    user_id (str): MongoDB unique Object_ID

    Returns:
    str: Access token, False if fail.
    """
    if user_id:
        headers = {
        'Authorization': 'Basic xxxxxxxxx', #replace with new token
        'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
        }

        try:
            response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data).json()
            refresh_token = response['refresh_token']
            access_token = response['access_token']
            db.add_fitbit_refresh(refresh_token, user_id)
        except Exception as e:
            traceback.print_exc()
            db.add_fitbit_refresh("", user_id)
            return False
    else:
        return "Not logged in", 401
    return access_token

def f_get_data(db, refresh_token, user_id):
    """
    Fetches and parses user data (steps & distance) from Fitbit API.
    Data is from 30 days back until today.
    Updates database with new refresh token.

    Parameters:
    db (DBM): Global database manager object
    user_id (str): MongoDB unique Object_ID
    refresh_token (str): Fitbit access token

    Returns:
    dict: Dictionary with keys per day, each day contains dict with steps and distance variables. False if fail.
    """
    access_token = f_get_access_token(db, refresh_token, user_id)
    headers = {
    'Authorization': f'Bearer {access_token}'
    }
    
    start_date = datetime.datetime.now() - datetime.timedelta(days=+30)
    start_date = start_date.strftime("%Y/%m/%d")\
                           .replace("/","-")
    try:
        response_steps = requests.get('https://api.fitbit.com/1/user/-/activities/steps/date/' + start_date + '/today/1min.json', headers=headers).json()
        access_token = f_get_access_token(db, refresh_token, user_id)
        response_dist = requests.get('https://api.fitbit.com/1/user/-/activities/distance/date/' + start_date + '/today/1min.json', headers=headers).json()
    except Exception as e:
        traceback.print_exc()
        return False

    result = {day["dateTime"]:{'steps':int(day["value"])} for day in response_steps["activities-steps"]}

    for day in response_dist["activities-distance"]:
        result[day["dateTime"]]['distance'] = float(day["value"])*1000
    
    return result
