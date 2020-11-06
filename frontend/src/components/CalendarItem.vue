<template>
  <b-col 
    md="10" 
    offset-md="1"
  >
    <!-- Shows only one depending on the type of the item -->
    <CalendarItemDate
      v-if="itemData.type === 'date'"
      :itemData="itemData"
    />

    <CalendarItemWorkout
      v-if="itemData.type === 'workout'"
      :id="id"
      :itemData="itemData"
    />

  </b-col>
</template>

<script>
// Components
import CalendarItemDate from '../components/CalendarItemDate.vue'
import CalendarItemWorkout from '../components/CalendarItemWorkout.vue'

export default {
  name: 'CalendarItem',
  components: {
    CalendarItemDate,
    CalendarItemWorkout
  },
  props: {
    itemData: Object,
    id: Number
  }
}
</script>

<style scoped>

</style>