import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createPersistPlugin } from '@pinia/persist'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import './style.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

const pinia = createPinia()
pinia.use(createPersistPlugin())
app.use(pinia)
app.use(router)
app.use(ElementPlus, {
    locale: zhCn,
})

app.mount('#app')
