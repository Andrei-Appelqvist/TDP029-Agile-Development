<template>
  <b-container>
    <b-row>
      <b-col cols="12">
        <!-- Page title -->
        <b-card class="mt-3">
          <h3 class="mb-0">Användarinställningar</h3>
        </b-card>
        
        <!-- User data -->
        <b-card
          no-body
          class="mt-3"
        >
          <template v-slot:header>
            <h5 class="mb-0">Användaruppgifter</h5>
          </template>

          <b-card-body>
            <b-form>
              
              <!-- Username -->
              <b-form-group
                label="Användarnamn"
              >
                <b-input-group>
                  
                  <b-input-group-prepend is-text>
                    <b-icon icon="person-fill"></b-icon>
                  </b-input-group-prepend>

                  <b-form-input
                    class="bg-light"
                    :readonly="true"
                    v-model="user.name"
                  ></b-form-input>

                </b-input-group>
              </b-form-group>

              <!-- Email -->
              <b-form-group
                label="Epost"
              >
                <b-input-group>
                  
                  <b-input-group-prepend is-text>
                    <b-icon icon="envelope-fill"></b-icon>
                  </b-input-group-prepend>
                  
                  <b-form-input
                    class="bg-light"
                    :readonly="true"
                    v-model="user.email"
                  ></b-form-input>

                </b-input-group>
              </b-form-group>
            </b-form>
          </b-card-body>
        </b-card>


        <!-- Health services -->
        <b-card
          no-body
          class="mt-3"
        >
          <template v-slot:header>
            <h5 class="mb-0">Hälsotjänster</h5>
          </template>

          <b-card-body>
            <b-form>
              
              <!-- Google -->
              <b-form-group
                label="Google Fit"
              >
                <b-button
                  variant="info"n
                  :disabled="user.connectedHealthServices.includes('google')"
                  @click="connectGoogle"
                >
                  {{ googleButtonText }}
                </b-button>

              </b-form-group>
              
              <!-- Fitbit -->
              <b-form-group
                label="Fitbit"
              >
                <b-button
                  variant="info"
                  :disabled="user.connectedHealthServices.includes('fitbit')"
                  @click="connectFitbit"
                >
                  {{ fitbitButtonText }}
                </b-button>
                
              </b-form-group>
            </b-form>
          </b-card-body>
        </b-card>
      </b-col>
    </b-row>

    <b-row>
      <b-col 
        class="d-flex justify-content-end" 
        cols="12"
      >
        <!-- Logout Button -->
        <b-button
          class="mt-3"
          variant="secondary"
          size="lg"
          @click="$emit('logout-user')"
        >
          Logout
        </b-button>

      </b-col>
    </b-row>
    
  </b-container>
</template>

<script>

export default {
  name: 'UserSettingsSection',
  props: {
    user: Object
  },

  // Responsively checking if a health service is connected 
  // and then returns the correct text
  computed: {

    googleButtonText() {
      if (this.user.connectedHealthServices.includes('google')) {
        return 'Du är kopplad till ett Google Fit-konto'

      } else {
        return 'Koppla till ett Google Fit-konto'
      }
    },

    fitbitButtonText() {
      if (this.user.connectedHealthServices.includes('fitbit')) {
        return 'Du är kopplad till ett Fitbit-konto'
        
      } else {
        return 'Koppla till ett Fitbit konto'
      }
    }
  },

  methods: {

    // Redirects the user to a third party health service to connect to the app

    connectGoogle() {
      window.location.href = "<enter link to oauth consent page for google>"
    },

    connectFitbit() {
      window.location.href = "<enter link to oauth consent page for fitbit>"
    },
  },

}
</script>

<style scoped>

</style>