import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import '@/css/font/font.css'
import '@/../node_modules/animate.css'
import axios from 'axios'
import VueAxios from 'vue-axios'
import qs from'qs'



const app = createApp(App)

app.use(qs)
app.use(VueAxios, axios)
app.use(store)
app.use(router)
app.use(ElementPlus)
app.mount('#app')

