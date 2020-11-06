<!-- this file contains the date of a day in the calendar, the title being used in CalendarItem -->
<template>
  <div class="text-dark py-2 px-4 my-2">
    
    <h6 class="font-weight-bold mb-n1">
      {{ itemData.weekday }}, {{ itemData.dayofmonth }} {{ itemData.month }}
    </h6>
    
  </div>
</template>

<script>
export default {
  name: 'CalendarItemDate',
  props: {
    itemData: Object
  }
}
</script>

<style scoped>
div {
  background-color: #dde2e6;
  border-bottom: 1px solid #C9CED2;
}
</style>