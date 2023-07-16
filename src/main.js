import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// import popup from './global'
import cookies from 'vue-cookies'
// import axios from 'axios'
import 'amfe-flexible'
// import jsonp  from 'vue-jsonp'
// import md5 from 'js-md5'

let app = createApp(App)
app.use(router)
app.use(cookies)
app.mount('#app')
