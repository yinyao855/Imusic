<script setup>
import SongTable from "@/components/SongTable.vue";
import {HomeView_NewSongView_NewSongs} from "@/js/BeforeEnterHomeView.js";
import {MusicPlayerVisible} from "@/js/MusicPlayer.js";
</script>

<template>
  <div class="w-full flex flex-wrap bg-[#FAF7F5] h-full overflow-auto">
    <SongTable :Songs="HomeView_NewSongView_NewSongs"></SongTable>
    <div class="w-full h-32" v-if="MusicPlayerVisible"></div>
  </div>
</template>

<style scoped>

</style>