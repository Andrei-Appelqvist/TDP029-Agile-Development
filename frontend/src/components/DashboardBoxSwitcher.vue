<template>
  <div>
    
    <DashboardBoxSwitcherButton
      v-for="(service, index) in serviceList" 
      :key="index"
      :buttonTitle="service"
      :active="service === activeService"
      @button-clicked="$emit('switch-service', service)"
    />
    
  </div>
</template>

<script>
// Components
import DashboardBoxSwitcherButton from '../components/DashboardBoxSwitcherButton.vue'

export default {
  name: 'DashboardBoxSwitcher',
  components: {
    DashboardBoxSwitcherButton
  },
  props: {
    serviceList: Array,
    activeService: String
  },
}
</script>

<style scoped>
</style>