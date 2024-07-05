import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://182.92.100.66:5000',
    timeout: 5000, // 请求超时时间，可选
});

export const setAuthToken = (token) => {
    instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
};

export const removeAuthToken = () => {
    delete instance.defaults.headers.common['Authorization'];
};

export default instance;