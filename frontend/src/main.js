// This site is built using the Vue grid system. 
// The basis of this system are rows(b-row) and columns(b-col)
// For more information regarding the Vue grid system check out:
// https://bootstrap-vue.org/docs/components/layout

// This is where most of the packages used in the app are imported
import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import Vuelidate from 'vuelidate'
import ECharts from 'vue-echarts'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import 'echarts/lib/chart/pie'
import 'echarts/lib/chart/line'
import 'echarts/lib/chart/bar'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/legend'
import 'echarts/lib/component/axis'
import 'echarts/lib/component/grid'
import 'echarts/lib/component/dataZoom'

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(Vuelidate);

Vue.component('v-chart', ECharts)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')