import db_manager
import user_api
import workout_api
import api_api

from flask import Flask, session, request
from flask_cors import CORS

app = Flask(__name__)
app.config["SESSION_COOKIE_NAME"] = 'session2'
app.secret_key = 'secrethehe'

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

db = db_manager.DBM()
db.connect()

app.register_blueprint(user_api.user_api_constructor(db), url_prefix="/user")
app.register_blueprint(workout_api.workout_api_constructor(db), url_prefix="/user/workout")
app.register_blueprint(api_api.api_api_constructor(db), url_prefix="/user/api")

