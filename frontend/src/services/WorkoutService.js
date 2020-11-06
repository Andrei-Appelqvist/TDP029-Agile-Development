// Used in DashboardSection.vue, CalendarSection.vue and CalendarAddWorkoutForm.vue

import axios from 'axios';
import url from '../url.js'

const apiUrl = url.backendUrl + '/user/workout'


export default {
  
  // Gets a users performed workouts for a specific week of a year
  async getWorkouts(year, week) {
    
    let requestUrl = `${apiUrl}/get_workouts?year=${year}&week=${week}`;
    
    try {
      
      let response = await axios.get(requestUrl, {withCredentials: true});
      return response;
      
    } catch(error) {
      
      return error.response;
    }
  },
  
  // Adds a user created workout using the information inputed in the CalendarAddWorkoutForm
  async addWorkout(obj) {
    
    let requestUrl = `${apiUrl}/add_workout`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      withCredentials: true
    }

    const body = obj;
    
    try {
      
      const response = await axios.post(requestUrl, body, config);
      return response;
    
    } catch(error) {
      
      return error.response;
    }
  },
  
  // Fetches all workout types that the specific gymsystem contains
  async getAllWorkoutTypes() {
    
    let requestUrl = `${apiUrl}/get_workout_types`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      withCredentials: true
    }

    try {
      
      const response = await axios.get(requestUrl, config);
      return response;
    
    } catch(error) {
      
      return error.response;
    }
  },
  
  // Gets a users statistics regarding time spent performing different types of workouts
  async getWorkoutTypeStats(year, week) {
    
    let requestUrl = `${apiUrl}/get_week_stats?year=${year}&week=${week}`;
    
    try {
      
      let response = await axios.get(requestUrl, {withCredentials: true});
      return response;
    
    } catch(error) {
      
      return error.response;
    }
  }
}