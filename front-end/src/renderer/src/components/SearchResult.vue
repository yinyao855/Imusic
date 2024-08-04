<!--显示查询结果的组件-->
<script setup>
import {SearchResult, SearchResultVisible} from "@/js/Search.js";
import {MusicPlayerVisible} from "@/js/MusicPlayer.js";
import SongTable_HasFavor from "@/components/SongTable_HasFavor.vue";
import {ref} from "vue";

const Songs=ref(SearchResult);
</script>

<template>
  <div class="w-full h-full">
    <div class="btn btn-sm" @click="SearchResultVisible=false">
      <img src="./icons/Return_Icon.svg" alt="返回">
    </div>
    <SongTable_HasFavor v-model:Songs="Songs"></SongTable_HasFavor>
    <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
  </div>
</template>

<style scoped>

</style>