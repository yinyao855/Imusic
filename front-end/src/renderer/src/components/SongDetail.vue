<!--歌曲详情-->
<script setup>
import {GetSongDetail, LyricList, SongDetail, SongDetailVisible, SongId} from "@/js/SongDetail.js";
import {onMounted} from "vue";
import {HandlePlayNow, MusicPlayerVisible} from "@/js/MusicPlayer.js";
import { SubscribeUser } from '@/js/SubscribeUser.js'

onMounted(GetSongDetail)

const SubScribe=(id)=>{
  SongDetail.value.isSubscribed=!SongDetail.value.isSubscribed;
  SubscribeUser(id);
}
</script>

<template>
  <div class="h-screen w-full overflow-auto flex flex-row z-50 bg-[#FAF7F5]">
    <div class="block w-2/5 my-auto">
      <div class="btn btn-sm mt-2" @click="SongDetailVisible=false">
        <img src="./icons/Return_Icon.svg" alt="返回">
      </div>
      <div class="mt-4">
        <img :src="SongDetail.cover" alt="封面" class="aspect-square rounded-md w-72 ml-12 my-2">
        <div class="ml-12 flex flex-wrap my-1">
          <div class="text-4xl w-full my-1">{{ SongDetail.title }}</div>
          <div class="text-base text-gray-60 ml-2 w-full my-1">歌手:{{ SongDetail.singer }}</div>
          <div class="w-full my-1">
            <div class="inline tooltip tooltip-primary" :data-tip="SongDetail.isSubscribed===false?'关注用户':'取消关注'" @click="SubScribe(SongDetail.uploader)">
              <img src="./icons/SubscribeUser_Icon.svg" alt="关注" class="inline" v-if="SongDetail.isSubscribed">
              <img src="./icons/NotSubscribeUser_Icon.svg" alt="未关注" class="inline" v-else>
            </div>
            <span class="ml-2">{{ SongDetail.uploader }}</span>
            <span>・</span>
            <span>{{ SongDetail.upload_date }}</span>
          </div>
          <div class="dropdown w-full my-1">
            <div tabindex="0" role="button" class="btn m-1 btn-sm">简介</div>
            <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-30 p-2 shadow text-sm"
                style="width:600px">
              <li><a>{{ SongDetail.introduction }}</a></li>
            </ul>
          </div>
          <div class="w-full flex my-2">
            <div
                class="bg-blue-500 hover:bg-blue-600 transition-colors ease-in duration-300 h-10 rounded-full w-32 flex mr-4"
                @click="HandlePlayNow(SongId)">
              <div class="m-auto text-white flex">
                <img src="./icons/Play_White_Icon.svg" alt="播放" class="h-6 inline my-auto mr-2">
                播放
                <div class="w-1 h-full"></div>
              </div>
            </div>
            <div class="bg-red-500 hover:bg-red-700 transition-colors ease-in duration-300 h-10 rounded-full w-32 flex">
              <div class="m-auto text-white flex">
                <img src="./icons/Report_Icon.svg" alt="举报" class="h-6 inline my-auto mr-2">
                举报
                <div class="w-1 h-full"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
    </div>
    <div class="block w-3/5 h-full overflow-auto border-l-2">
      <div class="w-full flex">
        <span class="mx-auto text-2xl my-2">歌词</span>
      </div>
      <div class="w-full flex" v-for="(Content,index) in LyricList" :key="index">
        <span class="mx-auto">{{ Content.content }}</span>
      </div>
      <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
    </div>

  </div>
</template>

<style scoped>

</style>