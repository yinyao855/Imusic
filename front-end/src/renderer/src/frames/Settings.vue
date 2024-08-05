<script setup>
import PackageJson from '../../../../package.json'
import {onMounted, ref} from "vue";
import UpdateDialog from "@/components/UpdateDialog.vue";

const version = PackageJson.version
const dialogVisible = ref(false)
const btnVisible = ref(false)
const checkUpdate = () => {
  // console.log('check update')
  dialogVisible.value = true
}

onMounted(() => {
  // 判断是否是electron环境，如果是显示检查更新按钮
  if ('electron' in window) {
    console.log('electron')
    btnVisible.value = true
  }
})
</script>

<template>
  <UpdateDialog v-model:visible="dialogVisible"></UpdateDialog>
  <div class="w-full h-full flex-col p-6">
    <div class="flex items-center">
      <p class="mr-3">当前版本:{{version}}</p>
      <el-button v-if="btnVisible" @click="checkUpdate">检查更新</el-button>
    </div>
    <p>Imusic开发团队</p>
  </div>
</template>

<style scoped>

</style>
