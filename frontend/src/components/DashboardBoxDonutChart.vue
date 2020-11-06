<template>
  <b-card
    class="mb-3"
    style="height: 590px;"
    ref="donutCard"
    no-body
    @mousemove="updateOtherTypesTooltipPosition"
  >
    <b-card-header header-bg-variant="white">

      <b-row class="align-items-center">
        <b-col cols="12">
          
          <h5 class="mb-0">{{ boxTitle }}</h5>
        
        </b-col>
      </b-row>
    </b-card-header>

    <b-card-body>

      <!-- Donut Chart -->
      <v-chart
        :options="chartOptionsData"
        :autoresize="true"
        @mouseover="checkOtherTypesTooltip"
        @mouseout="removeOtherTypesTooltip"
      />

      <!-- Other workout types custom made tooltip to show all -->
      <!-- types that have been put in the other category -->
      <div
        v-if="otherTypesTooltipActive"
        class="rounded"
        :style="otherTypesTooltipStyle"
      >
        <span :style="otherTypesColorMarkerStyle"></span>

        <span class="tooltiptext">
          Övrigt: {{ otherTypesTimeSum }} min, {{ otherTypesPercentage }}%
        </span>
        
        <p 
          v-for="(type, index) in otherTypes" 
          :key="index"
          class="tooltiptext"
        >
          {{ type }}
        </p>
      </div>

    </b-card-body>

    <b-card-footer
      class="pt-0"
      footer-bg-variant="white" 
      footer-border-variant="white"
    >
      <p 
        class="mb-0 text-center text-muted"
        style="font-size: 0.8em"
      >
        {{ timeSpan }}
      </p>
    </b-card-footer>

  </b-card>
</template>

<script>

export default {
  name: 'DashboardBoxDonutChart',
  props: {
    boxTitle: String,
    chartData: Object,
  },
  data() {
    return {

      otherTypesTooltipActive: false,
      otherTypesTimeSum: 0,
      otherTypesPercentage: 0,

      // Used as the color dot before the other type tooltip
      // This is to mimic the look of the echarts library
      otherTypesColorMarkerStyle: {
        'display': 'inline-block',
        'margin-right': '5px',
        'border-radius': '10px',
        'width': '10px',
        'height': '10px',
        'background-color': '#fff'
      },

      // Used as the style of the custom tooltip
      // This is to mimic the look of the echarts library
      otherTypesTooltipStyle: {
        'display': 'inline-block',
        'padding': '5px',
        'background-color': 'rgba(50,50,50,0.7)',
        'position': 'fixed',
        'top': '500px',
        'left': '50px',
        'z-index': '2'
      },

      options: {
        tooltip: {},
        legend: {
          top: 12,
          itemGap: 10,
          itemWidth: 24,
          itemHeight: 20,
          textStyle: {
            fontSize: 14,
          }
        },
        color: [
          '#00a2b6', 
          '#00697a', 
          '#ff4a4c', 
          '#ffb467', 
          '#66b477', 
          '#478553', 
          '#DEE3E5', 
          '#9CA3A8', 
          '#6b757c',
        ],
        series: [{
          type: 'pie',
          radius: ['40%', '80%'],
          center: ['50%', '56%'],
          top: 20,
          label: {
            show: false
          },
          data: [{ name: 'Inga Träningspass', value: 1}]
        }],
      }
    }
  },
  computed: {

    // Adds the statistics data into the options object that the echart is using
    chartOptionsData() {
      
      let chartOptions = this.options
      let formattedData = []

      if (this.chartData.minutes != undefined) {
        
        for (let [index, dataObject] of this.chartData.minutes.entries()) {
          
          dataObject.tooltip = {}
          dataObject.tooltip.formatter = `<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:${chartOptions.color[index]};"></span>{b}: {c} min, {d}%`
          formattedData.push(dataObject)
        }
      }

      if (formattedData.length != 0) {
        chartOptions.series[0].data = formattedData
      }

      if (this.chartData.misc_labels != undefined &&
          this.chartData.misc_labels.length != 0) {

        let lastIndex = chartOptions.series[0].data.length - 1
        chartOptions.series[0].data[lastIndex].tooltip.extraCssText = 'visibility: hidden;'
      }

      return chartOptions
    },

    // If there is no date a default value is displayed
    timeSpan() {

      if (this.chartData.minutes != undefined) {
        return this.chartData.dates
      }

      return ''
    },

    // A list of the workout types that have been put into the other category
    otherTypes() {
      
      if (this.chartData.misc_labels != undefined) {
        return this.chartData.misc_labels
      }

      return []
    }

  },

  watch: {

    // Used to fill in information about the other category tooltip if there is one
    chartData(newChartData) {
      
      if (newChartData.misc_labels != undefined && 
          newChartData.misc_labels.length != 0) {

        let lastIndex = newChartData.minutes.length - 1
        this.otherTypesColorMarkerStyle['background-color'] = this.options.color[lastIndex]
        this.otherTypesTimeSum = newChartData.minutes[lastIndex].value
        this.otherTypesPercentage = Math.round((this.otherTypesTimeSum / newChartData.tot_minutes) * 10000) / 100
      }
    }
  },

  methods: {
    
    // Listens for a event hovering over a category and sets a boolean 
    // to true so that the custom tooltip can be shown
    checkOtherTypesTooltip(object) {
      if (object.name === 'Övrigt') {
        this.otherTypesTooltipActive = true
      }
    },

    // Listens to an event where the mouse pointer moves out of hovering over a category
    // Used to remove the custom tooltip
    removeOtherTypesTooltip() {
      this.otherTypesTooltipActive = false
    },

    // Listens to an event where the mouse moves and changes position
    // of the custom tooltip to mimic the behaviour of echarts tooltips
    updateOtherTypesTooltipPosition(object) {
      
      if (this.otherTypesTooltipActive) {

        if (object.clientX < (this.$refs.donutCard.clientWidth / 2) + 20) {
          this.otherTypesTooltipStyle['top'] = (object.clientY + 20).toString() + 'px'
          this.otherTypesTooltipStyle['left'] = (object.clientX + 20).toString() + 'px'

        } else {
          this.otherTypesTooltipStyle['top'] = (object.clientY + 20).toString() + 'px'
          this.otherTypesTooltipStyle['left'] = (object.clientX - 140).toString() + 'px'
        }
      }

    }
  }
}
</script>

<style scoped>
.echarts {
  width: 100%;
  height:100%;
}

.tooltiptext {
  font-size: 0.82em;
  color: white;
  margin: 0;
  padding: 0;
}
</style>