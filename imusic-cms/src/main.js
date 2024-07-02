import { createApp } from 'vue'
import { createPinia } from 'pinia'

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate' //引入持久化插件

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import './style.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

import {useUserStore} from "@/stores/user.js";
const userStore = useUserStore()
router.beforeEach((to, from, next) => {
    // 在导航前执行操作，例如身份验证检查
    if (userStore.token === '' && to.path !== '/login') {
        next('/login'); // 重定向到登录页
    } else {
        next(); // 继续导航
    }
})

app.use(router)
app.use(ElementPlus, {
    locale: zhCn,
})

app.mount('#app')
