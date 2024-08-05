<!--左侧导航栏-->
<template>
  <div class="relative h-full bg-[#FAF7F5]">
    <el-menu
        default-active="1"
        class="el-menu-vertical-demo h-full use_font"
        :collapse="isCollapse"
        @select="handleSelect"
    >
      <el-menu-item index="0" class="border-b" style="height:80px;padding-left:16px">
        <img src="./icons/User_Icon.svg" alt="用户" class="h-8 mr-3" v-if="ActiveIndex!==0&&user_store.State===false">
        <img src="./icons/User_Active_Icon.svg" alt="用户" class="h-8 mr-3"
             v-else-if="ActiveIndex===0&&user_store.State===false">
        <img :src="user_store.Avatar" alt="头像" class="h-10 mr-4 rounded-full aspect-square" v-else>
        <template #title><span
            style="font-family: 'TsangerYuYangT_W03_W03', sans-serif;" class="text-lg">{{
            user_store.State === true ? user_store.Username : '请先登录'
          }}</span></template>
      </el-menu-item>
      <el-menu-item index="1" class="border-b">
        <img src="./icons/Home_Icon.svg" alt="首页" class="h-4 mr-3 ml-1" v-if="ActiveIndex!==1">
        <img src="./icons/Home_Active_Icon.svg" alt="首页" class="h-4 mr-3 ml-1" v-else>
        <template #title><span
            style="font-family: 'TsangerYuYangT_W03_W03', sans-serif;font-size: 15px;line-height: 22px">首页</span>
        </template>
      </el-menu-item>
      <el-menu-item index="2" class="border-b">
        <img src="./icons/Explore_Icon.svg" alt="探索" class="h-4 mr-3 ml-1" v-if="ActiveIndex!==2">
        <img src="./icons/Explore_Active_Icon.svg" alt="探索" class="h-4 mr-3 ml-1" v-else>
        <template #title><span
            style="font-family: 'TsangerYuYangT_W03_W03', sans-serif;font-size: 15px;line-height: 22px">探索</span>
        </template>
      </el-menu-item>
      <el-menu-item index="3" class="border-b">
        <img src="./icons/Create_Icon.svg" alt="创作中心" class="h-4 mr-3 ml-1" v-if="ActiveIndex!==3">
        <img src="./icons/Create_Active_Icon.svg" alt="创作中心" class="h-4 mr-3 ml-1" v-else>
        <template #title><span
            style="font-family: 'TsangerYuYangT_W03_W03', sans-serif;font-size: 15px;line-height: 22px">创作中心</span>
        </template>
      </el-menu-item>
      <el-menu-item index="4" class="border-b">
        <img src="./icons/CreateLikeSongs_Icon.svg" alt="我的歌单" class="h-4 mr-3 ml-1" v-if="ActiveIndex!==4">
        <img src="./icons/CreateLikeSongs_Active_Icon.svg" alt="我的歌单" class="h-4 mr-3 ml-1" v-else>
        <template #title><span
            style="font-family: 'TsangerYuYangT_W03_W03', sans-serif;font-size: 15px;line-height: 22px">我的歌单</span>
        </template>
      </el-menu-item>
      <el-menu-item index="5" class="border-b">
        <img src="./icons/LikeSongs_Icon.svg" alt="收藏的歌单" class="h-4 mr-3 ml-1" v-if="ActiveIndex!==5">
        <img src="./icons/LikeSongs_Active_Icon.svg" alt="收藏的歌单" class="h-4 mr-3 ml-1" v-else>
        <template #title><span
            style="font-family: 'TsangerYuYangT_W03_W03', sans-serif;font-size: 15px;line-height: 22px">收藏的歌单</span>
        </template>
      </el-menu-item>
      <el-menu-item index="6" class="border-b">
        <img src="./icons/Message_Icon.svg" alt="消息中心" class="h-4 mr-3 ml-1" v-if="ActiveIndex!==6">
        <img src="./icons/Message_Active_Icon.svg" alt="消息中心" class="h-4 mr-3 ml-1" v-else>
        <template #title>
          <span style="font-family: 'TsangerYuYangT_W03_W03', sans-serif;font-size: 15px;line-height: 22px">消息中心</span>
          <div class="bg-red-500 w-5 h-5 rounded-full text-xs flex ml-1" style="font-family: 'TsangerYuYangT_W03_W03', sans-serif;" v-if="MessageNotRead!==0">
            <div class="m-auto">
              {{MessageNotRead}}
            </div>
          </div>
        </template>
      </el-menu-item>
      <el-menu-item index="7" class="border-b">
        <img src="./icons/AboutUs_Icon.svg" alt="关于我们" class="h-4 mr-3 ml-1" v-if="ActiveIndex!==7">
        <img src="./icons/AboutUs_Active_Icon.svg" alt="关于我们" class="h-4 mr-3 ml-1" v-else>
        <template #title><span
            style="font-family: 'TsangerYuYangT_W03_W03', sans-serif;font-size: 15px;line-height: 22px">关于我们</span>
        </template>
      </el-menu-item>
      <el-menu-item index="8">
        <img src="./icons/AboutUs_Icon.svg" alt="设置" class="h-4 mr-3 ml-1" v-if="ActiveIndex!==8">
        <img src="./icons/AboutUs_Active_Icon.svg" alt="设置" class="h-4 mr-3 ml-1" v-else>
        <template #title><span
          style="font-family: 'TsangerYuYangT_W03_W03', sans-serif;font-size: 15px;line-height: 22px">设置</span>
        </template>
      </el-menu-item>
    </el-menu>
    <img class="absolute top-1/2 right-0 translate-x-1/2 h-8 p-1 rounded-full bg-[#FAF7F5] z-10" style="border-width: 1px"
         src="./icons/Expand_Icon.svg" alt="测试" @click="isCollapse=false" v-if="isCollapse">
    <img class="absolute top-1/2 right-0 translate-x-1/2 h-8 p-1 rounded-full bg-[#FAF7F5] z-10" style="border-width: 1px"
         src="./icons/Collapse_Icon.svg" alt="测试" @click="isCollapse=true" v-else>
  </div>
</template>

<script setup>
import {UserStore} from "@/stores/User.js";
import {ref} from 'vue'
import router from "@/router/index.js";
import {watch} from 'vue'
import { ActiveIndex, NavicatWidth } from '@/js/NavicatStatus.js'
import { CheckLogin, GetMySongLists } from '@/js/MySongList.js'
import { GetLikeSongLists } from '@/js/LikeSongLists.js'
import { GetMyCreatedSongs } from '@/js/MyCreates.js'
import { MessageNotRead } from '@/js/Message.js'

const user_store = UserStore(); //用户信息
const isCollapse = ref(false) //是否展开状态栏


watch(()=>isCollapse.value,()=>{
  if(isCollapse.value===true){
    NavicatWidth.value=152;
  }
  else{
    NavicatWidth.value=288;
  }
})

//点击导航栏
const handleSelect = (index) => {
  ActiveIndex.value = parseInt(index);
}

watch(() => ActiveIndex.value, (newValue,oldValue) => {
  switch (newValue) {
    case 0:
      if (user_store.State === false)
        router.push('/login');
      else
        router.push('/home/personalCenter');
      break;
    case 1:
      router.push('/home/homeView');
      break;
    case 2:
      router.push('/home/explore');
      break;
    case 3:
      if(!CheckLogin()){
        ActiveIndex.value=oldValue;
        break;
      }
      GetMyCreatedSongs();
      router.push('/home/create');
      break;
    case 4:
      if(!CheckLogin()){
        ActiveIndex.value=oldValue;
        break;
      }
      GetMySongLists();
      router.push('/home/mySongLists');
      break;
    case 5:
      if(!CheckLogin()){
        ActiveIndex.value=oldValue;
        break;
      }
      GetLikeSongLists();
      router.push('/home/likeSongLists');
      break;
    case 6:
      if(!CheckLogin()){
        ActiveIndex.value=oldValue;
        break;
      }
      router.push('/home/message');
      break;
    case 7:
      router.push('/home/aboutUs');
      break;
    case 8:
      router.push('/home/settings');
      break;
  }
})
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
</style>
