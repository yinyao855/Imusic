<script setup>
import {useUserStore} from "@/stores/user.js";
import {computed, onMounted, onUnmounted, ref} from "vue"
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

const currentTime = ref(getFormattedTime());
// 定义更新时间的函数
function updateCurrentTime() {
  currentTime.value = getFormattedTime();
}
// 在组件加载时启动定时器
onMounted(() => {
  // 每秒更新一次时间
  setInterval(updateCurrentTime, 1000);
});
// 在组件销毁时清除定时器
onUnmounted(() => {
  clearInterval(updateCurrentTime);
});
// 获取格式化后的当前时间字符串
function getFormattedTime() {
  const date = new Date();
  return `${date.getFullYear()}-${padZero(date.getMonth() + 1)}-${padZero(date.getDate())} ${padZero(date.getHours())}:${padZero(date.getMinutes())}:${padZero(date.getSeconds())}`;
}
// 辅助函数，在数字小于10时添加前导零
function padZero(num) {
  return num < 10 ? '0' + num : num;
}
</script>

<template>
  <div class="w-full h-full p-0">
    <el-row class="h-full">
      <el-col :span="8">
        <div class="flex h-full items-center">
          <el-image src="/logo.png" class="h-10 aspect-square ml-10"/>
          <h1 class="lg:text-2xl font-bold ml-5 truncate">Imusic 内容管理系统</h1>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="h-full flex">
          <h1 class="m-auto lg:font-semibold truncate">当前时间：{{ currentTime }}</h1>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="flex h-full items-center justify-center">
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
          <h1 class="ml-5 truncate">欢迎回来，{{ userInfo.username }}！</h1>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>

</style>