<script setup>
import { GetSongListDetail } from '@/js/SongList.js'
import { MusicPlayerVisible } from '@/js/MusicPlayer.js'
import { LikeSongLists } from '@/js/LikeSongLists.js'
</script>

<template>
  <div class="w-full h-full flex flex-wrap py-4 overflow-auto">
    <div class="card card-compact bg-base-100 w-72 shadow-xl mx-4 h-72" v-for="(SongList,index) in LikeSongLists"
         :key="index" @click="GetSongListDetail(SongList.id)">
      <figure class="relative">
        <img
          :src="SongList.cover"
          alt="封面"
          class="h-[200px]"
        />
        <div
          class="w-full h-full absolute hover:bg-gray-400/40 transition-colors ease-in duration-300 cursor-pointer"></div>
      </figure>
      <div class="card-body">
        <div class="text-xl">{{ SongList.title }}</div>
        <div>
          <span>创建者：{{ SongList.owner }}</span>
          <span>・</span>
          <span>{{ SongList.create_date }}</span>
        </div>
      </div>
    </div>
    <div class="w-full h-32" v-if="MusicPlayerVisible"></div>
  </div>
</template>

<style scoped>

</style>