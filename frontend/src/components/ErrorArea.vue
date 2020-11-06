<template>
  <b-container>
    <b-row 
      id="content-row" 
      class="align-items-center"
    >
      <b-col
        id="content-col"
        class="mx-auto"
        cols="4" 
      >
        <!-- Card containing the content -->
        <b-card 
          class="text-center" 
          bg-variant="white"
        >
          
          <b-icon 
            id="calendar-icon" 
            class="my-3"
            icon="calendar-fill"
          ></b-icon>
          
          <h2>{{ error.title }}</h2>
          <p>{{ error.message }}</p>
          
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'ErrorArea',
  props: {
    error: Object
  }
}
</script>

<style scoped>
#content-row {
  height: 100vh;
}

#content-col {
  min-width: 350px;
}

#calendar-icon {
  width: 100px;
  height: 100px;
}
</style>