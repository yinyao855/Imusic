<!--上传歌曲文件-->
<script setup>
import { defineModel, ref,watch } from 'vue'

//歌曲音频文件
const Mp3File = defineModel('Mp3File')

//歌曲的文件名
const Filename = ref('点击上传音频文件')

//处理上传后的逻辑
const HandleUpload = (event) => {
  Mp3File.value = event.target.files[0];
  Filename.value=Mp3File.value.name;
}

//监测复位
watch(()=>Mp3File.value,()=>{
  if(Mp3File.value===null){
    Filename.value='点击上传音频文件';
  }
})
</script>

<template>
  <input class="hidden" @change="HandleUpload" type="file" id="UploadMp3File">
  <label for="UploadMp3File" class="flex flex-wrap">
    <div
      class="bg-blue-400 hover:bg-blue-500 transition-colors ease-in duration-300 hover:shadow flex rounded-md text-white h-10">
      <div class="flex mx-3">
        <div class="my-auto">
          <img src="../../icons/AddFile_Icon.svg" alt="上传文件" class="h-6 mx-auto">
        </div>
        <div class="my-auto">
          {{ Filename }}
        </div>
      </div>
    </div>
  </label>
</template>

<style scoped>

</style>