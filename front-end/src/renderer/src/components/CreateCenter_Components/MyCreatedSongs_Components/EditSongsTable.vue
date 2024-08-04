<!--歌曲列表-->
<script setup>
import {AddSongToCurrentPlayList, HandlePlayNow} from "@/js/MusicPlayer.js";
import { ShowEditSong } from '@/js/SongDetail.js'
import { ActiveDialog } from '@/js/MySongList.js'

const props = defineProps({
  Songs: Array
})
</script>

<template>
  <table class="table">
    <thead>
    <tr>
      <th>音乐标题</th>
      <th>歌手</th>
      <th>时长</th>
      <th>上传日期</th>
      <th>操作</th>

    </tr>
    </thead>
    <tbody>
    <tr v-for="(Song,index) in props.Songs" :key="index"
        class="transition-colors ease-in duration-150 hover:bg-gray-300 hover:bg-opacity-40 cursor-pointer">
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
      <td @click="HandlePlayNow(Song.id)">{{ Song.upload_date }}</td>
      <th>
        <div class="dropdown dropdown-bottom dropdown-left z-10">
          <div tabindex="0" role="button" class="btn btn-ghost btn-xs">
            <img src="../../icons/Menu_Icon.svg" alt="详情">
          </div>
          <ul tabindex="0"
              class="dropdown-content menu rounded-box z-[1] w-52 p-2 shadow bg-base-100"
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
                <img src="../../icons/PlayNow_Icon.svg" alt="立即播放" class="ml-1">
                立即播放
              </div>
            </li>
            <li>
              <div class="text-sm font-semibold" @click="AddSongToCurrentPlayList(Song)">
                <img src="../../icons/AddToPlayList_Icon.svg" alt="添加到播放列表">
                添加到播放列表
              </div>
            </li>
            <li>
              <div class="text-sm font-semibold" @click="ActiveDialog(Song.id)">
                <img src="../../icons/AddToSongList_Icon.svg" alt="添加到歌单">
                添加到歌单
              </div>
            </li>
            <li>
              <div class="text-sm font-semibold" @click="ShowEditSong(Song.id)">
                <img src="../../icons/DetailInformation_Icon.svg" alt="编辑歌曲">
                编辑歌曲
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