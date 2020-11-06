// Used in App.vue and LoginArea.vue
import axios from 'axios';
import url from '../url.js';

const apiUrl = url.backendUrl + '/user';


export default {
  
  // Tries to login a user using the user inputs of the login form
  async attemptLogin(email, password) {
    
    let requestUrl = `${apiUrl}/login`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      withCredentials: true
    };
    
    const body = JSON.stringify({
      email: email,
      password: password
    });
    
    try {
      
      let response = await axios.post(requestUrl, body, config);
      return response;
      
    } catch(error) {
      
      return error.response;
    }
  },
  
  // Checking if a users credentials(cookie) are still valid
  async checkLoginStatus() {
    
    let requestUrl = `${apiUrl}/logged_in`;
    
    const config = {
      withCredentials: true
    };
    
    try {
      
      let response = await axios.get(requestUrl, config);
      return response;
      
    } catch(error) {
      
      return error.response;
    }
  },
  
  // Makes the credentials(cookie) for a logged in user invalid
  async logoutUser() {
    
    let requestUrl = `${apiUrl}/logout`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      withCredentials: true
    };
    
    try {
      
      let response = await axios.post(requestUrl, {} ,config);
      return response;
      
    } catch(error) {
      
      return error.response;
    }
  }
}