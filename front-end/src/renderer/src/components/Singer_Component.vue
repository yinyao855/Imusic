<!--歌手详情展示-->
<script setup>
import { MusicPlayerVisible, PlayAll } from '@/js/MusicPlayer.js'
import { ref} from 'vue'
import { NavicatWidth, WindowWidth } from '@/js/NavicatStatus.js'
import { SingerDetail, SingerDetailVisible } from '@/js/SingerDetail.js'
import SongTable from '@/components/SongTable.vue'

//歌单中的歌曲
const Songs = ref(SingerDetail.value.songs)
</script>

<template>
  <div class="h-screen overflow-auto flex flex-row flex-wrap">
    <div class="btn btn-sm mt-3 ml-2 z-40" @click="SingerDetailVisible=false">
      <img src="./icons/Return_Icon.svg" alt="返回">
    </div>
    <!--    背景模糊-->
    <div class="w-full h-1/3 absolute overflow-hidden" style="filter:blur(12px)"
         :style="{width:`${WindowWidth-NavicatWidth+88}px`}">
      <img class="w-full aspect-[3/1]" :src="SingerDetail.singerImage" alt="封面">
    </div>
    <!--    歌单详情-->
    <div class="w-full h-1/3 absolute z-10" :style="{width:`${WindowWidth-NavicatWidth+88}px`}">
      <div class="w-full h-full flex flex-row z-10">
        <div class="h-3/4 my-auto ml-20">
          <img class="h-full aspect-square rounded-2xl" :src="SingerDetail.singerImage" alt="封面">
        </div>
        <div class="h-3/4 my-auto ml-8 flex">
          <div class="my-auto block">
            <div class="text-white text-3xl">
              {{ SingerDetail.singerName }}
            </div>

            <div class="text-white text-lg btn btn-sm btn-success mt-3" @click="PlayAll(SingerDetail.songs)">
              <span class="ml-3">播放全部</span>
              <img src="./icons/Plus_Icon.svg" alt="加" class="h-4 mr-3">
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="h-2/3 absolute bottom-0 px-4" :style="{width:`${WindowWidth-NavicatWidth+88}px`}">
      <SongTable v-model:Songs="Songs" class="w-full"></SongTable>
      <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
    </div>
  </div>
</template>

<style scoped>
</style>