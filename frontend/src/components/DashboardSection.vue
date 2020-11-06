<template>
  <b-container
    class="px-4 py-3"
    fluid
  >
    <b-row>
      <!-- First column -->
      <b-col
        class="px-2"
        cols="12"
        md="6"
        xl="4"
      >
        <DashboardBoxDonutChart
          :boxTitle="'Träningstyp'"
          :chartData="workoutTypeData"
        />

      </b-col>

      <!-- Second column -->
      <b-col
        class="px-2"
        cols="12"
        md="6"
        xl="4"
      >
        <DashboardBoxTotalDaily
          :boxTitle="'Steg'"
          :data="monthlyStepsData"
          :unit="''"
          :connectedHealthServices="connectedHealthServices"
          @goto-user-settings="$emit('change-state', 'settings')"
        />

        <DashboardBoxBarChart
          :boxTitle="'Steg över tid'"
          :data="monthlyStepsData"
          :unit="{ name: 'steg', shortened: 'steg' }"
          :connectedHealthServices="connectedHealthServices"
          @goto-user-settings="$emit('change-state', 'settings')"
        />
        
      </b-col>

      <!-- Third column -->
      <b-col
        class="px-2"
        cols="12"
        md="6"
        xl="4"
      >
        <DashboardBoxTotalDaily
          :boxTitle="'Distans'"
          :data="monthlyDistanceData"
          :unit="'m'"
          :connectedHealthServices="connectedHealthServices"
          @goto-user-settings="$emit('change-state', 'settings')"
        />
        
        <DashboardBoxBarChart
          :boxTitle="'Distans över tid'"
          :data="monthlyDistanceData"
          :unit="{ name: 'meter', shortened: 'm' }"
          :connectedHealthServices="connectedHealthServices"
          @goto-user-settings="$emit('change-state', 'settings')"
        />

      </b-col>

    </b-row>
  </b-container>
</template>

<script>
//Components
import DashboardBoxDonutChart from '../components/DashboardBoxDonutChart.vue'
import DashboardBoxBarChart from '../components/DashboardBoxBarChart.vue'
import DashboardBoxTotalDaily from '../components/DashboardBoxTotalDaily.vue'

// Services
import UserService from '../services/UserService.js'
import WorkoutService from '../services/WorkoutService.js'

export default {
  name:'DashboardSection',
  components: {
    DashboardBoxDonutChart,
    DashboardBoxBarChart,
    DashboardBoxTotalDaily
  },
  props: {
    currentWeek: Number,
    currentYear: Number,
    connectedHealthServices: Array
  },
  data() {
    return {
      workoutTypeStats: {},
      stepsDistanceStats: {
        google: null,
        zoezi: null
      }
    }
  },
  computed: {

    // Functions that reformat statistics data into new datastructures 
    // that fit with the echart library

    workoutTypeData() {

      if (this.workoutTypeStats.minutes != undefined) {

        let data = this.workoutTypeStats
        let typeMinutes = []
        
        for (let entry of Object.entries(this.workoutTypeStats.minutes)) {
          
          let dataObject = {}
          
          dataObject.name = entry[0]
          dataObject.value = entry[1]
          
          typeMinutes.push(dataObject)
        }
        
        data.minutes = typeMinutes
        return data
      }
      return this.workoutTypeStats
    },

    monthlyStepsData() {
      
      let data = {}

      for (let service of this.connectedHealthServices) {
        data[service] = {
          dates: [],
          data: [],
        }
        
        if (this.stepsDistanceStats[service] != null) {
          data[service].dates = this.stepsDistanceStats[service].dates
          data[service].data = this.stepsDistanceStats[service].steps
        }
      }

      return data
    },

    weeklyStepsData() { // Not currently in use
      
      let data = {}

      for (let service of this.connectedHealthServices) {
        data[service] = {
          dates: [],
          data: [],
        }
        
        if (this.stepsDistanceStats[service] != null) {
          data[service].dates = this.stepsDistanceStats[service].dates.slice(24)
          data[service].data = this.stepsDistanceStats[service].steps.slice(24)
        }
      }

      return data
    },

    monthlyDistanceData() {

      let data = {}

      for (let service of this.connectedHealthServices) {
        data[service] = {
          dates: [],
          data: [],
        }
        
        if (this.stepsDistanceStats[service] != null) {
          data[service].dates = this.stepsDistanceStats[service].dates
          data[service].data = this.stepsDistanceStats[service].distance
        }
      }

      return data
    },

    weeklyDistanceData() { // Not currently in use

      let data = {}

      for (let service of this.connectedHealthServices) {
        data[service] = {
          dates: [],
          data: [],
        }
        
        if (this.stepsDistanceStats[service] != null) {
          data[service].dates = this.stepsDistanceStats[service].dates.slice(24)
          data[service].data = this.stepsDistanceStats[service].distance.slice(24)
        }
      }

      return data
    }
  },

  // Fetches all statistics data if health services are connected
  async created() {
    
    let typeResponse = await WorkoutService.getWorkoutTypeStats(this.currentYear, this.currentWeek)

    if (typeResponse.status === 200) {
      this.workoutTypeStats = typeResponse.data

    } else if (typeResponse.status === 401) {
      this.$emit('logout-user')
      
    } else {
      this.$emit('error-occurred', typeResponse.status.toString(), 'Oväntat fel har uppstått')
    }

    if (this.connectedHealthServices.length != 0) {
      
      let stepDistanceResponse = await UserService.getUserStepsDistanceStats()

      if (stepDistanceResponse.status === 200) {
        this.stepsDistanceStats = stepDistanceResponse.data

      } else if (stepDistanceResponse.status === 401) {
        this.$emit('logout-user')

      } else {
        this.$emit('error-occurred', stepDistanceResponse.status.toString(), 'Oväntat fel har uppstått')
      }
      
    }
  },
  methods: {

    // Redirects a user to the UserSettingsPage
    goToUserSettings() {
      this.$emit('change-state', 'settings')
    },

  }
}
</script>

<style scoped>
.switchbutton {
  cursor: pointer;
}
</style>