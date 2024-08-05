<script setup>
import { MySongLists } from '@/js/MySongList.js'
import { MusicPlayerVisible } from '@/js/MusicPlayer.js'
import { GetSongListDetail } from '@/js/SongList.js'
import { UserStore } from '@/stores/User'
import { GetLikeSongs } from '@/js/LikeSongs.js'
</script>

<template>
  <div class="w-full h-full flex flex-wrap py-4 overflow-auto">
    <div class="card card-compact bg-base-100 w-72 shadow-xl mx-4 h-72" @click="GetLikeSongs">
      <figure class="relative">
        <img
          src="/LikeSongs.png"
          alt="封面"
        />
        <div class="w-full h-full absolute hover:bg-gray-400/40 transition-colors ease-in duration-300 cursor-pointer"></div>
      </figure>
      <div class="card-body">
        <div class="text-xl">喜爱的歌曲</div>
        <div>创建时间：{{ UserStore().Registration_date }}</div>
      </div>
    </div>
    <div class="card card-compact bg-base-100 w-72 shadow-xl mx-4 h-72" v-for="(SongList,index) in MySongLists"
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
        <div>创建时间：{{ SongList.create_date }}</div>
      </div>
    </div>
    <div class="w-full h-32" v-if="MusicPlayerVisible"></div>
  </div>
</template>

<style scoped>

</style>
