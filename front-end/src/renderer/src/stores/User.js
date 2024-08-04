import {defineStore} from "pinia";
import {ref} from "vue";

export const UserStore = defineStore('user', () => {
    const State = ref(false); //是否登录
    const Username = ref(''); //用户名
    const token = ref('') //token
    const HasTryLogin = ref(''); //是否尝试登录
    const Role = ref(''); //用户身份
    const Avatar = ref(''); //用户头像
    const Registration_date=ref(''); //注册时间

    return {
        State,
        Username,
        token,
        HasTryLogin,
        Role,
        Avatar,
        Registration_date
    }


})