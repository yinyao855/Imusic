<!--歌曲列表（显示是否被当前用户喜爱）-->
<script setup>
import {AddSongToCurrentPlayList, HandlePlayNow} from "@/js/MusicPlayer.js";
import {ShowSongDetail} from "@/js/SongDetail.js";
import {AddFavorSong, DeleteFavorSong} from "@/js/Favor.js";
import { ActiveDialog, CheckLogin } from '@/js/MySongList.js'

const Songs = defineModel('Songs');

//添加喜爱歌曲
const PageAddFavorSong = (SongId, index) => {
  if (!CheckLogin()) {
    return
  }
  Songs.value[index].user_like = true;
  AddFavorSong(SongId);
}

//删除喜爱歌曲
const PageDeleteFavorSong = (SongId, index) => {
  if (!CheckLogin()) {
    return
  }
  Songs.value[index].user_like = false;
  DeleteFavorSong(SongId);
}

</script>

<template>
  <table class="table">
    <thead>
    <tr>
      <th class="w-[5%]">喜欢</th>
      <th>音乐标题</th>
      <th>歌手</th>
      <th>时长</th>
      <th>操作</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(Song,index) in Songs" :key="index"
        class="transition-colors ease-in duration-150 hover:bg-gray-300 hover:bg-opacity-40 cursor-pointer">
      <td>
        <img src="./icons/Like_Icon.svg" alt="喜欢" class="w-6 h-6" v-if="Song.user_like===true"
             @click="PageDeleteFavorSong(Song.id,index)">
        <img src="./icons/NotLike_Icon.svg" alt="不喜欢" class="w-6 h-6" v-else
             @click="PageAddFavorSong(Song.id,index)">
      </td>
      <td @click="HandlePlayNow(Song.id)">
        <div class="flex items-center gap-3">
          <div class="avatar">
            <div class="mask mask-squircle h-12 w-12">
              <img
                  :src="Song.cover"
                  alt="封面"/>
            </div>
          </div>
          <div>
            <div class="font-bold">{{ Song.title }}</div>
          </div>
        </div>
      </td>
      <td @click="HandlePlayNow(Song.id)">
        {{ Song.singer }}
      </td>
      <td @click="HandlePlayNow(Song.id)">{{ Song.duration }}</td>
      <th>
        <div class="dropdown dropdown-top dropdown-end z-10">
          <div tabindex="0" role="button" class="btn btn-ghost btn-xs">
            <img src="./icons/Menu_Icon.svg" alt="详情">
          </div>
          <ul tabindex="0"
              class="dropdown-content dropdown-left dropdown-top menu rounded-box z-50 w-52 p-2 shadow bg-base-100"
              style="width:300px">
            <li>
              <div>
                <img :src="Song.cover" alt="封面" class="aspect-square h-12 w-12 ml-0 pl-0 rounded-xl">
                <a class="font-semibold text-sm">{{ Song.title }}</a>
                <br>
                <a class="block text-xs mr-0">{{ Song.singer }}</a>
              </div>
            </li>
            <li>
              <div class="text-sm font-semibold" @click="HandlePlayNow(Song.id)">
                <img src="./icons/PlayNow_Icon.svg" alt="立即播放" class="ml-1">
                立即播放
              </div>
            </li>
            <li>
              <div class="text-sm font-semibold" @click="AddSongToCurrentPlayList(Song)">
                <img src="./icons/AddToPlayList_Icon.svg" alt="添加到播放列表">
                添加到播放列表
              </div>
            </li>
            <li>
              <div class="text-sm font-semibold" @click="ActiveDialog(Song.id)">
                <img src="./icons/AddToSongList_Icon.svg" alt="添加到歌单">
                添加到歌单
              </div>
            </li>
            <li>
              <div class="text-sm font-semibold" @click="ShowSongDetail(Song.id)">
                <img src="./icons/DetailInformation_Icon.svg" alt="详细信息">
                详细信息
              </div>
            </li>
          </ul>
        </div>
      </th>
    </tr>
    </tbody>
  </table>
</template>

<style scoped>

</style>