<template>
  <div id="app">
    
    <LoginArea
      v-if="appState === 'unauthorized'"
      @login-user="setAuthorized"
      @error-occurred="showError"
    />

    <UserArea
      v-if="appState === 'authorized'"
      @logout-user="setUnauthorized"
      @error-occurred="showError"
    />

    <ErrorArea
      v-if="appState === 'error'"
      :error="error"
    />
  
  </div>
</template>

<script>
// Components
import LoginArea from "./components/LoginArea.vue"
import UserArea from "./components/UserArea.vue"
import ErrorArea from "./components/ErrorArea.vue"

// Services
import LoginService from "./services/LoginService.js"

export default {
  name: 'App',
  components: {
    LoginArea,
    UserArea,
    ErrorArea
  },
  data() {
    return {
      appState: '',
      error: {
        title: '',
        message: ''
      }
    }
  },

  // Checks a users login status to know which state to load into
  async created() {
    
    let response = await LoginService.checkLoginStatus();

    if (response.status === 200) {
      this.appState = 'authorized'

    } else if (response.status === 401) {
      this.appState = 'unauthorized'
      
    } else {
      this.showError(response.status.toString(), 'Oväntat fel har uppstått')
    }

  },
  methods: {
    
    // Methods to change app state

    setAuthorized() {
      this.appState = 'authorized'
    },

    async setUnauthorized() {
      await LoginService.logoutUser()
      this.appState = 'unauthorized'
    },

    async showError(errorTitle, errorMessage) {
      this.error.title = errorTitle
      this.error.message = errorMessage

      await LoginService.logoutUser()

      this.appState = 'error'
    }
    
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #F8F9FA;
  height: 100vh;
  width: 100vw;
}
</style>
