<script setup>
import {ref} from "vue";
import {ElDialog, ElLoading, ElMessage} from "element-plus";

const dialogVisible = defineModel("visible");
const canUpdate = ref(false)
const downloading = ref(false)
const text = ref('获取更新信息...')

const onDialog = async() =>{ // 弹窗的打开方法 添加loading
  let loading = ElLoading.service({
    target: '.dialogLoading',
    lock: true,
    text: '正在获取更新...',
  })

  const UPDATE_URL = 'http://127.0.0.1:4523/m1/4891856-4547514-default/update/check'
  text.value = await api.checkUpdateInfo(UPDATE_URL)
  loading.close()
  canUpdate.value = text.value === '有新版本可用';
}

const downloadProgress = ref(0);

const downloadFile = async () => {
  try {
    const DOWNLOAD_URL = 'http://182.92.100.66:5000/media/dist.zip';

    text.value = '正在下载资源...'
    canUpdate.value = false
    downloading.value = true

    // 监听主进程发送的下载进度数据
    window.electron.ipcRenderer.on('downloadProgress', (event, progress) => {
      downloadProgress.value = Math.round((progress.loaded * 100) / progress.total);
    });

    // 向主进程发送下载请求，并监听下载进度
    await window.electron.ipcRenderer.invoke('downloadZip', {DOWNLOAD_URL});

    downloading.value = false
    text.value = '下载完成，正在安装...'
    await api.hotUpdateApp()
  } catch (error) {
    console.error('Error downloading file:', error);
    ElMessage.error('下载文件时出错，请重试');
  }
};
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    title="更新"
    width="500"
    @open="onDialog"
    custom-class="dialogLoading"
  >
    <span>{{text}}</span>
    <el-progress v-if="downloading" :percentage="downloadProgress"></el-progress>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="downloadFile" :disabled="!canUpdate">
          更新
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>

</style>
