<!--音乐操作的卡片-->
<script setup>
import {
  CurrentSongDetail,
  CurrentTime,
  Duration, IsDragging,
  IsPlaying, MusicPlayModeDataTip,
  NextSong,
  PlayType,
  PreviousSong,
} from "@/js/MusicPlayer.js";
import {SecondToTime} from "@/js/BeforeEnterHomeView.js";
import { CommentsVisible, GetComments } from '@/js/Comment.js'


//更改是否显示评论的状态
const ChangeCommentMode = (id) => {
  if (CommentsVisible.value === false) {
    GetComments(id);
  } else {
    CommentsVisible.value = false;
  }
}
</script>

<template>
  <div class="card">
    <label for="uploads">
      <div class="card__img">
        <img :src="CurrentSongDetail.cover"
             :class="{'content':true, 'rotate':IsPlaying,'stop':!IsPlaying, 'rounded-full':true, 'w-[243px]':true, 'h-[243px]':true}"
             alt="封面">
      </div>
      <div class="card__title" style="font-weight: bolder !important;">{{ CurrentSongDetail.title }}</div>
      <div class="card__subtitle">{{ CurrentSongDetail.singer }}</div>
      <div class="card__wrapper">
        <div class="card__time card__time-passed">{{ SecondToTime(parseInt(CurrentTime)) }}</div>
        <div class="card__timeline">
          <input type="range" min="0" :max="Duration" v-model="CurrentTime" @change="IsDragging=true">
        </div>
        <div class="card__time card__time-left">{{ SecondToTime(parseInt(Duration)) }}</div>
      </div>
    </label>
    <div class="card__wrapper">
      <div class="tooltip my-auto tooltip-primary" :data-tip="MusicPlayModeDataTip[PlayType]">
        <button class=" card__btn"
                @click="PlayType=(PlayType+1)%3">
          <img src="../../icons/List_Circulate_White_Icon.svg" v-if="PlayType === 0" alt="列表循环">
          <img src="../../icons/Single_Circulate_White_Icon.svg" v-if="PlayType === 1" alt="单曲循环">
          <img src="../../icons/Random_Play_White_Icon.svg" v-if="PlayType === 2" alt="随机播放">
        </button>
      </div>
      <button class="card__btn tooltip tooltip-primary" @click="PreviousSong" data-tip="上一首">
        <img src="../../icons/PreviousSong_White_Icon.svg" alt="上一首">
      </button>
      <button class="card__btn card__btn-play tooltip tooltip-primary" @click="IsPlaying = !IsPlaying" data-tip="播放/暂停">
        <img v-if="!IsPlaying" src="../../icons/Play_Icon.svg" alt="播放">
        <img v-else src="../../icons/Suspend_Icon.svg" alt="暂停">
      </button>
      <button class="card__btn tooltip tooltip-primary" @click="NextSong" data-tip="下一首">
        <img src="../../icons/NextSong_White_Icon.svg" alt="下一首">
      </button>
      <button class="card__btn tooltip tooltip-primary" data-tip="显示/关闭评论" @click="ChangeCommentMode(CurrentSongDetail.id)">
        <img src="../../icons/Comment_Icon.svg" alt="评论">
      </button>
    </div>
  </div>
</template>

<style scoped>
@import url('../../../css/Music_Card.css');
</style>