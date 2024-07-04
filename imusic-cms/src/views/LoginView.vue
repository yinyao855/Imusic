<script setup>
import {reactive} from 'vue'
import {ElMessage} from "element-plus";
import instance from "@/js/axiosConfig.js";
import {useUserStore} from "@/stores/user.js";
const userStore = useUserStore()

const formLabelAlign = reactive({
  username: '',
  password: '',
})

const login = () => {
  if (!formLabelAlign.username || !formLabelAlign.password) {
    ElMessage.error('用户名或密码不能为空')
    return
  }

  const formData = new FormData()
  formData.append('username', formLabelAlign.username)
  formData.append('password', formLabelAlign.password)
  // 发送请求
  instance.post('/users/login', formData)
      .then(res => {
        // console.log(res)
        if (res.data.success === true) {
          if (res.data.data.role !== 'admin') {
            ElMessage.warning('您不是管理员')
            return
          }
          ElMessage.success('登录成功')
          let new_data = res.data.data
          userStore.setToken(res.data.token)
          userStore.setUsername(new_data.username)
          userStore.setAvatar(new_data.avatar)
          userStore.setRole(new_data.role)
          userStore.setUserInfo(new_data)
          userStore.userLogin()
          window.location.href = '/'
        } else {
          ElMessage.error(res.data.message)
        }
      })
      .catch(err => {
        console.log(err)
      })
}
</script>

<template>
  <div class="h-screen w-full flex bg-with-image">
    <div class="m-auto rounded-2xl w-96 h-96 p-12 shadow-2xl bg-white">
      <div class="font-bold text-3xl mb-10">Imusic 内容管理系统</div>
      <el-form
          label-position="right"
          label-width="auto"
          :model="formLabelAlign"
          style="max-width: 600px"
          size="large"
      >
        <el-form-item label="用户名">
          <el-input v-model="formLabelAlign.username"/>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="formLabelAlign.password" type="password" show-password @keydown.enter="login"/>
        </el-form-item>
      </el-form>
      <el-button type="primary" class="w-full mt-10" round size="large" @click="login">登录</el-button>
    </div>
  </div>
</template>

<style scoped>
.bg-with-image {
  background-image: url("/cover.jpeg");
  background-size: cover;
  background-position: center;
}
</style>