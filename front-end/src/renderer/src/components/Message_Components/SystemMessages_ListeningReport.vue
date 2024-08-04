<script setup>

import {ContentDetails} from "@/js/SystemMessage.js";


</script>

<template>
  <div class="carousel rounded-box w-full h-96">
    <div class="carousel-item stat w-10/12 text-center bg-cyan-800">
      <div class="m-auto">
        <img src="../icons/Message_System_Listening_Report.svg" alt="听歌周报"
             class="h-16 rounded-xl aspect-square inline-block"/>
        <div class="stat-value text-yellow-400 font-bold mb-10">
          听歌周报
        </div>
        <div class="text-yellow-100 font-bold">
          {{ ContentDetails.StartDateAndEndDate }}
        </div>
      </div>
    </div>
    <div class="carousel-item stat w-10/12 text-center bg-orange-100">
      <div class="m-auto">
        <div class="text-left stat-title text-accent-content mb-1 font-bold">
          听歌统计
        </div>
        <div class="stat-value text-pink-500">
          {{ ContentDetails.Duration }}
        </div>
      </div>
      <div class="">
        <div class="stat-value text-content inline-block mr-3">
          共听歌
        </div>
        <div class="stat-value text-purple-400 inline-block">
          {{ ContentDetails.SongsNumber }}
        </div>
        <div class="stat-value text-content inline-block ml-3">
          首
        </div>
        <img src="../icons/Message_System_Creation_Report_Icon.svg" alt="听歌周报"
             class="h-14 rounded-xl aspect-square m-auto mt-10"/>
      </div>
    </div>
    <div class="carousel-item stat w-10/12 text-center bg-blue-900">
      <div class="m-auto">
        <div class="text-left stat-title text-white mb-1 font-bold">
          最常听的歌曲
        </div>
        <div class="stat-value text-yellow-500 text-center">
          {{ ContentDetails.FavoriteSong }}
        </div>
      </div>
      <div class="">
        <div class="stat-value text-white inline-block mr-3">
          共播放
        </div>
        <div class="stat-value text-cyan-300 inline-block">
          {{ ContentDetails.SongPlayTimes }}
        </div>
        <div class="stat-value text-white inline-block ml-3">
          次
        </div>
        <img src="../icons/Like_Icon.svg" alt="听歌周报"
             class="h-10 rounded-xl aspect-square m-auto mt-10"/>
      </div>
    </div>
    <div class="carousel-item stat w-10/12 text-center bg-yellow-100">
      <div class="m-auto">
        <div class="text-left stat-title text-accent-content mb-1 font-bold">
          最喜爱的歌手
        </div>
        <div class="stat-value text-secondary text-center">
          {{ ContentDetails.FavoriteSinger }}
        </div>
      </div>
      <div class="">
        <div class="stat-title text-blue-700 font-bold inline-block mr-3">
          共听过他/她的
        </div>
        <div class="stat-value text-content inline-block">
          {{ ContentDetails.SingerPlayTimes }}
        </div>
        <div class="stat-title text-blue-700 font-bold inline-block ml-3">
          首歌曲
        </div>
        <img src="../icons/Message_System_Listening_Report.svg" alt="听歌周报"
             class="h-14 rounded-xl aspect-square m-auto mt-10"/>
      </div>
      <div class="font-bold text-pink-400">
        {{ ContentDetails.SingerPlaySongs }}
      </div>
    </div>
    <div class="carousel-item stat w-10/12 text-center bg-neutral-500">
      <div class="m-auto">
        <div class="text-left stat-title text-cyan-100 mb-1 font-bold">
          喜欢听的风格
        </div>
        <div class="stat-value text-primary">
          {{ ContentDetails.FavoriteStyle }}
        </div>
      </div>
      <div class="stat-value text-yellow-500 inline-block ml-3">
        祝您生活愉快！
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>