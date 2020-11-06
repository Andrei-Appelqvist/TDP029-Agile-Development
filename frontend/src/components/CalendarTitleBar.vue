<template>
    <b-row>
      <b-col 
        md="10" 
        offset-md="1"
      >
        <div class="bg-white p-2 mb-1 border-bottom">
          
          <b-container 
            class="mb-n1" 
            fluid
          >
            <b-row class="align-items-center">
              
              <!-- Column containing all headings -->
              <b-col 
                sm="10" 
                cols="9"
              >
                <b-row class="align-items-center">
                  
                  <b-col 
                    md="4" 
                    cols="12"
                  >
                    <h6 class="mb-n1 d-inline-block">
                      Träningstyp
                    </h6>
                  </b-col>
                  
                  <b-col 
                    md="4" 
                    cols="6"
                  >
                    <h6 class="mb-n1 d-inline-block">
                      Tid
                    </h6>
                  </b-col>

                  <b-col 
                    md="4" 
                    cols="6"
                  >
                    <h6 class="mb-n1 d-inline-block">
                      Plats
                    </h6>
                  </b-col>
                </b-row>
              </b-col>
              
              <!-- Column containing add workout button -->
              <b-col 
                sm="2" 
                cols="3"
              >
                <b-row class="align-items-center">
                    
                  <b-col
                    class="text-right ml-2"
                    cols="12"
                  >

                    <!-- this button presents a pop-up for adding workouts -->
                    <b-icon 
                      id="add-workout-button" 
                      class="mr-3"
                      v-b-modal.add-workout
                      v-b-tooltip.hover title="Lägg till träningspass" 
                      icon="plus-square-fill"
                      shift-v="-1"
                    ></b-icon>

                  </b-col>
                </b-row>
              </b-col>
            </b-row>
          </b-container>
        </div>
      </b-col>

      <!-- This is the modal opened by the button above, contains a form to add a workout -->
      <b-modal 
        id="add-workout" 
        size="md" 
        hide-footer 
        title="Lägg till träningspass"
      >
        <CalendarAddWorkoutForm
          @successfully-added-workout="$emit('update-workouts')"
          @logout-user="$emit('logout-user')"
          @error-occurred="emitError"
        />
      </b-modal>

    </b-row>
</template>

<script>
// Components
import CalendarAddWorkoutForm from '../components/CalendarAddWorkoutForm.vue'

export default {
  name: 'CalendarTitleBar',
  components: {
    CalendarAddWorkoutForm
  },
  
  methods: {

    // Sends error information up to CalendarSection.vue if any error has occurred
    emitError(errorTitle, errorMessage) {
      this.$emit('error-occurred', errorTitle, errorMessage)
    }
  }
}
</script>

<style scoped>
h6 {
  font-size: 0.9rem;
}

#add-workout-button {
  width: 25px;
  height: 25px;
  color: #6b757c;
}

#add-workout-button:hover {
  color: #535b62;
  cursor: pointer;
}

#add-workout-button:focus {
  outline: none;
}
</style>