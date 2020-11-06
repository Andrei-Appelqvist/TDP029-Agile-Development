<template>
  
  <b-navbar 
    type="dark" 
    variant="info"
  >
    <b-navbar-brand>
      
      <!-- Logo (just text in a p element) -->
      <p 
        class="d-inline-block font-weight-bolder ml-1 mb-0" 
        style="font-size: 1.5rem;"
      >
        Träningsdagbok
      </p>

    </b-navbar-brand>

    <!-- Tab navigation -->
    <b-navbar-nav class="ml-auto">
      
      <!-- Home -->
      <b-nav-item 
        class="mr-1" 
        v-b-tooltip.hover title="Hem" 
        :active="page === 'home'" 
        :hidden="page === 'welcome'"
        @click="$emit('change-state', 'home')"
      >
        <b-icon 
          icon="house-fill" 
          shift-v="-1" 
          style="width: 40px; height: 40px;"
        ></b-icon>

      </b-nav-item>
      
      <!-- Calendar -->
      <b-nav-item 
        class="mr-1" 
        v-b-tooltip.hover title="Kalender" 
        :active="page === 'calendar'" 
        :hidden="page === 'welcome'"
        @click="$emit('change-state', 'calendar')"
      >
        <b-icon 
          icon="calendar-fill" 
          shift-v="-2" 
          style="width: 38px; height: 38px;"
        ></b-icon>

      </b-nav-item>
      
      <!-- User Settings -->
      <b-nav-item 
        v-b-tooltip.hover title="Användare" 
        :active="page === 'settings'" 
        :hidden="page === 'welcome'"
        @click="$emit('change-state', 'settings')"
      >
        <b-icon 
          icon="person-fill" 
          shift-v="-1" 
          style="width: 45px; height: 45px;"
        ></b-icon>

      <!-- Logout button (Only present when in welcome state in UserArea) -->
      </b-nav-item>

        <b-nav-item :class="logoutButtonClass">
          
          <b-button
            id="logout-button"
            variant="secondary"
            v-on:click="$emit('logout-user')"
          >
            Logout
          </b-button>

        </b-nav-item>

    </b-navbar-nav>
  </b-navbar>
</template>


<script>

export default {
  name: "HeaderSection",
  props: {
    user: Object,
    page: String
  },

  data() {
    return {
      logoutButtonClass: {
        'mr-2': true,
        'mb-0': true,
        'mt-0': true,
        'd-none': true
      }
    }
  },

  // Checks which UserArea state the app is in, if it is in 
  // welcome state the logout button changes to display: none
  updated() {
    
    if (this.page === 'welcome') {
      this.logoutButtonClass['d-none'] = false;
    
    } else {
      this.logoutButtonClass['d-none'] = true;
    }
    
  },
}
</script>


<style scoped>
</style>