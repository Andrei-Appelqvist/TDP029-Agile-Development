<template>

  <b-form 
    @submit.prevent 
    @keyup.enter="onRegister"
  >
    <h2 class="text-dark mb-4">Registrera</h2>

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

     <!-- username input -->
    <b-form-group>
      <b-input-group>
        
        <b-input-group-prepend is-text>
          <b-icon icon="person-fill"></b-icon>
        </b-input-group-prepend>
        
        <b-form-input
          placeholder="Användarnamn"
          type="text"
          :state="usernameState"
          v-model.trim="$v.form.username.$model"
        ></b-form-input>

      </b-input-group>

      <!-- username error messages -->
      <div
        v-if="usernameRequiredError"
        class="text-danger text-left mt-2" 
      >
        Fyll i användarnamn
      </div>
      
      <div
        v-if="usernameMinLengthError"
        class="text-danger text-left mt-2" 
      >
        Användarnamn måste ha minst 
        {{ $v.form.username.$params.minLength.min }} 
        antal tecken
      </div>

      <div
        v-if="usernameMaxLengthError"
        class="text-danger text-left mt-2" 
      >
        Användarnamn kan max ha 
        {{ $v.form.username.$params.maxLength.max }} 
        antal tecken
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

      <!-- password error messages -->
      <div
        v-if="passwordRequiredError"
        class="text-danger text-left mt-2" 
      >
        Fyll i lösenord
      </div>
      
      <div
        v-if="passwordMinLengthError"
        class="text-danger text-left mt-2" 
      >
        Lösenord måste ha minst 
        {{ $v.form.password.$params.minLength.min }} 
        antal tecken
      </div>

      <div
        v-if="passwordMaxLengthError"
        class="text-danger text-left mt-2"
      >
        Lösenordet kan max ha 
        {{ $v.form.password.$params.maxLength.max }} 
        antal tecken
      </div>
    </b-form-group>

    <!-- confirm password input -->
    <b-form-group>
      <b-input-group>
        
        <b-input-group-prepend is-text>
          <b-icon icon="lock-fill"></b-icon>
        </b-input-group-prepend>
        
        <b-form-input
          placeholder="Bekräfta lösenord"
          type="password"
          :state="confirmPasswordState"
          v-model.trim="$v.form.confirmPassword.$model"
        ></b-form-input>

      </b-input-group>

      <!-- confirm password error messages -->
      <div
        v-if="confirmPasswordRequiredError"
        class="text-danger text-left mt-2" 
      >
        Bekräfta lösenord
      </div>

      <div
        v-if="confirmPasswordSameError"
        class="text-danger text-left mt-2" 
      >
        Lösenorden stämmer inte överens
      </div>
    </b-form-group>
    
    <!-- Register button -->
    <b-button
      size="lg"
      variant="info"
      block
      :disabled="$v.form.$invalid || !sameAsPassword"
      @click="onRegister"
    >
      Registrera
    </b-button>

    <!-- switch over to Login -->
    <p class="text-left mt-3">
      Har du redan ett konto? 
      
      <b-link
        class="text-info" 
        @click="onLogin"
      >
        Logga in
      </b-link>

    </p>
  </b-form>
</template>


<script>
// Vuelidate form validation package
import { required, email, minLength, maxLength} from 'vuelidate/lib/validators'

export default {
  name: "RegisterForm",
  data() {
    return {
      form: {
        email: '',
        username: '',
        password: '',
        confirmPassword: ''
      },
    }
  },
  validations: {
    form: {
      email: {
        required,
        email
      },
      // the max and min length has only been used for testing
      // please change them into something more appropriate
      username: {
        required,
        minLength: minLength(2), 
        maxLength: maxLength(20) 
      },
      password: {
        required, 
        minLength: minLength(3),
        maxLength: maxLength(20) 
      },
      confirmPassword: {
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

    usernameState() {
      if (!this.$v.form.username.$dirty) {
        return null
      }
      else {
        return !this.$v.form.username.$invalid
      }
    },

    usernameRequiredError() {
      return this.$v.form.username.$dirty &&
             !this.$v.form.username.required
    },

    usernameMinLengthError() {
      return this.$v.form.username.$dirty && 
             !this.$v.form.username.minLength
    },

    usernameMaxLengthError() {
      return this.$v.form.username.$dirty && 
             !this.$v.form.username.maxLength
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
    },

    passwordMinLengthError() {
      return this.$v.form.password.$dirty && 
             !this.$v.form.password.minLength
    },

    passwordMaxLengthError() {
      return this.$v.form.password.$dirty && 
             !this.$v.form.password.maxLength
    },

    //these last two check if the confirmed password and password are the same
    confirmPasswordState() {
      if (!this.$v.form.confirmPassword.$dirty) {
        return null
      }
      else {
        return !this.$v.form.confirmPassword.$invalid && 
               this.sameAsPassword
      }
    },

    confirmPasswordRequiredError() {
      return this.$v.form.confirmPassword.$dirty && 
             !this.$v.form.confirmPassword.required
    },
    
    confirmPasswordSameError() {
      return this.$v.form.confirmPassword.$dirty && 
             !this.sameAsPassword && 
             this.$v.form.confirmPassword.required
    },
    sameAsPassword() {
      return this.form.confirmPassword === this.form.password;
    }

  },
  methods: {
    // Passes on information to LoginArea to take care of the login and register logic
    onLogin() {
      this.$emit('login-pressed');
    },

    onRegister() {
      this.$emit('register-pressed', this.form);
    }

  }
  
}
</script>

<style scoped>
</style>