<script setup>
import {useUserStore} from "@/stores/user.js";
import {computed} from "vue"
import router from "@/router/index.js";
import {ElMessage} from "element-plus";

const userStore = useUserStore();

const userInfo = computed(() => {
  return userStore.userInfo;
});

function logout() {
  userStore.userLogout();
  router.push('/login');
}

function changeInfo() {
  ElMessage.info('暂不支持修改用户信息');
}
</script>

<template>
  <div class="w-full h-full flex items-center">
    <el-image src="/logo.png" class="h-10 aspect-square ml-10"/>
    <h1 class="text-2xl font-semibold ml-5">Imusic 内容管理系统</h1>
    <div class="ml-96">
      <el-popover width="220px">
        <template #reference>
          <el-avatar :src="userInfo.avatar"/>
        </template>
        <template #default>
          <div class="flex-col items-center">
            <div class="flex justify-center">
              <el-avatar :size="60" :src="userInfo.avatar"/>
            </div>
            <p class="text-lg mb-4">当前用户: {{ userInfo.username }}</p>
            <p class="text-sm mb-4">{{ userInfo.email }}</p>
            <div class="flex">
              <el-button type="success" plain @click="changeInfo">修改信息</el-button>
              <el-button type="primary" plain @click="logout">退出登录</el-button>
            </div>
          </div>
        </template>
      </el-popover>
    </div>
  </div>
</template>

<style scoped>

</style>