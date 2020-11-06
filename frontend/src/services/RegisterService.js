// Used in LoginArea.vue
import axios from 'axios';
import url from '../url.js';

const apiUrl = url.backendUrl + '/user';

export default {
  
  // Tries to register a new user using the user inputs of the register form
  async attemptRegister(username, email, password) {
    
    let requestUrl = `${apiUrl}/create`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      withCredentials: true
    }
    
    const body = JSON.stringify({
      username: username,
      email: email,
      password: password
    });
    
    try {
      
      let response = await axios.post(requestUrl, body, config);
      return response;
      
    } catch(error) {
      
      return error.response;
    }
  }
}