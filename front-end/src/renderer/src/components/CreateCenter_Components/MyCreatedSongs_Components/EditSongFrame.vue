<!--编辑歌曲的组件-->
<script setup>
import { EditLyricList, EditSongDetail, EditSongVisible, GetEditSongDetail, SongId } from '@/js/SongDetail.js'
import { onMounted, ref, watch } from 'vue'
import { HandlePlayNow, MusicPlayerVisible } from '@/js/MusicPlayer.js'
import UploadImage from '@/components/UploadImage.vue'
import { GenerateLRCFile, UploadedLyricList } from '@/js/HandleLyrics.js'
import instance from '@/js/axios.js'
import { OpenMessage } from '@/js/Notification.js'
import UploadFile_Small from '@/components/CreateCenter_Components/MyCreatedSongs_Components/UploadFile_Small.vue'
import { GetMyCreatedSongs } from '@/js/MyCreates.js'


const Lyrics = ref(EditLyricList.value)


//展示的图片
const ShowImage = ref('')
//歌曲名
const title = ref('')
//歌手名
const singer = ref('')
//歌曲介绍
const introduction = ref('')
//上传的封面文件
const CoverFile = ref(null)
//生成的歌词文件
const GeneratedFile = ref()

//监测歌词上传之后的变化
watch(() => UploadedLyricList.value, () => {
  Lyrics.value = UploadedLyricList.value
})

//初始赋值
watch(() => EditSongDetail.value, () => {
  title.value = EditSongDetail.value.title
  singer.value = EditSongDetail.value.singer
  introduction.value = EditSongDetail.value.introduction
  ShowImage.value = EditSongDetail.value.cover
})

//歌词初始赋值
watch(() => EditLyricList.value, () => {
  Lyrics.value = EditLyricList.value
})

//保存修改
const SaveChanges = () => {
  GeneratedFile.value=GenerateLRCFile(Lyrics.value,title.value);
  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('singer', singer.value)
  formData.append('introduction', introduction.value)
  if (CoverFile.value !== null) {
    formData.append('cover', CoverFile.value)
  }
  if (GeneratedFile.value !== null) {
    console.log(GeneratedFile.value);
    formData.append('lyric', GeneratedFile.value)
  }
  instance.post('/songs/update/' + EditSongDetail.value.id, formData)
    .then(response => {
      if (response.data.success === true) {
        OpenMessage('修改成功', 'success')
        GetMyCreatedSongs();
        EditSongVisible.value = false
      } else {
        OpenMessage('修改失败', 'error')
      }
    })
    .catch(error => {
      console.log(error)
    })
}

//取消修改
const CancelChange=()=>{
  title.value=EditSongDetail.value.title
  singer.value=EditSongDetail.value.singer
  introduction.value=EditSongDetail.value.introduction
  ShowImage.value=EditSongDetail.value.cover
  Lyrics.value=EditLyricList.value
}

onMounted(GetEditSongDetail)
</script>

<template>
  <div class="h-full w-full overflow-auto flex flex-row z-50 bg-[#FAF7F5]">
    <div class="block w-2/5">
      <div class="btn btn-sm mt-2" @click="EditSongVisible=false">
        <img src="../../icons/Return_Icon.svg" alt="返回">
      </div>
      <div class="mt-4">
        <UploadImage v-model:ShowImage="ShowImage" v-model:AvatarFile="CoverFile" :UploadImageId="'EditSong'"
                     class="w-72 ml-12 my-2"></UploadImage>
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
              class="bg-blue-500 hover:bg-blue-600 transition-colors ease-in duration-300 h-10 rounded-full w-32 flex mr-4"
              @click="HandlePlayNow(SongId)"
            >
              <div class="m-auto text-white flex">
                <img src="../../icons/Play_White_Icon.svg" alt="播放" class="h-6 inline my-auto mr-2">
                播放
                <div class="w-1 h-full"></div>
              </div>
            </div>
            <div
              class="bg-green-500 hover:bg-green-600 transition-colors ease-in duration-300 h-10 rounded-full w-32 flex mr-4"
              @click="SaveChanges"
            >
              <div class="m-auto text-white flex">
                保存
              </div>
            </div>
            <div
              class="bg-gray-500 hover:bg-gray-600 transition-colors ease-in duration-300 h-10 rounded-full w-32 flex mr-4"
              @click="CancelChange"
            >
              <div class="m-auto text-white flex">
                取消修改
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
          <img src="../../icons/Add_Icon.svg" alt="添加" class="h-6 inline my-auto ml-2 cursor-pointer"
               @click="Lyrics.splice(index+1,0,{timestamp:'',content:''})">
        </div>
      </div>
      <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
    </div>

  </div>
</template>

<style scoped>

</style>