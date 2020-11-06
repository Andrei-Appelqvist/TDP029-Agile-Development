<template>
  <b-form 
    @:submit.prevent
    @keyup.enter="addWorkout"
  >
    <!-- Choose date -->
    <b-form-group>
      
      <b-form-datepicker
        placeholder="Välj ett datum"
        locale="sv"
        start-weekday="1"
        :max="currentDate"
        :state="dateInputState"
        v-bind="svDatepicker"
        v-model="$v.form.date.$model"
        @hidden="onDateTouched"
      ></b-form-datepicker>

      <!-- Date error message -->
      <div
        v-if="dateInputRequiredError"
        class="text-danger text-left mt-2" 
      >
        Du måste välja ett datum
      </div>
    </b-form-group>

    <!-- Enter workout type -->
    <b-form-group>
      <b-form-input
        placeholder="Välj eller skriv in en träningstyp"
        list="type-list"
        autocomplete="false"
        :state="typeInputState"
        v-model="$v.form.type.$model"
        @blur="onTypeTouched"
      >
      </b-form-input>

      <b-datalist
        id="type-list"
        :options="workoutTypes"
      ></b-datalist>

      <!-- Workout type error messages -->
      <div
        v-if="typeInputRequiredError"
        class="text-danger text-left mt-2" 
      >
        Du måste välja eller skriva in en träningstyp
      </div>

      <div
        v-if="typeInputMaxLengthError"
        class="text-danger text-left mt-2" 
      >
        För många tecken
      </div>
    </b-form-group>

    <b-container>
      <b-row>
        <b-col 
          class="px-0" 
          cols="5"
        >
          <!-- Choose start time -->
          <b-form-group>
            
            <b-form-timepicker
              placeholder="Välj starttid"
              now-button
              now-button-variant="outline-secondary"
              close-button-variant="info"
              locale="sv"
              :hour12="false"
              :state="startInputState"
              v-bind="svTimepicker"
              v-model="$v.form.startTime.$model"
              @hidden="onStartTouched"
            ></b-form-timepicker>

            <!-- Start time error messages -->
            <div
              v-if="startInputRequiredError"
              class="text-danger text-left mt-2" 
            >
              Du måste välja en starttid
            </div>

            <div
              v-if="startInputLessThanEndError"
              class="text-danger text-left mt-2" 
            >
              Sätt tidigare än sluttid
            </div>
          </b-form-group>
        </b-col>

        <b-col 
          class="text-center"
          cols="2"
        >
          <b-icon 
            class="text-secondary" 
            icon="dash" 
            shift-v="-4" 
            style="width: 26px; height: 26px;"
          ></b-icon>
        </b-col>

        <b-col 
          class="px-0" 
          cols="5"
        >
          <!-- Choose end time -->
          <b-form-group>
            
            <b-form-timepicker
              placeholder="Välj sluttid"
              now-button
              now-button-variant="outline-secondary"
              close-button-variant="info"
              locale="sv"
              :hour12="false"
              :state="endInputState"
              v-bind="svTimepicker"
              v-model="$v.form.endTime.$model"
              @hidden="onEndTouched"
            ></b-form-timepicker>

            <!-- End time error messages -->
            <div
              v-if="endInputRequiredError"
              class="text-danger text-left mt-2" 
            >
              Du måste välja en sluttid
            </div>

            <div
              v-if="endInputMoreThanStartError"
              class="text-danger text-left mt-2" 
            >
              Sätt senare än starttid
            </div>
          </b-form-group>
        </b-col>
      </b-row>
    </b-container>

    <!-- Enter location -->
    <b-form-group>
      
      <b-form-input
        placeholder="Skriv in en plats"
        :state="locationInputState"
        v-model="$v.form.location.$model"
      ></b-form-input>

      <!-- Location error messages-->
      <div
        v-if="locationInputMaxLengthError"
        class="text-danger text-left mt-2" 
      >
        För många tecken
      </div>
    </b-form-group>

    <!-- Enter Description -->
    <b-form-group>
      
      <b-form-textarea
        placeholder="Skriv en beskrivning..."
        rows="3"
        no-resize
        :state="descriptionInputState"
        v-model="$v.form.description.$model"
      ></b-form-textarea>

      <div
        v-if="descriptionInputMaxLengthError"
        class="text-danger text-left mt-2" 
      >
        För många tecken
      </div>
    </b-form-group>

    <!-- Button to add workout when form is filled out -->
    <b-button
      class="mb-3"
      variant="info"
      block
      :disabled="$v.form.$invalid"
      @click="addWorkout"
    >
      Lägg till
    </b-button>

    <!-- Success and error messages after add workout attempt -->
    <div
      v-if="showSuccess"
      class="alert alert-success mb-0 mt-3 mx-auto" 
      role="alert"
    >
      Träningspass är tillagt
    </div>

    <div
      v-if="showError"
      class="alert alert-danger mb-0 mt-3 mx-auto" 
      role="alert"
    >
      {{ errorMessage }}
    </div>

  </b-form>
</template>


<script>
// Services
import WorkoutService from '../services/WorkoutService.js'

// Vuelidate form validation package
import { required, maxLength} from 'vuelidate/lib/validators'

// Custom validators
function lessThanEnd(value) {
  
  if (this.form.endTime != '') {
    return value < this.form.endTime
  }

  return true
}

function moreThanStart(value) {
  
  if (this.form.startTime != '') {
    return value > this.form.startTime
  }

  return true
}


export default {
  name: "CalendarAddWorkoutForm",
  data() {
    return {
      form: {
        date: '',
        type: '',
        startTime: '',
        endTime: '',
        location: '',
        description: ''
      },

      showSuccess: false,
      showError: false,
      errorMessage: '',

      currentDate: '',

      workoutTypes: [],

      svDatepicker: {
        labelPrevDecade: 'Föregående årtionde',
        labelPrevYear: 'Föregående år',
        labelPrevMonth: 'Föregående månad',
        labelCurrentMonth: 'Nuvarande månad',
        labelNextMonth: 'Nästa månad',
        labelNextYear: 'Nästa år',
        labelNextDecade: 'Nästa årtionde',
        labelToday: 'Idag',
        labelSelected: 'Valt datum',
        labelNoDateSelected: 'Inget valt datum',
        labelCalendar: 'Kalender',
        labelNav: 'Kalendernavigation',
        labelHelp: 'Använd pilarna ovan för att navigera kalendern'
      },

      svTimepicker: {
        labelHours: 'Timmar',
        labelMinutes: 'Minuter',
        labelSeconds: 'Sekunder',
        labelIncrement: 'Öka',
        labelDecrement: 'Minska',
        labelSelected: 'Vald tid',
        labelNoTimeSelected: 'Ingen tid vald',
        labelCloseButton: 'OK',
        labelNowButton: 'Sätt nu'
      },
    }
  },
  // Might want to add a better max length for type, location and description
  validations: {
    form: {
      date: {
        required
      },
      type: {
        required,
        maxLength: maxLength(40) 
      },
      startTime: {
        required,
        lessThanEnd
      },
      endTime: {
        required,
        moreThanStart
      },
      location: {
        maxLength: maxLength(40) 
      },
      description: {
        maxLength: maxLength(300) 
      }
    }
  },

  // Responsively computing if any validation error or state change has occurred
  computed: {

    dateInputState() {
      if (!this.$v.form.date.$dirty) {
        return null
      }
      else {
        return !this.$v.form.date.$invalid
      }
    },

    dateInputRequiredError() {
      return this.$v.form.date.$dirty && 
             !this.$v.form.date.required
    },

    typeInputState() {
      if (!this.$v.form.type.$dirty) {
        return null
      }
      else {
        return !this.$v.form.type.$invalid
      }
    },

    typeInputRequiredError() {
      return this.$v.form.type.$dirty && 
             !this.$v.form.type.required
    },

    typeInputMaxLengthError() {
      return this.$v.form.type.$dirty && 
             !this.$v.form.type.maxLength
    },

    startInputState() {
      if (!this.$v.form.startTime.$dirty) {
        return null
      }
      else {
        return !this.$v.form.startTime.$invalid
      }
    },

    startInputRequiredError() {
      return this.$v.form.startTime.$dirty && 
             !this.$v.form.startTime.required
    },

    startInputLessThanEndError() {
      return this.$v.form.startTime.$dirty && 
             !this.$v.form.startTime.lessThanEnd
    },

    endInputState() {
      if (!this.$v.form.endTime.$dirty) {
        return null
      }
      else {
        return !this.$v.form.endTime.$invalid
      }
    },

    endInputRequiredError() {
      return this.$v.form.endTime.$dirty && 
             !this.$v.form.endTime.required
    },

    endInputMoreThanStartError() {
      return this.$v.form.endTime.$dirty && 
             !this.$v.form.endTime.moreThanStart
    },

    locationInputState() {
      if (!this.$v.form.location.$invalid) {
        return null
      }
      else {
        return false
      }
    },

    locationInputMaxLengthError() {
      return this.$v.form.location.$dirty && 
             !this.$v.form.location.maxLength
    },

    descriptionInputState() {
      if (!this.$v.form.description.$invalid) {
        return null
      }
      else {
        return false
      }
    },

    descriptionInputMaxLengthError() {
      return this.$v.form.description.$dirty && 
             !this.$v.form.description.maxLength
    }

  },

  // Checks the current date to use as a limit for calendar date choice in the form
  // Fetches the workout types to use as suggestions
  async created() {

    this.currentDate = new Date()

    let response = await WorkoutService.getAllWorkoutTypes()

    if (response.status === 200) {
      this.workoutTypes = response.data

    } else if (response.status === 401) {
      this.$emit('logout-user')

    } else {
      this.$emit('error-occurred', response.status.toString(), 'Oväntat fel har uppstått')
    }
  },

  methods: {

    // Creates and adds a new workout to the backend with given form data
    async addWorkout() {
      this.showError = false;
      this.showSuccess = false;
      this.errorMessage = '';
      
      let new_workout = {
        workout_name: this.form.type,
        start_time: this.form.date + " " + this.form.startTime,
        end_time: this.form.date + " " + this.form.endTime,
        location: this.form.location,
        description: this.form.description
      }

      let response = await WorkoutService.addWorkout(new_workout);

      if (response.status === 200) {
        this.showSuccess = true

        this.$v.form.$reset()
        this.form.type = '';
        this.form.date = '';
        this.form.startTime = '';
        this.form.endTime = '';
        this.form.location = '';
        this.form.description = '';

        this.$emit('successfully-added-workout')

      } else if (response.status === 401) {
        this.$emit('logout-user')

      } else {
        this.showError = true;
        this.errorMessage = 'Oväntat fel'
        this.$emit('error-occurred', response.status.toString(), 'Oväntat fel har uppstått')
      }
    },

    // Used to provide validation error when opening calendar- and 
    // time-picker and then not entering a value
    onDateTouched() {
      this.$v.form.date.$touch()
    },

    onTypeTouched() {
      this.$v.form.type.$touch()
    },

    onStartTouched() {
      this.$v.form.startTime.$touch()
    },
    
    onEndTouched() {
      this.$v.form.endTime.$touch()
    },
  },
}
</script>

<style scoped>

</style>