<template>
  <b-container fluid="lg">
    <b-row 
      id="welcome-row" 
      class="align-items-center"
    >
      <b-col 
        id="welcome-col"
        class="mx-auto"
        md="6"
      >
        <!-- Card containing welcome message -->
        <b-card class="text-center">

          <h2>Välkommen till din Träningsdagbok!</h2> 
          
          <p>För att använda träningsdagboken behöver du först koppla ditt gymsystem-konto genom att trycka på knappen nedan</p>
          
          <!-- Button which activates a modal containing the form to connect to gymsystem -->
          <b-button
            class="d-inline-block ml-2 mr-3 mb-3"
            variant="info" 
            size="lg"
            v-b-modal.connect-gymsystem
          >
            Koppla
          </b-button>
          
          <!-- Modal containing the form to connect to gymsystem -->
          <b-modal 
            id="connect-gymsystem" 
            title="Koppla till Gymsystem"
            hide-footer
          >
            <ConnectGymsystemForm
              @gymsystem-connected="$emit('goto-dashboard')"
              @error-occurred="emitError"
            />

          </b-modal>

        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>


<script>
//Components
import ConnectGymsystemForm from '../components/ConnectGymsystemForm.vue'

export default {
  name: "WelcomeSection",
  components: {
    ConnectGymsystemForm
  },

  methods: {
    // Sends error information up to UserArea.vue if any error has occurred
    emitError(errorTitle, errorMessage) {
      this.$emit('error-occurred', errorTitle, errorMessage)
    }
  }
}
</script>

<style scoped>
#welcome-row {
  height: 90vh;
}

#welcome-col {
  height: 400px;
}
</style>