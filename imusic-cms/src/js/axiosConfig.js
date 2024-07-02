import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://182.92.100.66:5000',
    timeout: 5000, // 请求超时时间，可选
    // headers: {
    //     'Content-Type': 'application/json', // 设置请求头
    // }
});

export default instance;