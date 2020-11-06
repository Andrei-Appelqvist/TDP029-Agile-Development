import db_manager

from datetime import datetime
import bson

class Workout:
    """
    Class that parses workout objects from various sources and inserts
    data to instance. This data is then retrieved in a standardized
    format using to_dictionary(). Each new source of Workout objects
    only requires a new parse_<source>() function that is able to properly
    extract the required data.
    """
    def __init__(self):
        pass


    def parse_zoezi(self, workout):
        """
        Initializes standardized Workout object from gymsystem-formatted dict.

        Parameters:
        workout (dict): JSON-parsed dict of raw zoezi-gymsystem workout.

        Returns:
        None
        """
        self.workout_name = workout["workoutType"]["name"]
        self.workout_id   = workout['id']
        self.start_time   = workout['startTime']
        self.end_time     = workout['endTime']
        self.description  = workout["workoutType"].get('description')
        self.location     = workout["resources"][0]["lastname"] if workout["resources"] else None
        self.source       = "Z"

    def parse_manual(self, workout):
        """
        Initializes standardized Workout object from Frontend-formatted dict.

        Parameters:
        workout (dict): JSON-parsed dict of raw Frontend-type workout.

        Returns:
        None
        """

        # Mandatory values:
        self.workout_name = workout["workout_name"]
        self.workout_id   = str(bson.ObjectId()) # create unique ID for workout
        self.start_time   = workout['start_time']
        self.end_time     = workout['end_time']
        self.source       = "M"

        # Optional values:
        self.description  = workout.get('description')
        self.location     = workout.get('location')
        self.distance     = workout.get('distance')
        self.steps        = workout.get('steps')


    def to_dictionary(self):
        """
        Converts class member variables of current object to dictionary and
        filters out None values. Class members are standardized so this will
        yield a dict that has consistently named keys, but only if they have data.

        Parameters:
        None

        Returns:
        dict : Workout dict with standardized keys
        """
        member_variables = {attr:val for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and (val:=eval(f"self.{attr}")) != None}
        return member_variables