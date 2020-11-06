// Used in ConnectGymsystemForm.vue
import axios from 'axios';
import url from '../url.js';

const apiUrl = url.gymsystemUrl + '/api';

export default {
  
  // Tries to login a user to the gymsystem and returns the gymsystem user information
  async getGymsystemInfo(email, password) {
    
    let requestUrl = `${apiUrl}/memberapi/login`;
    
    try {
      
      const response = await axios.post(requestUrl, {}, {
        params: {
          mail: email,
          password: password
        }
      });
      
      return response;
      
    } catch(error){
      
      return error.response;
    }
  }
}