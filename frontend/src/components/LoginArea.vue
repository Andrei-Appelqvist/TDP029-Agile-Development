<template>
  <b-container>
    
    <b-form-row 
      id="content-row" 
      class="align-items-center"
    >
      <b-col 
        id="content-col" 
        cols="4" 
        class="mx-auto"
      > 
        <!-- Card containing the forms -->
        <b-card 
          class="text-center" 
          bg-variant="white">
          
          <b-icon 
            id="calendar-icon" 
            class="my-3" 
            icon="calendar-fill"
          ></b-icon>
          
          <LoginForm
            v-if="loginState === 'login'"
            @login-pressed="attemptLogin" 
            @register-pressed="changeLoginState('register')"
          />

          <RegisterForm
            v-if="loginState === 'register'"
            @login-pressed="changeLoginState('login')"
            @register-pressed="attemptRegister"
          />
          
          <div
            v-if="showSuccess"
            class="alert alert-success" 
            role="alert" 
          >
            {{ successMessage }}
          </div>

          <div
            v-if="showError"
            class="alert alert-danger" 
            role="alert" 
          >
            {{ errorMessage }}
          </div>

        </b-card>
      </b-col>
    </b-form-row>
  </b-container>
</template>


<script>
// Components
import LoginForm from "../components/LoginForm.vue";
import RegisterForm from "../components/RegisterForm.vue";

// Services
import LoginService from "../services/LoginService.js";
import RegisterService from "../services/RegisterService.js";

export default {
  name: "LoginArea",
  components: {
    LoginForm,
    RegisterForm
  },
  data() {
    return {
      loginState: 'login',
      showSuccess: false,
      showError: false,
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    
    // Changes between register and login forms
    changeLoginState(newState) {
      this.clearMessages()
      this.loginState = newState
    },

    // Tries to login a user in the backend
    async attemptLogin(loginForm) {

      this.clearMessages()

      // Grabs whatever was written in the email and password fields
      // And sends it to the function attemptLogin in the LoginService file
      let response = await LoginService.attemptLogin(
        loginForm.email,
        loginForm.password
      ); 

      if (response.status === 200) {
        this.$emit("login-user");

      } else if (response.status === 400) {
        this.errorMessage = "Fel format på epost eller lösenord"
        this.showError = true

      } else if (response.status === 401) {
        this.errorMessage = "Fel epost eller lösenord"
        this.showError = true

      } else {
        this.$emit('error-occurred', response.status.toString(), 'Oväntat fel har uppstått')
      }
    },

    // Tries to register a new user in the backend
    async attemptRegister(registerForm) {
      
      this.clearMessages();

      // Sends the information from the username, email and password fields to attemptRegister
      // In the LogRegService file
      let response = await RegisterService.attemptRegister(
        registerForm.username,
        registerForm.email,
        registerForm.password
      );

      if (response.status === 200) {
        this.successMessage = "Du är registrerad!";
        this.showSuccess = true;

      } else if (response.status === 400) {
        this.errorMessage = "Fel format på epost, användarnamn eller lösenord"
        this.showError = true

      } else if (response.status === 409) {
        this.errorMessage = "Epost är upptagen"
        this.showError = true

      } else {
        this.$emit('error-occurred', response.status.toString(), 'Oväntat fel har uppstått')
      }
    },

    // Clears success and error messages
    clearMessages() {

      this.showSuccess = false;
      this.showError = false;
      this.successMessage = '';
      this.errorMessage = '';

    }
  }
};
</script>


<style scoped>
#content-row {
  height: 100vh;
}

#content-col {
  min-width: 350px;
}

#calendar-icon {
  width: 100px;
  height: 100px;
}
</style>