<script setup>
import MusicPlayer from "@/components/MusicPlayer_Components/MusicPlayer.vue";
import {MusicPlayerVisible} from "@/js/MusicPlayer.js";
import {onMounted, onUnmounted, ref ,watch} from 'vue'
import { GetAllMessage } from '@/js/Message.js'
import { UserStore } from '@/stores/User.js'



//当前时间
const currentTime = ref(0)
//计时器
let timer = null

//开始计时
const startTimer = () => {
  timer = setInterval(() => {
    currentTime.value++
  }, 1000) // 每秒钟增加1秒
}

onMounted(() => {
  startTimer()
})

onUnmounted(() => {
  clearInterval(timer)
})

watch(()=>UserStore().State,()=>{
  if(UserStore().State===true){
    GetAllMessage();
  }
});

//每五秒获取一次消息
watch(()=>currentTime.value,()=>{
  if(currentTime.value>=5&&UserStore().State===true){
    GetAllMessage();
    currentTime.value=0;
  }
})
</script>

<template>
  <router-view v-slot="{ Component }" class="w-screen h-screen">
    <transition name="fade">
      <component :is="Component" />
    </transition>
  </router-view>
  <MusicPlayer class="fixed"  v-if="MusicPlayerVisible"></MusicPlayer>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.use_font {
  font-family: 'TsangerYuYangT_W03_W03',sans-serif;
}

#app{
  font-family: 'TsangerYuYangT_W03_W03', sans-serif;
}
</style>
