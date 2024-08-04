import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://182.92.100.66:5000/',
    timeout: 5000, // 设置请求超时时间
    withCredentials: true // 全局设置 withCredentials 为 true
});

export const setAuthToken = (token) => {
    instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
};

export default instance;
