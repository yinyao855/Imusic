import {ref, computed} from 'vue'
import {defineStore} from 'pinia'

export const useUserStore = defineStore('user', () => {
        const token = ref('')
        const username = ref('')
        const avatar = ref('')
        const role = ref('')
        const isLogin = ref(false)
        const userInfo = ref({})

        function setToken(value) {
            token.value = value
        }

        function setUsername(value) {
            username.value = value
        }

        function setAvatar(value) {
            avatar.value = value
        }

        function setRole(value) {
            role.value = value
        }

        function userLogin() {
            isLogin.value = true
        }

        function userLogout() {
            token.value = ''
            username.value = ''
            avatar.value = ''
            role.value = ''
            isLogin.value = false
            userInfo.value = {}
        }

        function setUserInfo(value) {
            userInfo.value = value
        }

        return {
            token,
            username,
            avatar,
            role,
            isLogin,
            userInfo,
            setToken,
            setUsername,
            setAvatar,
            setRole,
            userLogin,
            userLogout,
            setUserInfo
        }
    },
    {
        persist: true
    })