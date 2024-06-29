import Vue from 'vue'
import App from './App.vue'
import store from './store'

import ElementUI from 'element-ui'

import 'element-ui/lib/theme-chalk/index.css'
import drag from '@/config/drag';

import recursive from './recursive'
Vue.use(recursive)

import tooltip_ele from './tooltip'
Vue.use(tooltip_ele)

import dataHighLight_In_and_Out from './dataHighLight'
Vue.use(dataHighLight_In_and_Out)

Vue.use(ElementUI)

Vue.use(require('@hscmap/vue-window'))

Vue.config.productionTip = false

Vue.prototype.download = function(content, fileName, contentType) {
  let contentStr = JSON.stringify(content,null,2);
  var a = document.createElement("a");
  var file = new Blob([contentStr], {type: contentType});
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
}

import * as d3 from "d3"
window.d3 = d3

window.d3VoronoiTreemap = require('d3-voronoi-treemap')

import * as $ from 'jquery'
window.$ = $


new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
