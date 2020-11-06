<template>
  <div>
    <!-- Year row -->
    <b-row>
      
      <b-col 
        class="text-center" 
        md="4" 
        offset-md="4"
      >
        <h5 class="font-weight-bold text-dark mt-4 mb-n2">
          {{ year }}
        </h5>
      </b-col>

    </b-row>

    <!-- Week row -->
    <b-row>
      <b-col 
        md="4" 
        offset-md="4"
      >
        <div 
          id="week-selector" 
          class="text-center mb-3"
        >
        <!-- Previous button -->
          <b-button
            class="d-inline-block"
            size="sm"
            @click="$emit('previous-week')"
          >
            <b-icon 
              icon="chevron-left" 
              scale="1.3" 
              shift-v="-1" 
              shift-h="-1"
            ></b-icon>
            
          </b-button>

          <h2 class="font-weight-bold text-dark d-inline-block mx-3 mt-2 align-middle">
            Vecka {{ week }}
          </h2>

          <!-- Next button -->
          <b-button
            class="d-inline-block"
            size="sm" 
            :disabled="week === currentWeek"
            @click="$emit('next-week')"
          >
            <b-icon 
              icon="chevron-right" 
              scale="1.3" 
              shift-v="-1" 
              shift-h="1"
            ></b-icon>

          </b-button>
        </div>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: 'CalendarWeekSwitcher',
  props: {
    year: Number,
    week: Number,
    currentWeek: Number
  }
}
</script>

<style scoped>
#week-selector {
  min-width: 250px;
}
</style>