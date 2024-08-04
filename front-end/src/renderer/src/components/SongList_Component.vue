<!--歌单详情展示-->
<script setup>
import { MusicPlayerVisible, PlayAll } from '@/js/MusicPlayer.js'
import { AddLikeSongList, DeleteLikeSongList, SongListDetail, SongListVisible } from '@/js/SongList.js'
import SongTable_HasFavor from '@/components/SongTable_HasFavor.vue'
import { ref,onMounted,watch } from 'vue'
import { NavicatWidth, WindowWidth } from '@/js/NavicatStatus.js'
import { CheckLogin } from '@/js/MySongList.js'
import { useTransition } from '@vueuse/core'
import { SubscribeUser } from '@/js/SubscribeUser.js'

//歌单中的歌曲
const Songs = ref(SongListDetail.value.songs)

//本地处理添加以及减少的问题
const ThisAddLikeSongList = (id) => {
  if (!CheckLogin()) {
    return
  }
  SongListDetail.value.like++
  SongListDetail.value.user_favor = true
  AddLikeSongList(id)
}

const ThisDeleteLikeSongList = (id) => {
  if (!CheckLogin()) {
    return
  }
  SongListDetail.value.like--
  SongListDetail.value.user_favor = false
  DeleteLikeSongList(id)
}

//喜爱部分动画
const LikeCount=ref(0);
const outputValue = useTransition(LikeCount, {
  duration: 1000,
})
onMounted(()=>{
  LikeCount.value=SongListDetail.value.like;
})
watch(()=>SongListDetail.value.like,(newVal)=>{
  LikeCount.value=newVal;
});

const SubScribe=(id)=>{
  SongListDetail.value.isSubscribed=!SongListDetail.value.isSubscribed;
  SubscribeUser(id);
}
</script>

<template>
  <div class="h-screen overflow-auto flex flex-row flex-wrap">
    <div class="btn btn-sm mt-3 ml-2 z-40" @click="SongListVisible=false">
      <img src="./icons/Return_Icon.svg" alt="返回">
    </div>
    <!--    背景模糊-->
    <div class="w-full h-1/3 absolute overflow-hidden" style="filter:blur(12px)"
         :style="{width:`${WindowWidth-NavicatWidth+88}px`}">
      <img class="w-full aspect-[3/1]" :src="SongListDetail.cover" alt="封面">
    </div>
    <!--    歌单详情-->
    <div class="w-full h-1/3 absolute z-10" :style="{width:`${WindowWidth-NavicatWidth+88}px`}">
      <div class="w-full h-full flex flex-row z-10">
        <div class="h-3/4 my-auto ml-20">
          <img class="h-full aspect-square rounded-2xl" :src="SongListDetail.cover" alt="封面">
        </div>
        <div class="h-3/4 my-auto ml-8 flex">
          <div class="my-auto block">
            <div class="text-white text-3xl">
              {{ SongListDetail.title }}
            </div>
            <div class="w-full mt-3 text-white text-lg">
              <div class="inline tooltip tooltip-primary" :data-tip="SongListDetail.isSubscribed===false?'关注用户':'取消关注'" @click="SubScribe(SongListDetail.owner)">
                <img src="./icons/SubscribeUser_Icon.svg" alt="关注" class="inline" v-if="SongListDetail.isSubscribed">
                <img src="./icons/NotSubscribeUser_Icon.svg" alt="未关注" class="inline" v-else>
              </div>
              <span class="ml-2">{{ SongListDetail.owner }}</span>
              <span>・</span>
              <span>{{ SongListDetail.create_date }}</span>
            </div>
            <div class="flex">
              <div class="dropdown w-full mt-3 block">
                <div tabindex="0" role="button" class="btn m-1 btn-sm">简介</div>
                <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-30 p-2 shadow text-sm"
                    style="width:300px">
                  <li><a>{{ SongListDetail.introduction === 'null' ? '无简介' : SongListDetail.introduction }}</a></li>
                </ul>
              </div>
            </div>

            <div class="text-white text-lg btn btn-sm btn-success mt-3" @click="PlayAll(SongListDetail.songs)">
              <span class="ml-3">播放全部</span>
              <img src="./icons/Plus_Icon.svg" alt="加" class="h-4 mr-3">
            </div>
            <div class="mt-3 flex" v-if="SongListDetail.mode===1">
              <img src="./icons/Like_SongList_Icon.svg" alt="喜欢" class="h-6" v-if="SongListDetail.user_favor===true"
                   @click="ThisDeleteLikeSongList(SongListDetail.id)">
              <img src="./icons/NotLike_SongList_Icon.svg" alt="不喜欢" class="h-6" v-else
                   @click="ThisAddLikeSongList(SongListDetail.id)">
              <div class="flex h-7 ml-3">
                <div class="my-auto text-white">{{ outputValue.toFixed(0) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="h-2/3 absolute bottom-0 px-4" :style="{width:`${WindowWidth-NavicatWidth+88}px`}">
      <SongTable_HasFavor v-model:Songs="Songs" class="w-full"></SongTable_HasFavor>
      <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
    </div>
  </div>
</template>

<style scoped>
</style>