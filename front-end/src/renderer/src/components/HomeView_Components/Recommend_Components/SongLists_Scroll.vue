<script setup>
import { HomeView_HotSongLists } from '@/js/BeforeEnterHomeView.js'
import { NavicatWidth, WindowWidth } from '@/js/NavicatStatus.js'
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { GetSongListDetail } from '@/js/SongList.js'

//偏移量
const Offset = ref(2080)
//当前时间,这里从1开始，以让两者错开
const currentTime = ref(1)
//计时器
let timer = null
//当前索引
const CurrentIndex = ref(0)

//开始计时
const startTimer = () => {
  timer = setInterval(() => {
    currentTime.value++
  }, 1000) // 每秒钟增加1秒
}

onMounted(() => {
  startTimer()
})

onUnmounted(() => {
  clearInterval(timer)
})

//土方法解决，会浪费性能
const NextPhoto = () => {
  Offset.value += 208
  currentTime.value=0;
  HomeView_HotSongLists.value.push(HomeView_HotSongLists.value[CurrentIndex.value])
  CurrentIndex.value++
}

const PrevPhoto = () => {
  Offset.value -= 208
}


//监测当前时间变化
watch(() => currentTime.value, () => {
  if (currentTime.value >= 4) {
    NextPhoto()
  }
})
</script>

<template>
  <div class="relative pl-6 pr-10">
    <div :style="{width:`${WindowWidth-NavicatWidth}px`}" class="overflow-hidden">
      <div class="flex mt-2" :style="{ transform: `translateX(-${Offset}px)`,transition: `transform 0.5s ease` }">
        <div v-for="(SongList,index) in HomeView_HotSongLists" :key="index" class="mx-2 flex flex-wrap w-48">
          <div class="relative w-48 h-48" @click="GetSongListDetail(SongList.id)">
            <div
              class="absolute top-0 left-0 rounded-full hover:bg-gray-400/40 w-full h-full transition-colors ease-in duration-300 cursor-pointer"></div>
            <img :src="SongList.cover" alt="歌单封面" class="aspect-square rounded-full w-48 cursor-pointer">
          </div>
          <div class="text-center w-48 mt-2">{{ SongList.title }}</div>
        </div>

      </div>
    </div>
    <div class="absolute top-1/2 left-0 -translate-y-1/2 px-0.5 py-1 bg-gray-300/60 hover:bg-gray-400/50 transition-colors ease-in duration-300 cursor-pointer rounded">
      <img src="../../icons/Left_Photo_Icon.svg" class="h-6 w-6" alt="上一张" @click="PrevPhoto">
    </div>
    <div class="absolute top-1/2 right-4 -translate-y-1/2 px-0.5 py-1 bg-gray-300/60 hover:bg-gray-400/50 transition-colors ease-in duration-300 cursor-pointer rounded">
      <img src="../../icons/Left_Photo_Icon.svg" class="h-6 w-6 rotate-180" alt="下一张" @click="NextPhoto">
    </div>
  </div>
</template>

<style scoped>
</style>