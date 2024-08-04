<template>
  <div class="h-[120px] mb-2 w-full px-3 fixed bottom-0 left-0 z-20">
    <div class="h-[120px] w-full px-2 bg-[#C9C7C5] bg-opacity-90 rounded-3xl">
      <div class="w-full h-full flex flex-row">
        <div class="h-full ml-4 flex">
          <img :src="CurrentSongDetail.cover" alt="当前封面" class="aspect-square rounded-md h-[90%] my-auto">
        </div>

        <div class="h-full flex-1 flex">
          <div class="my-auto ml-4">
            <div class="text-xl font-bold mb-1">{{ CurrentSongDetail.title }}</div>
            <div class="text-sm">{{ CurrentSongDetail.singer }}</div>
          </div>
        </div>

        <div class="w-1/2 h-full">
          <div class="flex h-[62%] justify-around w-1/2 mx-auto">
            <!--播放上一首-->
            <div class="tooltip my-auto tooltip-primary" data-tip="上一首">
              <button
                  class="btn btn-sm rounded-md border-none fill-zinc-900 glass">
                <img src="../icons/NextSong_Icon.svg" style="transform: rotate(180deg);" alt="上一首" @click="PreviousSong">
              </button>
            </div>
            <!--播放与暂停-->
            <div class="tooltip my-auto tooltip-primary" data-tip="播放与暂停">
              <button class="btn rounded-md border-none glass"
                      @click="IsPlaying = !IsPlaying">
                <img v-if="!IsPlaying" src="../icons/Play_Icon.svg" alt="播放">
                <img v-else src="../icons/Suspend_Icon.svg" alt="暂停">
              </button>
            </div>
            <!--播放下一首-->
            <div class="tooltip my-auto tooltip-primary" data-tip="下一首">
              <button class="btn btn-sm rounded-md border-none glass" @click="NextSong">
                <img src="../icons/NextSong_Icon.svg" alt="下一首">
              </button>
            </div>
          </div>
          <input type="range" min="0" :max="Duration" v-model="CurrentTime" class="range range-xs range-primary w-full"
                 @change="IsDragging=true"/>
          <div class="flex">
            <div class="text-sm">{{ SecondToTime(CurrentTime) }}</div>
            <div class="flex-1"></div>
            <div class="text-sm">{{ SecondToTime(parseInt(Duration)) }}</div>
          </div>
        </div>

        <div class="w-1/4 ml-8 flex justify-around">

          <!--控制播放方式-->
          <button class="btn btn-sm rounded-md border-none glass tooltip my-auto tooltip-primary" @click="PlayType=(PlayType+1)%3"
                  :data-tip="MusicPlayModeDataTip[PlayType]">
            <img src="../icons/List_Circulate_Icon.svg" v-if="PlayType === 0" alt="列表循环">
            <img src="../icons/Single_Circulate_Icon.svg" v-if="PlayType === 1" alt="单曲循环">
            <img src="../icons/Random_Play_Icon.svg" v-if="PlayType === 2" alt="随机播放">
          </button>
          <!--控制音量-->
          <div class="my-auto flex">
            <button class="btn btn-sm rounded-md border-none glass">
              <img src="../icons/Volume1_Icon.svg" alt="音量" v-if="VolumePercent<=0">
              <img src="../icons/Volume2_Icon.svg" alt="音量" v-else-if="VolumePercent<=33">
              <img src="../icons/Volume3_Icon.svg" alt="音量" v-else-if="VolumePercent<=66">
              <img src="../icons/Volume4_Icon.svg" alt="音量" v-else>
            </button>
            <input type="range" min="0" max="100" class="range range-secondary range-xs my-auto mx-2"
                   v-model="VolumePercent"/>
          </div>
          <!--播放列表-->
          <button
              class="border-none my-auto tooltip btn btn-sm z-50 glass tooltip-primary"
              data-tip="播放列表" @click="PlayListVisible=!PlayListVisible">
            <img src="../icons/Menu_Icon.svg" alt="播放列表">
          </button>

          <!--全屏播放器-->
          <button class="btn btn-sm rounded-md border-none glass tooltip my-auto tooltip-primary" data-tip="全屏显示"
                  @click="IsFullScreen=true;CommentsVisible=false">
            <img src="../icons/FullScreen_Icon.svg" alt="全屏">
          </button>
        </div>
      </div>
    </div>
  </div>

  <transition name="slide">
    <PlayList_Component v-if="PlayListVisible"></PlayList_Component>
  </transition>
</template>

<script setup>
import {
  CurrentSongDetail,
  CurrentTime,
  Duration,
  IsDragging,
  IsFullScreen,
  IsPlaying, MusicPlayModeDataTip,
  NextSong,
  PlayListVisible,
  PlayType, PreviousSong,
  VolumePercent
} from "@/js/MusicPlayer.js";
import {SecondToTime} from '@/js/BeforeEnterHomeView.js'
import PlayList_Component from "@/components/PlayList_Component.vue";
import { CommentsVisible } from '@/js/Comment.js'
</script>


<style scoped>

</style>