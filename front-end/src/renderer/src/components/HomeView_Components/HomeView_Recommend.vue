<!--推荐页面的组件-->
<script setup>
import {BeforeEnterHomeView, HomeView_HotSongs, HomeView_NewSongs} from "@/js/BeforeEnterHomeView.js";
import {onMounted} from "vue";
import {MusicPlayerVisible} from "@/js/MusicPlayer.js";
import SongLists_Scroll from "@/components/HomeView_Components/Recommend_Components/SongLists_Scroll.vue";
import Singer_Scroll from "@/components/HomeView_Components/Recommend_Components/Singer_Scroll.vue";
import SongTable from "@/components/SongTable.vue";

//获取当前页展示数据
onMounted(BeforeEnterHomeView);


</script>

<template>
  <div class="w-full flex flex-wrap bg-[#FAF7F5] h-full overflow-auto">
    <div class="w-full">
      <div class="text-xl">推荐歌单</div>
      <SongLists_Scroll></SongLists_Scroll>
      <el-divider class="w-full"></el-divider>
    </div>

    <div class="w-full">
      <div class="text-xl">推荐艺人</div>
      <Singer_Scroll></Singer_Scroll>
      <el-divider class="w-full"></el-divider>
    </div>
    <div class="w-full flex flex-row">
      <!--      最热门歌曲-->
      <div class="w-1/2 pr-2">
        <div class="text-xl">热门单曲</div>
        <div class="overflow-visible">
          <SongTable :Songs="HomeView_HotSongs"></SongTable>
        </div>
      </div>
      <!--      最新歌曲-->
      <div class="w-1/2 pl-2">
        <div class="text-xl">最新上传</div>
        <div class="overflow-visible">
          <SongTable :Songs="HomeView_NewSongs"></SongTable>
        </div>
      </div>
    </div>
    <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
  </div>
</template>

<style scoped>

</style>