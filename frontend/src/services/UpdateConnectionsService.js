// Used in UserArea.vue and ConnectGymsystemForm.vue
import axios from 'axios';
import url from '../url.js';

const apiUrl = url.backendUrl + '/user';

export default {
  
  // Sends user information, fetched from gymsystem, to update the backend of the app
  async updateGymsystemInfo(userInfo) {
    
    let requestUrl = `${apiUrl}/add_zoezi_id`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      withCredentials: true
    }
    
    const body = userInfo;
    
    try {
      
      const response = await axios.post(requestUrl, body, config);
      return response;
      
    } catch(error){
      
      return error.response;
    }
  },
  
  // Sends a google authorization code, fetched from google API, to update the backend of the app
  async updateGoogleInfo(authorizationCode) {
    
    let requestUrl = `${apiUrl}/api/auth_google_fit?code=${authorizationCode}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      withCredentials: true
    } 
    
    try {
      
      const response = await axios.post(requestUrl, {}, config);
      return response;
      
    } catch(error){
      
      return error.response;
    }
  },
  
  // Sends a fitbit authorization code, fetched from fitbit API, to update the backend of the app
  async updateFitbitInfo(authorizationCode) {
    
    let requestUrl = `${apiUrl}/api/authorize_fitbit?code=${authorizationCode}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      withCredentials: true
    } 
    
    try {
      
      const response = await axios.post(requestUrl, {}, config);
      return response;
      
    } catch(error){
      
      return error.response;
    }
  }
}