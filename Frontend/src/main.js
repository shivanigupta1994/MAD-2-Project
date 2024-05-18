
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axiosInstance from './axios'
import store from './store'

const app = createApp(App);

// Set up Axios as a plugin with the configured instance
app.config.globalProperties.$axios = axiosInstance;

app.use(router)
app.use(store)

app.mount('#app')
