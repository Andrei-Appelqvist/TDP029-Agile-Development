<template>
  <b-card
    class="mb-3"
    no-body
  >
    <b-card-header header-bg-variant="white">

      <b-row class="align-items-center">
        
        <b-col cols="6">
          
          <h5 class="mb-0">{{ boxTitle }}</h5>
        
        </b-col>
        

        <b-col
          class="text-right"
          cols="6"
        >
          <DashboardBoxSwitcher
            v-if="isConnected"
            :serviceList="connectedHealthServices"
            :activeService="displayedService"
            @switch-service="switchDisplayedService"
          />
        
        </b-col>
      
      </b-row>
    </b-card-header>

    <b-card-body class="p-3">

      <div v-if="isConnected">
        
        <!-- Headings -->
        <b-row>
        
          <b-col
            class="text-center"
            cols="6"
          >
            <p class="text-muted">Idag</p>
          </b-col>
        
          <b-col
            class="text-center"
            cols="6"
          >
            <p class="text-muted">Totalt</p>
          </b-col>

        </b-row>

        <!-- Values -->
        <b-row class="pb-n1">
        
          <b-col
            class="text-center"
            cols="6"
          >
            <h3>{{todayData}} {{unit}}</h3>
          </b-col>
        
          <b-col
            class="text-center"
            cols="6"
          >
            <h3>{{totalData}} {{unit}}</h3>
          </b-col>

        </b-row>
      </div>

      <!-- Only shown when no third party health service is connected -->
      <b-row 
        v-if="!isConnected" 
        class="align-items-center" 
        style="height: 100%;"
      >
        <b-col class="text-center">
            
          <b-button  
            class="mx-auto" 
            variant="info"
            size="lg"
            @click="$emit('goto-user-settings')"
          >
            Koppla till en hälsotjänst
          </b-button>
        </b-col>
      </b-row>

    </b-card-body>

    <b-card-footer
      class="pt-0"
      footer-bg-variant="white" 
      footer-border-variant="white"
    >
      <p
        v-if="isConnected"
        class="mb-0 text-center text-muted"
        style="font-size: 0.8em"
      >
        {{ timeSpan }}
      </p>
    </b-card-footer>


  </b-card>
</template>

<script>
// Components
import DashboardBoxSwitcher from '../components/DashboardBoxSwitcher.vue'

export default {
  name: 'DashboardBoxTotalDaily',
  components: {
    DashboardBoxSwitcher
  },
  props: {
    boxTitle: String,
    data: Object,
    unit: String,
    connectedHealthServices: Array
  },
  data() {
    return {
      displayedService: ''
    }
  },
  computed: {

    // Reformatting data for displaying
    todayData() {
      
      if (this.data[this.displayedService].data.length != 0) {
        
        return this.data[this.displayedService].data[this.data[this.displayedService].data.length - 1].toFixed(0)
      }

      return 0
    },

    // Reformatting data for displaying
    totalData() {
      
      if (this.data[this.displayedService].data.length != 0) {
        
        return this.data[this.displayedService].data.reduce((a,b)=> a+b,0).toFixed(0)
      }

      return 0
    },

    // If there is no date a default value is displayed
    timeSpan() {
      
      if (this.data[this.displayedService].dates.length != 0) {
        
        let startDate = this.data[this.displayedService].dates[0]
        
        let endDate = this.data[this.displayedService].dates[
                      this.data[this.displayedService].dates.length - 1]
        
        return `${startDate} - ${endDate}`
      }
      return ''
    },

    // Simple check if any third party health services are connected
    isConnected() {
      return this.connectedHealthServices.length != 0
    }

  },

  // Initiates variables
  created() {
    if (this.isConnected) {
      this.displayedService = this.connectedHealthServices[0]
    }
  },
  
  methods: {

    // Switching to another health service data
    switchDisplayedService(service) {
      this.displayedService = service
    }

  }

}
</script>

<style scoped>

</style>