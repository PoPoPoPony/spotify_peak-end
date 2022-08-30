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
import VuePlyr from 'vue-plyr'
import 'vue-plyr/dist/vue-plyr.css'


const app = createApp(App)

app.use(VueAxios, axios)
app.use(VuePlyr, {plyr: {
    "autoplay": true,
    "volume": 0.3,
    "speed": { selected: 1, options: [0.75, 1, 1.25] },
    "controls":[
        // 'play-large',
        // 'play',
        // 'progress',
        // 'current-time',
        // 'mute',
        // 'volume',
        // 'captions',
        // 'settings',
        // 'pip',
        // 'airplay',
        // 'fullscreen'
    ]
}})
app.use(store)
app.use(router)
app.use(ElementPlus)
app.mount('#app')

