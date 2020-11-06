<template>

  <!-- This form will be shown the first time you use the website -->
  <!-- it allows you to connect to your gymsystem account -->
  <b-form 
    v-on:submit.prevent 
    @keyup.enter="connectToGymsystem"
  >

    <!-- emailusername input -->
    <b-form-group >
      <b-input-group>
        
        <b-input-group-prepend is-text>
          <b-icon icon="person-fill"></b-icon>
        </b-input-group-prepend>
        
        <b-form-input
          placeholder="Epost eller användarnamn"
          :state="emailUsernameState"
          v-model.trim="$v.form.emailusername.$model"
          
        ></b-form-input>
      
      </b-input-group>

      <!-- emailusername error message -->
      <div
        v-if="emailUsernameRequiredError"
        class="text-danger text-left mt-2" 
      >
        Fyll i epost eller användarnamn
      </div>
    </b-form-group>

    <!-- password input -->
    <b-form-group>
      <b-input-group>
        
        <b-input-group-prepend is-text>
          <b-icon icon="lock-fill"></b-icon>
        </b-input-group-prepend>
        
        <b-form-input
          placeholder="Lösenord"
          type="password"
          :state="passwordState"
          v-model.trim="$v.form.password.$model"
        ></b-form-input>
      
      </b-input-group>
      
      <!-- password error message -->
      <div
        v-if="passwordRequiredError"
        class="text-danger text-left mt-2" 
      >
        Fyll i lösenord
      </div>
    </b-form-group>
    
    <!-- Connect button -->
    <b-button
      class="mb-3"
      variant="info"
      block
      :disabled="$v.form.$invalid"
      @click="connectToGymsystem"
    >
      Koppla
    </b-button>

    <!-- success and error message after connection attempt -->
    <div
      v-if="showSuccess"
      class="alert alert-success mb-0" 
      role="alert" 
    >
      Du är nu kopplad till Gymsystem
    </div>
    
    <div
      v-if="showError"
      class="alert alert-danger mb-0" 
      role="alert" 
    >
      Fel epost, användarnamn eller lösenord
    </div>
  </b-form>
</template>


<script>
// Services
import GymsystemService from '../services/GymsystemService.js'
import UpdateConnectionsService from '../services/UpdateConnectionsService.js'

// Vuelidate form validation package
import { required } from 'vuelidate/lib/validators'

export default {
  name: 'ConnectGymsystemForm',
  data() {
    return {
      form: {
        emailusername: '',
        password: ''
      },
      showSuccess: false,
      showError: false,
    }
  },
  validations: {
    form: {
      emailusername: {
        required
      },
      password: {
        required
      }
    }
  },

  // Responsively computing if any validation error or state change has occurred
  computed: {

    emailUsernameState() {
      if (!this.$v.form.emailusername.$dirty) {
        return null
      }
      else {
        return !this.$v.form.emailusername.$invalid
      }
    },

    emailUsernameRequiredError() {
      return this.$v.form.emailusername.$dirty && 
             !this.$v.form.emailusername.required
    },

    passwordState() {
      if (!this.$v.form.password.$dirty) {
        return null
      }
      else {
        return !this.$v.form.password.$invalid
      }
    },

    passwordRequiredError() {
      return this.$v.form.password.$dirty && 
             !this.$v.form.password.required
    }

  },

  methods: {
    // Tries to connect to gymsystem and then updates the backend using the response
    async connectToGymsystem() {
      
      this.showSuccess = false;
      this.showError = false;

      let gymsystemResponse = await GymsystemService.getGymsystemInfo(
        this.form.emailusername,
        this.form.password
      );

      if (gymsystemResponse.status === 200) {
        let backendResponse = await UpdateConnectionsService.updateGymsystemInfo(gymsystemResponse.data);

        if (backendResponse.status === 200) {
          this.showSuccess = true
          this.$emit('gymsystem-connected')
        
        } else if (backendResponse.status === 400) {
          this.showError = true
        
        } else if (backendResponse.status === 500) {
          this.$emit('error-occurred', backendResponse.status.toString(), 'Internt server-fel')
        
        } else {
          this.$emit('error-occurred', backendResponse.status.toString(), 'Oväntat fel har uppstått')
        }
      
      } else {
        this.showError = true;
      }
    }
  }
}
</script>

<style scoped>

</style>