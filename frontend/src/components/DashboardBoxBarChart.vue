<template>
  <b-card
    class="mb-3"
    style="height: 380px"
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

        <!-- Bar chart -->
        <v-chart
          v-if="isConnected"
          :options="chartOptionsData"
          :autoresize="true"
        />

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
  name: 'DashboardBoxBarChart',
  components: {
    DashboardBoxSwitcher
  },
  props: {
    boxTitle: String,
    data: Object,
    unit: Object,
    connectedHealthServices: Array
  },
  data() {
    return {
      
      displayedService: 'google',

      options: {
        color: ['#00a2b6'],
        tooltip: {},
        xAxis: {
          type: 'category',
          axisLine: {
            lineStyle: {
              color: '#6b757c'
            }
          },
          axisTick: {
            alignWithLabel: true
          },
          axisLabel: {
            fontSize: 14,
            color: '#6b757c'
          },
          data: []
        },
        yAxis: {
          name: '',
          nameLocation: 'end',
          nameTextStyle: {
            color: '#6b757c'
          },
          axisLabel: {
            fontSize: 14,
            color: '#6b757c'
          },
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          }
        },
        grid: {
          left: 60,
          right: 20,
          top: 30,
          bottom: 28,
        },
        dataZoom: [
          {
            type: 'inside'
          }
        ],
        series: [{
          type: 'bar',
          barWidth: '60%',
          itemStyle: {
            barBorderRadius: [2,2,0,0]
          },
          data: []
        }]
      },

      months: [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'Maj',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Okt',
        'Nov',
        'Dec'
      ],
    }
  },
  computed: {

    // Adds the statistics data into the options object that the echart is using
    chartOptionsData() {

      let optionsData = this.options

      if (this.data[this.displayedService].data.length != 0 && 
          this.data[this.displayedService].dates.length != 0) {
        
        let shortenedDates = []

        this.data[this.displayedService].dates.forEach((date) => {
          
          let day = parseInt(date.split('-')[2]).toString()
          let month = this.months[parseInt(date.split('-')[1]) - 1]
          
          shortenedDates.push(`${day} ${month}`)

        })

        optionsData.xAxis.data = shortenedDates
        
        let formattedData = []

        this.data[this.displayedService].data.forEach((dataObject) => {
          
          formattedData.push({ 
            value: dataObject, 
            tooltip: {
              formatter: `<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:#00a2b6;"></span>{b}: {c} ${this.unit.shortened}`
            }
          })

        })

        optionsData.series[0].data = formattedData
      }
      return optionsData
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
      this.options.yAxis.name = this.unit.name
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
.echarts {
  width: 100%;
  height: 100%;
}
</style>