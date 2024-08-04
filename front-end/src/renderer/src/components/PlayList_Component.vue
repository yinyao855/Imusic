<!--播放列表-->
<script setup>

import {CurrentPlayList, HandlePlayNow} from "@/js/MusicPlayer.js";
</script>

<template>
  <div class="max-h-[500px] fixed right-3 bottom-32 bg-[#f1ebe9] w-96 z-30 rounded-xl overflow-auto border-2">
    <div class="w-full flex pl-2 py-2 border-b hover:bg-gray-200 bg-opacity-30 transition-colors ease-in duration-300"
         v-for="(Song,index) in CurrentPlayList" :key="index" @click="HandlePlayNow(Song.id)">
      <div class="h-full">
        <img :src="Song.cover" alt="封面" class="aspect-square rounded-md w-16 my-auto">
      </div>
      <div class="my-auto text-sm font-bold ml-2">{{ Song.title }}</div>
      <div class="flex-1"></div>
      <div class="my-auto text-sm mr-5">{{ Song.singer }}</div>
    </div>
  </div>
</template>

<style scoped>
</style>