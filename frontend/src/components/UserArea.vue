<template>
  <div>
    
    <HeaderSection
      :user="user"
      :page="state"
      @logout-user="logoutUser"
      @change-state="changeState"
    />

    <WelcomeSection
      v-if="state === 'welcome'"
      @goto-dashboard="loadUserInfo"
      @error-occurred="emitError"
    />

    <DashboardSection
      v-if="state === 'home'"
      :currentWeek="currentWeek"
      :currentYear="currentYear"
      :connectedHealthServices="user.connectedHealthServices"
      @change-state="changeState"
      @logout-user="logoutUser"
      @error-occurred="emitError"
    />
    
    <CalendarSection
      v-if="state === 'calendar'"
      :currentYear="currentYear"
      :currentWeek="currentWeek"
      @logout-user="logoutUser"
      @error-occurred="emitError"
    />

    <UserSettingsSection
      v-if="state === 'settings'"
      :user="user"
      @logout-user="logoutUser"
    />
    
  </div>
</template>

<script>
// Components
import HeaderSection from "../components/HeaderSection.vue";
import WelcomeSection from "../components/WelcomeSection.vue";
import DashboardSection from "../components/DashboardSection.vue";
import CalendarSection from "../components/CalendarSection.vue";
import UserSettingsSection from "../components/UserSettingsSection.vue";

// Services
import UserService from "../services/UserService.js"
import UpdateConnectionsService from "../services/UpdateConnectionsService.js"

// weeknumber package since javascript doesn't have it
import { weekNumber } from "weeknumber"

export default {
  name: "UserArea",
  components: {
    HeaderSection,
    WelcomeSection,
    DashboardSection,
    CalendarSection,
    UserSettingsSection
  },
  data() {
    return {
      state: '',
      user: {
        name: '',
        email: '',
        connectedHealthServices: []
      },
      currentYear: 0,
      currentWeek: 0,
    }
  },

  watch: {
    // Saves state in browsers localStorage to so that a user ends
    // up in the same state when refreshing
    state(newState) {
      localStorage.state = newState
    }
  },

  // Gets the current date, year, and week, fetches user information and checks for
  // new health connections
  async created() {

    let date = new Date()
    this.currentYear = date.getFullYear()
    this.currentWeek = weekNumber(date)

    if (!(await this.loadUserInfo())) {
      return
    }

    this.updateHealthConnections()

  },

  methods: {

    changeState(new_state) {
      this.state = new_state;
    },
    
    logoutUser() {
      localStorage.state = 'home'
      this.$emit('logout-user');
    },

    // Fetches user information and sets state depending on what services are connected
    async loadUserInfo() {
      
      let response = await UserService.getUserInfo();

      if (response.status === 200) {
        this.user.name = response.data.username;
        this.user.email = response.data.email;

        if (response.data.google_connected) {
          this.user.connectedHealthServices.push('google')
        }

        if (response.data.fitbit_connected) {
          this.user.connectedHealthServices.push('fitbit')
        }

        if (response.data.is_connected_zoezi) {
          
          if (localStorage.state && localStorage.state != 'welcome') {
            this.state = localStorage.state
        
          } else {
            this.state = 'home'
          }
          return true;

        } else {
          this.state = 'welcome'
          return false;
        }

    } else if (response.status === 401) {
      this.logoutUser()
      return false;

    } else {
      this.$emit('error-occurred', response.status.toString(), 'Oväntat fel har uppstått')
      return false;
    }
    },

    // Checks for url-responses from third party health services 
    // and updates the backend if any are found
    async updateHealthConnections() {
      
      let urlParams = window.location;
      
      switch(urlParams.pathname) {
        
        case "/google": {
          
          let authorizationCodeGoogle = urlParams.search.substring(
              urlParams.search.lastIndexOf("code=") + 5, 
              urlParams.search.lastIndexOf("&")
          );

          let googleResponse = await UpdateConnectionsService.updateGoogleInfo(
            decodeURIComponent(authorizationCodeGoogle)
          );
          
          if (googleResponse.status != 200) {
            
            this.$emit('error-occurred', googleResponse.status.toString(), 'Oväntat fel har uppstått')
          }

          window.location.href = window.location.origin
          break;
        }
        case "/fitbit": {
          
          let authorizationCodeFitbit = urlParams.search.substring(
            urlParams.search.lastIndexOf("code=") + 5
          )

          let fitbitResponse = await UpdateConnectionsService.updateFitbitInfo(
            decodeURIComponent(authorizationCodeFitbit)
          );
          
          if (fitbitResponse.status != 200) {
            
            this.$emit('error-occurred', fitbitResponse.status.toString(), 'Oväntat fel har uppstått')
          } 

          window.location.href = window.location.origin
          break;
        }
      }
    },

    // Sends error information up to App.vue if any error has occurred
    emitError(errorTitle, errorMessage) {
      localStorage.state = 'home'
      this.$emit('error-occurred', errorTitle, errorMessage)
    }
  },
}
</script>

<style scoped>
</style>