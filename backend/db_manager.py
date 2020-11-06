import wt_manager

from datetime import *
from collections import defaultdict
from operator import itemgetter
import pymongo, bson
import bcrypt
import pprint
import json
import collections
import traceback

pp = pprint.PrettyPrinter(indent=4)


class DBM:
    """
    Database Manager.
    Class that handles MongoDB database connection and manipulates 
    data that is extracted or inserted.
    """
    def __init__(self):
        pass


    def connect(self):
        """
        Connects Pymongo to mongo database by URL and initializes database variables.

        Parameters:
        None

        Returns:
        None
        """
        self.myclient = pymongo.MongoClient("<MongoDB api link>")
        self.db = self.myclient["workout_tracker"]
        self.user_collection = self.db["users"]


    def create_user(self, username, email, password):
        """
        Function that is called by the "/create" route (user_api.py) in order to
        create the user object and add it to the database collection.

        Parameters:
        username (str): Username for the user from frontend form.
        email (str): Email for user account, also from frontend form.
        password (bytes): Encrypted password from route call.

        Returns:
        Nothing, adds only object to the database.

        """
        user_obj = {
                    "email"           : email,
                    "password"        : password,
                    "username"        : username,
                    "zoezi_workouts"  : {},
                    "manual_workouts" : {},
                    "lastdbupdate"    : datetime.now() - timedelta(minutes = 5),
                    "zoezi_id"        : "",
                    "zoezi_session"   : "",
                    "fitbit_refresh"  : "",
                    "fitbit_steps"    : {},
                    "google_refresh"  : "",
                    "google_steps"    : [],
                    "workout_types"   : []
                    }
        self.user_collection.insert_one(user_obj)


    def add_workout_type(self, user_id, w_type):
        """
        Function that adds workout types to the workout_types array
        in user object. It is called by the functions that add workouts
        to the user object (add_manual_workout & zoezi_workouts_refresh).
        The array will be used by frontend to give suggestions when user 
        adds workouts.

        Parameters:
        user_id (str): MongoDB unique Object_ID.
        w_type (str): Workout type to be added. 

        Returns:
        Nothing
        """
        self.user_collection.update({'_id':bson.ObjectId(user_id)},
                                    {'$addToSet' : { 'workout_types' : w_type}})


    def check_existing_user(self, email):
        """
        Checks if there is a user with that email in the database.

        Parameters:
        email (str): The email that gets checked out.

        Returns:
        bool : If exists
        """
        exists = list(self.user_collection.find({"email": email}))
        if len(exists) > 0:
            return True
        else:
            return False


    def check_credentials(self, email, password):
        """
        Checks if there is a user with that email in the database and
        checks if the password matches the parameter password.

        Parameters:
        email (str) : The email that gets checked out.
        password (str) : The password that is checked out.

        Returns:
        _id (str) : MongoDB unique Object_ID for user.
        False (bool): If there is no such user or password does not match.
        """
        try:
            usr = list(self.user_collection.find({"email":email}))
        except ServerSelectionTimeoutError as e:
            traceback.print_exc()
            return False

        if len(usr) > 0 and bcrypt.checkpw(password.encode("utf-8"), usr[0]["password"]):
            return str(usr[0]['_id'])
        else:
            return False


    def get_user_fromid(self, user_id):
        """
        Getter function for user data. The data is filtered in this function
        so that no sensitive information is returned. Some variables are also
        filtered down the line where this function is called.

        Parameters:
        user_id (str) : MongoDB unique Object_ID.

        Returns:
        None : If there is no object with that ID.
        user_dict (Dict) : Filtered dict with user info.
        """
        user_obj = {"_id" : bson.ObjectId(user_id)}
        user_obj = self.user_collection.find_one(user_obj,
                    {
                        "email"          : 1,
                        "username"       : 1,
                        "lastdbupdate"   : 1,
                        "zoezi_id"       : 1,
                        "zoezi_session"  : 1,
                        "google_refresh" : 1,
                        "fitbit_refresh" : 1
                    })
        if user_obj == None:
            return None
        
        user_dict = {
            "email"               : user_obj["email"],
            "username"            : user_obj["username"],
            "lastdbupdate"        : user_obj["lastdbupdate"], # Will be deleted in /current
            "is_connected_zoezi"  : user_obj["zoezi_id"] != "",
            "zoezi_id"            : user_obj["zoezi_id"],
            "zoezi_session"       : user_obj["zoezi_session"],
            "google_connected"    : user_obj["google_refresh"] != "", # BOOL is google connected?,
            "fitbit_connected"    : user_obj["fitbit_refresh"] != "" # BOOL is fitbit connected?
        }
        return user_dict


    def remove_user_by_id(self, user_id):
        """
        Removes user with the given user ID from the database.

        Parameters:
        user_id (str) : MongoDB unique Object_ID

        Returns:
        bool : Success
        """
        user_obj = {"_id" : bson.ObjectId(user_id)}
        return bool(self.user_collection.delete_one(user_obj).deleted_count)


    def update_time(self, mongo_id):
        """
        Updates the timestamp for latest update of the user object. The
        "lastdbupdate" value. This is used for a timer in /current so that
        the objects can't be spam updated.

        Parameters:
        user_id (str) : MongoDB unique Object_ID.

        Returns:
        Nothing only updates user obj in database.
        """
        self.user_collection.update_one({'_id':bson.ObjectId(mongo_id)},
                                        {'$set': {'lastdbupdate': datetime.now()}}, upsert=False)


    def create_manual_workout(self, user_id, workout_obj):
        """
        Creates and adds workout to user object in the manual_workouts object.
        The workout object comes from the frontend where the user adds their own workouts.
        Workouts that come from the zoezi system are parsed and added in another function.

        Parameters:
        user_id (str) : MongoDB unique Object_ID.
        workout_obj (dict) : Json object that has the relevant info, later parsed into Workout obj.

        Returns:
        Nothing only updates user obj in database.
        """
        w = wt_manager.Workout()
        w.parse_manual(workout_obj)
        self.add_workout_type(user_id, w.workout_name)
        w = w.to_dictionary()

        year, week = datetime.strptime(w['start_time'], '%Y-%m-%d %H:%M:%S').isocalendar()[0:2]

        self.user_collection.update_one({'_id': bson.ObjectId(user_id)},
                                        {'$push': {f'manual_workouts.{year}-{week}': w}}, upsert=True)


    def zoezi_workouts_refresh(self, user_id, raw_workouts_array):
        """
        Procedure to parse workouts from zoezi gymsystem, and insert
        to database with proper format.

        Parameters:
        user_id (str): MongoDB unique Object_ID
        raw_workouts_array (list): array with workouts from zoezi

        Returns:
        bool : Success
        """
        parsed_workouts = defaultdict(list)

        for workout in raw_workouts_array:
            w = wt_manager.Workout()
            try:
                w.parse_zoezi(workout)
            except KeyError as e:
                traceback.print_exc()
                return False
                
            self.add_workout_type(user_id, w.workout_name)
            w = w.to_dictionary()
            year, week = datetime.strptime(w['start_time'], '%Y-%m-%d %H:%M:%S').isocalendar()[0:2]
            parsed_workouts[f"{year}-{week}"].append(w)
            
        self.user_collection.update_one({"_id" : bson.ObjectId(user_id)}, {'$set': {'zoezi_workouts': parsed_workouts}})
        return True


    def get_week_stats(self, year, week, id):
        """
        Function that fetches and sorts the data for the doughnut chart in
        the frontend. Called by "/get_week_stats" route in workout_api.py.
        It works by getting all the workouts for four weeks back from 
        zoezi_workouts and manual workouts, and the amount of minutes for each workout type.
        That is the basic function. As an addition if the amount of workout types is higher than
        the [break_point_misc_workouts], workouts will be sorted so that those with a percentage of minutes lower than
        [percent_factor] of total minutes will be added to a miscellaneous pseudo-workout type "Övrigt" 
        that will sum the minutes of all the workouts in there. This behaviour can be 
        suppressed by having a really high [break_point_misc_workouts].

        Parameters:
        year (str) : The year the user wants to get workouts from.
        week (str) : The week the uesr wants to get workouts from.
        id (str) : MongoDB unique Object_ID for user.


        Returns:
        stats (Dict) : With workout types, minutes for all workout types
                       and the date interval for the data.
        """
        stats = {}
        all_workouts = []
        #Loop to get workout chosen week and three back
        for i in range(4):
            n_week = str(int(week)-i)
            week_workouts = self.get_week_workouts(year, n_week, id)
            all_workouts.extend(week_workouts)
        if not all_workouts:
            return {}
        stat_dict = collections.defaultdict(list)
        stats['minutes'] = {}
        #============Trained_Minutes_Per_Week=============
        FMT = '%Y-%m-%d %H:%M:%S'
        tot_time = timedelta()
        #Add date intervall to object
        stats['dates'] = all_workouts[-1]['start_time'].partition(' ')[0]+ " - "+all_workouts[0]['start_time'].partition(' ')[0]
        for obj in all_workouts:
            # Get time difference between start and end for all workouts and add
            # the time differences to an array with the workout type as key
            tdelta = datetime.strptime(obj['end_time'], FMT) - datetime.strptime(obj['start_time'], FMT)
            tot_time += tdelta
            stat_dict[obj['workout_name']].append(tdelta.total_seconds() /60)
        tdelta = tot_time.total_seconds()/60
        #Sum all minutes and add to object
        stats['tot_minutes'] = tdelta
        #==============Minutes_Workout_Type===============
        break_point_misc_workouts = 6
        percent_factor = 0.1
        if(len(stat_dict) > break_point_misc_workouts):
            #Sorting for övrigt starting here, can be skipped with high
            #break_point_misc_workouts
            workout_sorting_array = []
            temp_sum_minutes = 0
            #Same loop as in standard except addin to extra array for 
            #further manipulation
            for key,value in stat_dict.items():
                temp_sum_minutes = value[0]
                if len(value) > 1:
                    temp_sum_minutes = sum(value)
                workout_sorting_array.append((key, temp_sum_minutes))
            workout_sorting_array.sort(key=itemgetter(1), reverse=True)
            misc_val = 0
            stats['misc_labels'] = []
            for w in workout_sorting_array:
                #Here we choose if the workout should be added to regular
                #Array or to the Övrigt part based on amount of minutes
                if w[1]/tdelta > percent_factor:
                    stats['minutes'][w[0]]=w[1]
                else:
                    #If we get here, then minutes for workout type
                    #are less % than [percent_factor] and name is added to
                    #a label array where all övrigt workouts labels are stored
                    misc_val += w[1]
                    stats['misc_labels'].append(w[0])
            if misc_val > 0:
                #All summed övrigt workout minutes are added.
                stats['minutes']['Övrigt'] = misc_val
        else:
            #Standard return where all minutes for workout type
            #are being summed and added to obj.
            v = 0
            for key, value in stat_dict.items():
                v = value[0]
                if len(value) > 1:
                    #Sums all values in array for each workout type
                    v = sum(value)
                stats['minutes'][key] = v

        return stats


    def get_week_workouts(self, year, week, id):
        """
        Function that gets all the workouts for a certain year, week.
        Gets workouts from zoezi_workouts array and also manual_workouts.
        Used in all functions that need to get all workouts for any reason as
        well as being called in a route for the calendar part of frontend. The workouts
        are being sorted after start time.

        Parameters:
        year (str): The year the user wants to get workouts from.
        week (str): The week the uesr wants to get workouts from.
        id (str): MongoDB unique Object_ID for user.


        Returns:
        (Array) : Array that has all the workout dicts sorted after start_time.
        """
        zoezi  = self.user_collection.find_one({'_id': bson.ObjectId(id)}, {"zoezi_workouts":1})
        manual = self.user_collection.find_one({'_id': bson.ObjectId(id)}, {"manual_workouts":1})

        if z := zoezi["zoezi_workouts"].get(f"{year}-{week}"):
            all_workouts = z
        else:
            all_workouts = []   
        if m := manual["manual_workouts"].get(f"{year}-{week}"):
            all_workouts.extend(m)
        all_workouts = sorted(all_workouts, key=lambda x : datetime.strptime(x['start_time'], '%Y-%m-%d %H:%M:%S'))

        return all_workouts


    def add_zoezi_id(self, zoezi_id, zoezi_session, user_id):
        """
        Fetches Zoezi user ID from Zoezi and inserts in database.

        Parameters:
        user_id (str) : MongoDB unique Object_ID
        zoezi_id(int) : zoezi user ID
        zoezi_session(str) : Logged-in zoezi session

        Returns:
        bool : Success
        """
        r = self.user_collection.update_one({'_id': bson.ObjectId(user_id)},
                                            {'$set':{'zoezi_id': zoezi_id}})
                                            
        s = self.user_collection.update_one({'_id': bson.ObjectId(user_id)},
                                            {'$set':{'zoezi_session': zoezi_session}})

        return (r.acknowledged and s.acknowledged)


    def add_fitbit_refresh(self,refresh_token, user_id):
        """
        Inserts fitbit refresh token in database.

        Parameters:
        refresh_token (str): The refresh token to insert
        user_id (str): MongoDB unique Object_ID

        Returns:
        bool: Success.
        """
        r = self.user_collection.update_one({'_id': bson.ObjectId(user_id)},
                                            {'$set':{'fitbit_refresh': refresh_token}})
        return (r.acknowledged)


    def get_fitbit_refresh(self, user_id):
        """
        Gets fitbit refresh token from database.

        Parameters:
        user_id (str): MongoDB unique Object_ID

        Returns:
        str: Fitbit refresh token
        """
        refresh_token = self.user_collection.find_one({'_id': bson.ObjectId(user_id)}, 
                                                      {"fitbit_refresh":1})
        return refresh_token['fitbit_refresh']


    def fitbit_steps_refresh(self, user_id, steps):
        """
        Inserts step stats (including step count & distance) from Fitbit in database.

        Parameters:
        user_id (str) : MongoDB unique Object_ID
        steps(dict) : dictionary with date as key and step stats as values.

        Returns:
        bool : Success
        """
        r = self.user_collection.update_one({'_id': bson.ObjectId(user_id)},
                                            {'$set':{'fitbit_steps': steps}})
        return r.acknowledged


    def update_google_refresh_token(self, user_id, refresh_token):
        """
        Inserts Google refresh token in database.

        Parameters:
        refresh_token (str): The refresh token to insert
        user_id (str) : MongoDB unique Object_ID

        Returns:
        bool: Success.
        """
        r = self.user_collection.update_one({'_id': bson.ObjectId(user_id)},
                                            {'$set':{'google_refresh': refresh_token}})
        return r.acknowledged


    def get_google_refresh_token(self, user_id):
        """
        Gets Google refresh token from database.

        Parameters:
        user_id (str): MongoDB unique Object_ID

        Returns:
        str: Google refresh token
        """
        refresh_token = self.user_collection.find_one({'_id': bson.ObjectId(user_id)},
                                                      {"google_refresh":1})
        return refresh_token["google_refresh"]


    def google_steps_refresh(self, user_id, steps):
        """
        Inserts step stats (including step count & distance) from Google in database.

        Parameters:
        user_id (str) : MongoDB unique Object_ID
        steps(dict) : dictionary with date as key and step stats as values.

        Returns:
        bool : Success
        """
        r = self.user_collection.update_one({'_id': bson.ObjectId(user_id)},
                                            {'$set':{'google_steps': steps}})


    def get_workout_types(self, user_id):
        """
        Fetches workout types from database.

        Parameters:
        user_id (str) : MongoDB unique Object_ID

        Returns:
        list : list with workout types
        """
        try:
            types = self.user_collection.find_one({'_id': bson.ObjectId(user_id)},
            {"workout_types":1})
        except Exception as e:
            traceback.print_exc()
            return []
        return types['workout_types']


    def get_user_steps(self, user_id):
        """
        Gets separate step data from database and packages into dict with
        entries for Google and Fitbit data. Gets both steps and distance
        for google and fitbit despite the name.

        Parameters:
        user_id (str): MongoDB unique Object_ID

        Returns:
        dict : Dictionary with keys 'google' and 'fitbit', each containing
        step and distance data in the format stored in the database.
        """
        step_data = {}

        #====================GOOGLE========================
        google = self.user_collection.find_one({'_id': bson.ObjectId(user_id)},
                                               {"google_steps":1})['google_steps']
        if(type(google) is dict and len(google) > 0):
            g_data = self.make_user_data_dict(google)
        else:
            g_data = None
        #====================FITBIT========================        
        fitbit = self.user_collection.find_one({'_id': bson.ObjectId(user_id)}, 
                                               {"fitbit_steps":1})["fitbit_steps"]
        if(type(fitbit) is dict and len(fitbit) > 0):
            f_data = self.make_user_data_dict(fitbit)
        else:
            f_data = None
        #======================PACK========================
        step_data['google'] = g_data
        step_data['fitbit'] = f_data

        return step_data


    def make_user_data_dict(self, data_dict):
        """
        Helper function for get_user_steps. Splits the original data dict
        in three arrays; dates, steps, distance. This format is chosen because
        vue bootstrap charts likes it's data as arrays. Need to be careful so that
        all the arrays are sorted in the same way when split otherwise the graphs 
        will go bananas.
        

        Parameters:
        data_dict (dict) : dict containing google or fitbit data as retrieved from
                           database by find_one.

        Returns:
        (Dict) : with three arrays, each with key refering to the content and sorted in the
                 same manner.
        """
        done             = {}
        done['steps']    = []
        done['distance'] = []
        arr              = list(data_dict.items())
        arr.sort(key=itemgetter(0))
        dates, sdict     = zip(*arr)
        done['dates']    = dates
        
        for x in sdict:
            done['steps'].append(x['steps'])
            done['distance'].append(round(x['distance'], 2)) 
        
        return done