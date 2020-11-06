<template>
  <div class="mb-2">
    
    <div :class="headerClass">
      
      <!-- Using the same grid structure as the CalendarTitleBar for matching with headings -->
      <b-container 
        class="mb-n1" 
        fluid
      >
        <b-row class="align-items-center">
          
          <b-col 
            sm="10" 
            cols="9"
          >
            <b-row class="align-items-center">
              
              <b-col 
                md="4" 
                cols="12"
              >
                <h6 class="mb-n3 d-inline-block font-weight-bold">
                  {{ itemData.workout_name }}
                </h6>

              </b-col>

              <b-col 
                md="4" 
                cols="6"
              >
                <p class="mb-n3 d-inline-block font-weight-bold ">
                  {{ itemData.start_clock }} - {{ itemData.end_clock }}
                </p>

              </b-col>
              
              <b-col 
                md="4" 
                cols="6"
              >
                <p class="mb-n3 d-inline-block font-weight-bold">
                  {{ location }}
                </p>
              
              </b-col>
            </b-row>
          </b-col>

          <b-col 
            sm="2" 
            cols="3"
          >
            <b-row class="align-items-center">
              
              <b-col
                class="text-right"
                cols="12" 
              >
                <!-- Open and collapse button -->
                <b-button 
                  class="d-inline-block ml-3" 
                  size="sm"
                  v-b-toggle="'collapse-'+ id.toString()"
                  :variant="buttonVariant" 
                >
                  <b-icon 
                    icon="chevron-down" 
                    shift-v="-2"
                  ></b-icon>

                </b-button>

              </b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-container>
      
    </div>
    
    <!-- Content showed when a workout item is opened using the button above -->
    <b-collapse 
      :id="'collapse-' + id.toString()"
      @show="onOpen"
      @hide="onClose"
      @hidden="onClosed"
    >
      <div class="bg-white border-right border-bottom border-left rounded-bottom px-4 py-3">
        <p>{{ description }}</p>
      </div>
    </b-collapse>
  </div>
</template>

<script>
export default {
  name: "CalendarItemWorkout",
  props: {
    id: Number,
    itemData: Object
  },
  data() {
    return {
      selected: false,
      buttonVariant: 'info',

      // Special class used to custom style the element and 
      // also change style dynamically
      headerClass: {
        'bg-white': true,
        'bg-info': false,
        'text-dark': true,
        'text-light': false,
        'rounded': true,
        'rounded-top': false,
        'border': true,
        'px-2': true,
        'py-3': true
      }
    }
  },
  computed: {

    // Used to have a default value if a workout does not have
    // a specified location or description

    location() {

      if (this.itemData.location === '') {
        return '-'
      
      } else {
        return this.itemData.location
      }
    },

    description() {
      
      if (this.itemData.description === '') {
        return 'Ingen beskrivning'

      } else {
        return this.itemData.description
      }
    }
  },

  methods: {

    // Methods that listens for events and then changes style (class) of the element

    onOpen() {
      this.selected = true
      // Switch color
      this.buttonVariant = 'light'
      this.headerClass['bg-white'] = false
      this.headerClass['bg-info'] = true
      this.headerClass['text-dark'] = false
      this.headerClass['text-light'] = true

      // Change rounded
      this.headerClass['rounded'] = false
      this.headerClass['rounded-top'] = true
    },

    onClose() {
      // Switch color
      this.buttonVariant = 'info'
      this.headerClass['bg-info'] = false
      this.headerClass['bg-white'] = true
      this.headerClass['text-light'] = false
      this.headerClass['text-dark'] = true
    },

    onClosed() {
      this.selected = false
      // Change rounded
      this.headerClass['rounded-top'] = false
      this.headerClass['rounded'] = true
    }
  }
};
</script>

<style scoped>
p {
  font-size: 0.7rem;
  margin-bottom: 0;
}

h6 { 
  font-size:0.8rem; 
}

@media (min-width: 544px) {  
  p { font-size: 0.9rem; }
  h6 { font-size:1rem; }
}
</style>