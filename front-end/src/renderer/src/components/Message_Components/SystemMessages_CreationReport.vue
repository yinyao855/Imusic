<script setup>

import {ContentDetails, Contents} from "@/js/SystemMessage.js";


</script>

<template>
  <div class="carousel rounded-box w-full h-96">
    <div class="carousel-item stat w-10/12 text-center bg-cyan-800">
      <div class="m-auto">
        <img src="../icons/Message_System_Creation_Report_Icon.svg" alt="听歌周报"
             class="h-16 rounded-xl aspect-square inline-block"/>
        <div class="stat-value text-yellow-400 font-bold mb-10">
          创作周报
        </div>
        <div class="text-yellow-100 font-bold">
          {{ ContentDetails.StartDateAndEndDate }}
        </div>
      </div>
    </div>
    <div class="carousel-item stat w-10/12 text-center bg-orange-100">
      <div class="m-auto">
        <div class="stat-value text-content inline-block mr-3">
          共上传歌曲
        </div>
        <div class="stat-value text-purple-400 inline-block">
          {{ ContentDetails.SongsNumber }}
        </div>
        <div class="stat-value text-content inline-block ml-3">
          首
        </div>
      </div>
      <div class="">
        <div class="stat-value text-content inline-block mr-3">
          共创建
        </div>
        <div class="stat-value text-purple-400 inline-block">
          {{ ContentDetails.SongListsNumber }}
        </div>
        <div class="stat-value text-content inline-block ml-3">
          个歌单
        </div>
      </div>
    </div>
    <div class="carousel-item stat w-10/12 text-center bg-blue-900">
      <div class="m-auto">
        <div class="stat-value text-yellow-500 text-center">
          您上传的歌曲有
        </div>
        <div class="stat-title text-yellow-100 mt-1 font-bold">
          {{ ContentDetails.UploadSongs }}
        </div>
      </div>
      <img src="../icons/Like_Icon.svg" alt="听歌周报"
           class="h-10 rounded-xl aspect-square m-auto"/>
      <div class="">
        <div class="stat-value text-white inline-block mr-3">
          共获得
        </div>
        <div class="stat-value text-cyan-300 inline-block">
          {{ ContentDetails.FavoriteSongsNumber }}
        </div>
        <div class="stat-value text-white inline-block ml-3">
          个喜欢
        </div>
      </div>
    </div>
    <div class="carousel-item stat w-10/12 text-center bg-yellow-100">
      <div class="m-auto">
        <div class="stat-value text-secondary text-center">
          您创建的歌单
        </div>
        <div class="stat-title text-accent-content mt-1 font-bold">
          {{ ContentDetails.CreateSongLists }}
        </div>
      </div>
      <img src="../icons/Like_SongList_Icon.svg" alt="听歌周报"
           class="h-14 rounded-xl aspect-square m-auto"/>
      <div class="">
        <div class="stat-value text-blue-700 font-bold inline-block mr-3">
          共获得
        </div>
        <div class="stat-value text-content inline-block">
          {{ ContentDetails.FavoriteSongListsNumber }}
        </div>
        <div class="stat-value text-blue-700 font-bold inline-block ml-3">
          个收藏
        </div>
      </div>
      <div class="font-bold text-pink-400">
        {{ ContentDetails.SingerPlaySongs }}
      </div>
    </div>
    <div class="carousel-item stat w-10/12 text-center bg-neutral-500">
      <div class="stat-value text-yellow-500 inline-block m-auto">
        祝您创作愉快！
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>