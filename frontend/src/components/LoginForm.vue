<template>

  <b-form
    @submit.prevent
    @keyup.enter="onLogin"
  >
    <h2 class="text-dark mb-4">Logga in</h2>
    
    <!-- email input -->
    <b-form-group>
      <b-input-group>
        
        <b-input-group-prepend is-text>
          <b-icon icon="envelope-fill"></b-icon>
        </b-input-group-prepend>
        
        <b-form-input
          placeholder="Epost"
          type="email"
          :state="emailState"
          v-model.trim="$v.form.email.$model"
        ></b-form-input>

      </b-input-group>

      <!-- email error messages -->
      <div
        v-if="emailRequiredError"
        class="text-danger text-left mt-2" 
      >
        Fyll i epost
      </div>
      
      <div
        v-if="emailFormatError"
        class="text-danger text-left mt-2" 
      >
        Fel format på epost
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

    <!-- Login button -->
    <!-- the :disabled part makes the button unusable until the credentials are correct -->
    <b-button 
      size="lg"
      variant="info"
      block
      :disabled="$v.form.$invalid"
      @click="onLogin"
    >
      Logga in
    </b-button>
    
    <!-- Switch over to Register -->
    <p class="text-left mt-3">
      Är du inte registrerad? 
      
      <b-link
        class="text-info"
        @click="onRegister"
      >
        Registrera
      </b-link>
    
    </p>
  </b-form>
</template>


<script>
// Vuelidate form validation package
import { required, email } from 'vuelidate/lib/validators'

export default {
  name: "LoginForm",
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
    }
  },
  validations: {
    form: {
      email: { 
        required, 
        email 
      },
      password: { 
        required
      } 
    }
  },

  // Responsively computing if any validation error or state change has occurred
  computed: {
    
    emailState() {
      if (!this.$v.form.email.$dirty) {
        return null
      }
      else {
        return !this.$v.form.email.$invalid
      }
    },

    emailRequiredError() {
      return this.$v.form.email.$dirty && 
             !this.$v.form.email.required
    },

    emailFormatError() {
      return this.$v.form.email.$dirty && 
             !this.$v.form.email.email
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
    // Passes on information to LoginArea to take care of the login and register logic
    onLogin() {
      this.$emit('login-pressed', this.form);
    },
    onRegister() {
      this.$emit('register-pressed');
    }
  },
}
</script>

<style scoped>
</style>
