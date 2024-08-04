<!--创建歌单界面-->
<script setup>
import UploadImage from '@/components/UploadImage.vue'
import { ref } from 'vue'
import { MusicPlayerVisible } from '@/js/MusicPlayer.js'
import { OpenMessage } from '@/js/Notification.js'
import { UserStore } from '@/stores/User.js'
import instance from '@/js/axios.js'

//封面
const ShowImage = ref(null)
const CoverFile = ref(null)

const title=ref('');
const introduction=ref('');

const SubmitSongList=()=>{
  if(title.value===''){
    OpenMessage('请填写歌单名称','error');
    return;
  }
  if(CoverFile.value===null){
    OpenMessage('请上传封面','error');
    return;
  }
  const formData = new FormData()
  formData.append('title',title.value);
  if(introduction.value!==''){
    formData.append('introduction',introduction.value);
  }
  formData.append('cover',CoverFile.value);
  formData.append('owner',UserStore().Username);
  instance.post('/songlists/create',formData)
    .then(response=>{
      if(response.data.success===true){
        OpenMessage('创建成功','success');
      }
      else{
        OpenMessage('创建失败','error');
      }
    })
    .catch(error=>{
      console.log(error);
    })
}

const ClearContent=()=>{
  ShowImage.value=null;
  CoverFile.value=null;
  title.value='';
  introduction.value='';
}
</script>

<template>
  <div class="w-full h-full flex flex-wrap overflow-auto">
    <div class="mx-auto w-3/5 flex flex-wrap">
      <div class="w-full text-lg flex">
        <div class="my-auto">
          歌单封面:
        </div>
        <UploadImage v-model:ShowImage="ShowImage" v-model:AvatarFile="CoverFile" :UploadImageId="'CreateSongList'"></UploadImage>
      </div>
      <div class="w-full text-lg">
        歌单名称:
        <input class="w-3/4 p-2 border-2 rounded-lg my-1" placeholder="歌单名称" v-model="title">
      </div>
      <div class="w-full text-lg flex my-1">
        <div class="my-auto">
          歌单简介:
        </div>
        <textarea class="w-3/4 p-2 border-2 rounded-lg my-1" placeholder="歌单简介" v-model="introduction"></textarea>
      </div>
      <div class="w-full flex my-1">
        <div class="mx-auto flex">
          <div
            class="bg-green-500 hover:bg-green-600 transition-colors ease-in duration-300 h-10 rounded-full w-32 flex mr-4"
            @click="SubmitSongList"
          >
            <div class="m-auto text-white flex">
              上传歌单
            </div>
          </div>
          <div
            class="bg-gray-400 hover:bg-gray-500 transition-colors ease-in duration-300 h-10 rounded-full w-32 flex"
            @click="ClearContent"
          >
            <div class="m-auto text-white flex">
              重置输入
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="w-full h-32" v-if="MusicPlayerVisible"></div>
  </div>
</template>

<style scoped>

</style>