<script setup>
import {CurrentSongDetail, IsFullScreen} from "@/js/MusicPlayer.js";
import Music_Card from "@/components/MusicPlayer_Components/MusicPlayerFullView_Components/Music_Card.vue";
import Lyric_Viewer from "@/components/MusicPlayer_Components/MusicPlayerFullView_Components/Lyric_Viewer.vue";
import Comment_Component from '@/components/MusicPlayer_Components/MusicPlayerFullView_Components/Comment_Component.vue'
import { CommentsVisible } from '@/js/Comment.js'
</script>

<template>
  <div class="w-screen h-screen flex flex-row" :style="CurrentSongDetail.gradient">
    <div class="btn  btn-sm fixed top-2 left-2" @click="IsFullScreen=false">
      <img src="../icons/Return_Icon.svg" alt="返回">
    </div>
    <div class="w-2/5 h-full flex">
      <Music_Card class="m-auto"></Music_Card>
    </div>
    <div class="w-3/5 h-full">
      <Comment_Component v-if="CommentsVisible"></Comment_Component>
      <Lyric_Viewer v-else></Lyric_Viewer>
    </div>
  </div>
</template>

<style scoped>

</style>