import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import tChart from '../components/tChart.vue'
import chartSample from '../components/chartSample.vue'
import tableSample from '../components/tableSample.vue'
import radarSample from '../components/radarSample.vue'
Vue.use(Router)

export default new Router({
    routes: [{
        path: '/',
        name: 'tChart',
        component: chartSample
    }, {
        path: '/tS',
        name: 'tTable',
        component: tableSample
    }, {
        path: '/Ra',
        name: 'tRadar',
        component: radarSample
    }]
})