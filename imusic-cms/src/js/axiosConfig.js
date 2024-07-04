import axios from 'axios';
import {useUserStore} from "@/stores/user.js";
import {computed} from "vue";
let _token = computed(() => useUserStore().token);

const instance = axios.create({
    baseURL: 'http://182.92.100.66:5000',
    timeout: 5000, // 请求超时时间，可选
    headers: {
        //设置token
        'Authorization': `Bearer ${_token}`
    }
});

export default instance;