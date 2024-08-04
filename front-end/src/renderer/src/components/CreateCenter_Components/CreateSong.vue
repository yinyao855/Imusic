<!--创建歌曲界面-->
<script setup>
import UploadImage from '@/components/UploadImage.vue'
import { ref,watch,onMounted } from 'vue'
import { GenerateLRCFile, UploadedLyricList } from '@/js/HandleLyrics.js'
import { MusicPlayerVisible } from '@/js/MusicPlayer.js'
import UploadFile_Small from '@/components/CreateCenter_Components/MyCreatedSongs_Components/UploadFile_Small.vue'
import UploadSong from '@/components/CreateCenter_Components/CreateSong_Components/UploadSong.vue'
import { OpenMessage } from '@/js/Notification.js'
import { UserStore } from '@/stores/User.js'
import instance from '@/js/axios.js'
import { GetMyCreatedSongs } from '@/js/MyCreates.js'

const ShowImage=ref(null);
const CoverFile=ref(null);

//歌曲的一些详细信息
const title=ref('');
const singer=ref('');
const introduction=ref('');
const Mp3File=ref(null);

//歌曲的列表
const Lyrics=ref([{timestamp:'',lyric:''}]);


//监测歌词上传之后的变化
watch(() => UploadedLyricList.value, () => {
  Lyrics.value = UploadedLyricList.value
})


const ClearContent=()=>{
  ShowImage.value=null;
  CoverFile.value=null;
  title.value='';
  singer.value='';
  introduction.value='';
  Mp3File.value=null;
  Lyrics.value=[{timestamp:'',lyric:''}];
}

//上传歌曲
const SubmitSong=()=>{
  if(title.value===''){
    OpenMessage('请填写歌曲名','error');
    return;
  }
  if(singer.value===''){
    OpenMessage('请填写歌手名','error');
    return;
  }
  if(CoverFile.value===null){
    OpenMessage('请上传封面','error');
    return;
  }
  if(Mp3File.value===null){
    OpenMessage('请上传音频文件','error');
    return;
  }
  const formData=new FormData();
  formData.append('title',title.value);
  formData.append('singer',singer.value);
  if(introduction.value!==''){
    formData.append('introduction',introduction.value);
  }
  formData.append('cover',CoverFile.value);
  formData.append('audio',Mp3File.value);
  if(Lyrics.value.length>1||(Lyrics.value.length===1&&Lyrics.value[0].content!=='')){
    const LyricFile=GenerateLRCFile(Lyrics.value,title.value);
    formData.append('lyric',LyricFile);
  }
  formData.append('uploader',UserStore().Username);
  instance.post('/songs/upload',formData)
    .then(response=>{
      if(response.data.success===true){
        OpenMessage('上传成功','success');
        GetMyCreatedSongs();
        ClearContent();
      }
      else{
        OpenMessage('上传失败','error');
      }
      })
    .catch(error=>{
      console.log(error);
    })
}

onMounted(ClearContent);
</script>

<template>
  <div class="w-full h-full">
    <div class="h-full w-full overflow-auto flex flex-row z-50 bg-[#FAF7F5]">
      <div class="block w-2/5">
        <div class="mt-4">
          <div class="text-base text-gray-60 w-full my-1 ml-12">封面:</div>
          <UploadImage v-model:ShowImage="ShowImage" v-model:AvatarFile="CoverFile" :UploadImageId="'CreateSong'"
                       class="w-72 ml-12 my-2"></UploadImage>
          <div class="ml-12">
          <UploadSong v-model:Mp3File="Mp3File"></UploadSong>
          </div>
          <div class="ml-12 flex flex-wrap my-1">
            <div class="text-base text-gray-60 w-full my-1">歌曲名:
              <input v-model="title" class="w-3/4 p-2 border-2 rounded-lg" placeholder="歌曲名">
            </div>
            <div class="text-base text-gray-60 w-full my-1">歌手名:
              <input v-model="singer" class="w-3/4 p-2 border-2 rounded-lg" placeholder="歌手名">
            </div>
            <div class="w-[90%] my-1">
              <div class="flex flex-col">
                <div class="">歌曲介绍:</div>
                <div class="flex">
              <textarea v-model="introduction" class="w-full h-32 p-2 border-2 rounded-lg"
                        placeholder="歌曲介绍"></textarea>
                </div>
              </div>
            </div>
            <div class="w-full flex my-2">
              <div
                class="bg-green-500 hover:bg-green-600 transition-colors ease-in duration-300 h-10 rounded-full w-32 flex mr-4"
                @click="SubmitSong"
              >
                <div class="m-auto text-white flex">
                  上传歌曲
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
      </div>
      <div class="block w-3/5 h-full overflow-auto border-l-2">
        <div class="w-full flex">
          <div class="mx-auto text-2xl my-2 flex">
            <span class="mr-4 my-auto">歌词</span>
            <UploadFile_Small></UploadFile_Small>
          </div>

        </div>
        <div class="w-full flex" v-for="(Content,index) in Lyrics" :key="index">
          <div class="mx-auto">
            <input v-model="Content.timestamp" class="w-[30%] p-2 border-2 rounded-lg my-1 mx-2"
                   placeholder="时间，如00:00.00">
            <input v-model="Content.content" class="w-[50%] p-2 border-2 rounded-lg my-1" placeholder="内容">
            <!--          这里不知道为什么把svg放到icons中就会颜色错误-->
            <svg width="24" height="24" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"
                 class="h-6 inline my-auto ml-2 cursor-pointer" @click="Lyrics.splice(index,1)">
              <path d="M9 10V44H39V10H9Z" fill="#fc0516" stroke="#333" stroke-width="4" stroke-linejoin="round" />
              <path d="M20 20V33" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M28 20V33" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M4 10H44" stroke="#333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M16 10L19.289 4H28.7771L32 10H16Z" fill="#fc0516" stroke="#333" stroke-width="4"
                    stroke-linejoin="round" />
            </svg>
            <img src="../icons/Add_Icon.svg" alt="添加" class="h-6 inline my-auto ml-2 cursor-pointer"
                 @click="Lyrics.splice(index+1,0,{timestamp:'',content:''})">
          </div>
        </div>
        <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
      </div>

    </div>
  </div>
</template>

<style scoped>

</style>