<!--主界面-->
<template>
  <Transition name="slide">
    <MusicPlayerFullView class="fixed left-0 top-0 z-30" v-if="MusicPlayerVisible&&IsFullScreen"></MusicPlayerFullView>
  </Transition>
  <MusicPlayer_Bar v-if="MusicPlayerVisible&&!IsFullScreen"></MusicPlayer_Bar>

  <div class="w-screen h-screen flex bg-white" v-if="!IsFullScreen">
    <div class="h-screen">
      <Navicat></Navicat>
    </div>
    <div class="flex-1 h-full pl-2 bg-[#FAF7F5]">
      <Transition name="slide">
        <SongDetail v-if="SongDetailVisible" class="z-40 bg-[#FAF7F5]"></SongDetail>
      </Transition>
      <Transition name="slide">
        <Singer_Component v-if="SingerDetailVisible&&!SongDetailVisible"></Singer_Component>
      </Transition>
      <Transition name="slide">
        <SongList_Component v-if="SongListVisible&&!SongDetailVisible" class="z-30"></SongList_Component>
      </Transition>
      <router-view v-if="!SongListVisible&&!SongDetailVisible&&!SingerDetailVisible"></router-view>
    </div>
  </div>

  <MySongListsDialog></MySongListsDialog>

</template>

<script setup>
import Navicat from '@/components/Navicat_Component.vue'
import MusicPlayer_Bar from '@/components/MusicPlayer_Components/MusicPlayer_Bar.vue'
import { GetPlayList, IsFullScreen, MusicPlayerVisible } from '@/js/MusicPlayer.js'
import { UserStore } from '@/stores/User.js'
import { watch } from 'vue'
import MusicPlayerFullView from '@/components/MusicPlayer_Components/MusicPlayerFullView.vue'
import SongList_Component from '@/components/SongList_Component.vue'
import { SongListVisible } from '@/js/SongList.js'
import { SongDetailVisible } from '@/js/SongDetail.js'
import SongDetail from '@/components/SongDetail.vue'
import MySongListsDialog from '@/components/MySongListsDialog.vue'
import Singer_Component from '@/components/Singer_Component.vue'
import { SingerDetailVisible } from '@/js/SingerDetail.js'

watch(() => UserStore().State, GetPlayList)
</script>


<style>
.slide-leave-active {
  transition: transform 0.5s ease;
}

.slide-enter-active {
  transition: transform 0.5s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}
</style>