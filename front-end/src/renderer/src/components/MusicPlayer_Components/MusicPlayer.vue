<template>
  <div>
    <!-- 音频播放器 -->
    <audio ref="audioPlayer" controls @timeupdate="updateProgress" style="display:none" @ended="NextSong">
      <source :src="CurrentSongDetail.audio" type="audio/mpeg">
      Your browser does not support the audio element.
    </audio>
  </div>
</template>

<script setup>
import {onMounted, onBeforeUnmount, watch} from 'vue';
import {
  CurrentSongDetail,
  CurrentTime,
  IsDragging,
  IsPlaying, NextSong,
  TotalTime,
  Volume
} from "@/js/MusicPlayer.js";
import { GetComments } from '@/js/Comment.js'

// 音频播放器对象
let audioPlayer = null;

// 更新播放进度
const updateProgress = () => {
  CurrentTime.value = audioPlayer.currentTime.toFixed(0);
};

// 在组件挂载后设置音频播放器对象，并监听播放进度事件
onMounted(() => {
  audioPlayer = document.querySelector('audio');
  audioPlayer.addEventListener('timeupdate', updateProgress);
  audioPlayer.addEventListener('loadedmetadata', () => {
    TotalTime.value = audioPlayer.duration.toFixed(2);
  });
  audioPlayer.volume = Volume.value; // 初始化音量
  audioPlayer.play();
});

//监听获取评论
watch(()=>CurrentSongDetail.value,()=>{
  GetComments(CurrentSongDetail.value.id);
})

// 监听当前音频源变化
watch(() => CurrentSongDetail.value.audio, () => {
  audioPlayer.src = CurrentSongDetail.value.audio;
  CurrentTime.value = 0;
  audioPlayer.play();
})

// 组件卸载前移除事件监听
onBeforeUnmount(() => {
  audioPlayer.removeEventListener('timeupdate', updateProgress);
});

//调节是否播放
watch(() => IsPlaying.value, () => {
  if (IsPlaying.value) {
    audioPlayer.play();
  } else {
    audioPlayer.pause();
  }
})

watch(() => IsDragging.value, () => {
  if (IsDragging.value === true) {
    audioPlayer.currentTime = CurrentTime.value;
    IsDragging.value = false;
  }
})

//调节当前音量
watch(() => Volume.value, () => {
  audioPlayer.volume = Volume.value;
});
</script>

<style>

</style>
