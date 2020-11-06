// Used in UserArea.vue and DashboardSection.vue
import axios from 'axios';
import url from '../url.js';

const apiUrl = url.backendUrl + '/user';

export default {

  // Gets a users information from the backend
  async getUserInfo() {
    
    let requestUrl = `${apiUrl}/current`;
    
    try {
      
      let response = await axios.get(requestUrl, {withCredentials: true});
      return response;
      
    } catch(error) {
      
      return error.response;
    }
  },
  
  // Gets a users step and ditance statistics for the previous month
  async getUserStepsDistanceStats(){
    
    let requestUrl = `${apiUrl}/get_user_steps`;
    
    try {
      
      let response = await axios.get(requestUrl, {withCredentials: true});
      return response;
      
    } catch(error) {
      
      return error.response;
    }
  }    
  
}
