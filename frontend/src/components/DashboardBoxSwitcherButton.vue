<template>
    
  <div 
    :class="buttonClass"
    @click="$emit('button-clicked')"
  >
    {{ buttonTitle.charAt(0).toUpperCase() }}{{ buttonTitle.slice(1)}}
  </div>

</template>

<script>
export default {
  name: 'DashboardBoxSwitcherButton',
  props: {
    buttonTitle: String,
    active: Boolean
  },
  computed: {
    // Custom styled button for switching between health services
    buttonClass() {
      return {
        'switchbutton': true,
        'mx-1': true,
        'd-inline-block': true,
        'rounded': true,
        'font-weight-bold': true,
        'text-white': true,
        'active': this.active,
        'inactive': !this.active
      }
    }
  }
}
</script>

<style scoped>
.switchbutton {
  cursor: pointer;
  font-size: 0.8em;
  padding-left: 5px;
  padding-top: 2px;
  padding-right: 5px;
  padding-bottom: 2px;
}

.active {
  background-color: #00A2B6;
}

.active:hover {
  background-color: #10ABBD;
}

.inactive {
  background-color: #6B757C;
}

.inactive:hover {
  background-color: #798389;
}
</style>