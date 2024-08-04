<!--我的创作-->
<script setup>
import { MyCreatedSongs } from '@/js/MyCreates.js'
import { MusicPlayerVisible } from '@/js/MusicPlayer.js'
import EditSongsTable from '@/components/CreateCenter_Components/MyCreatedSongs_Components/EditSongsTable.vue'
import { EditSongVisible } from '@/js/SongDetail.js'
import EditSongFrame from '@/components/CreateCenter_Components/MyCreatedSongs_Components/EditSongFrame.vue'
</script>

<template>
  <div class="w-full h-full" v-if="!EditSongVisible">
    <EditSongsTable :Songs="MyCreatedSongs"></EditSongsTable>
    <div class="w-full h-32" v-if="MusicPlayerVisible"></div>
  </div>

  <Transition name="slide">
    <EditSongFrame v-if="EditSongVisible" class="z-40 bg-[#FAF7F5]"></EditSongFrame>
  </Transition>
</template>

<style scoped>

</style>