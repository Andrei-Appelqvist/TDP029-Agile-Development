<template>
  <b-container fluid="lg">
    
    <CalendarWeekSwitcher
      :year="calendarYear"
      :week="calendarWeek"
      :currentWeek="currentWeek"
      @previous-week="previousWeek"
      @next-week="nextWeek"
    />
    
    <CalendarTitleBar 
      @update-workouts="updateWorkouts"
      @logout-user="$emit('logout-user')"
      @error-occurred="emitError"
    />

    <b-row 
      v-for="(item, index) in calendarItems" 
      :key="index"
    >
      <CalendarItem 
        :itemData="item" 
        :id="index" 
      />
    </b-row>
  </b-container>
</template>


<script>
//Components
import CalendarWeekSwitcher from '../components/CalendarWeekSwitcher.vue'
import CalendarTitleBar from '../components/CalendarTitleBar.vue'
import CalendarItem from '../components/CalendarItem.vue'

//Services
import WorkoutService from '../services/WorkoutService.js'

export default {
  name: "CalendarSection",
  components: {
    CalendarWeekSwitcher,
    CalendarTitleBar,
    CalendarItem,
  },
  props: {
    currentYear: Number,
    currentWeek: Number,
  },
  data() {
    return {
      calendarYear: 0,
      calendarWeek: 0,
      workoutList: [],
      
      days: [
        'Söndag',
        'Måndag',
        'Tisdag',
        'Onsdag',
        'Torsdag',
        'Fredag',
        'Lördag'
      ],
      
      months: [
        'Januari',
        'Februari',
        'Mars',
        'April',
        'Maj',
        'Juni',
        'Juli',
        'Augusti',
        'September',
        'Oktober',
        'November',
        'December'
      ],
    }
  },
  computed: {
    
    // Creates a list of calendar items from a users workout list
    // Workouts are turned into workout type items and for every
    // specific day that there is a workout there is also a date
    // type item created and inserted before the workouts in the list
    calendarItems() {
      let itemList = []
      let prevDate = null

      for (let workout of this.workoutList) {
        let dateArray = workout.start_time.split(" ")[0].split("-")
        let dateObject = new Date(dateArray[0], dateArray[1]-1, dateArray[2])
        
        if (prevDate === null || 
            !(prevDate.getYear() === dateObject.getYear() &&
            prevDate.getMonth() === dateObject.getMonth() &&
            prevDate.getDate() === dateObject.getDate())) {
          
          let dateItem = {
            'type': 'date',
            'weekday': this.days[dateObject.getDay()],
            'dayofmonth': dateObject.getDate().toString(),
            'month': this.months[dateObject.getMonth()]
          }

          itemList.push(dateItem)
          prevDate = dateObject
        }

        workout.type = 'workout'
        
        let timeArray = workout.start_time.split(" ")[1].split(":")
        timeArray = timeArray.concat(workout.end_time.split(" ")[1].split(":"))
        
        workout.start_clock = timeArray[0] + ":" + timeArray[1]
        workout.end_clock = timeArray[3] + ":" + timeArray[4]
        
        itemList.push(workout)
      }
      
      return itemList
    },
  },

  // initiates week and year variables as well as fetches a users workouts
  async created() {
    this.calendarYear = this.currentYear
    this.calendarWeek = this.currentWeek

    await this.updateWorkouts()
  },

  methods: {

    // Fetches a list of workouts for a specific week
    async updateWorkouts() {
      
      let response = await WorkoutService.getWorkouts(this.calendarYear, this.calendarWeek)
        
      if (response.status === 200) {
        this.workoutList = response.data

      } else if (response.status === 401) {
        this.$emit('logout-user')

      } else {
        this.$emit('error-occurred', response.status.toString(), 'Oväntat fel har uppstått')
      }
    },

    // jumping to previous and next week in the calendar
    async previousWeek() {

      this.calendarWeek--
      
      if (this.calendarWeek === 0) {
        this.calendarYear--
        this.calendarWeek = 52
      }
      await this.updateWorkouts()
    },

    async nextWeek() {

      this.calendarWeek++

      if (this.calendarWeek === 53) {
        this.calendarYear++
        this.calendarWeek = 1
      }
      await this.updateWorkouts()
    },

    // Sends error information up to UserArea.vue if any error has occurred
    emitError(errorTitle, errorMessage) {
    
      this.$emit('error-occurred', errorTitle, errorMessage)
    
    }
  },
};
</script>


<style scoped>

</style>
