<template>
  <el-tabs v-if="!SongDetailVisible" v-model="activeName" class="demo-tabs ml-4 mt-2" @tab-click="handleClick">
    <el-tab-pane label="我的创作" name="我的创作">
      <div :style="{ height: (windowHeight-62) + 'px'}">
        <MyCreatedSongs></MyCreatedSongs>
      </div>
    </el-tab-pane>
    <el-tab-pane label="创作歌曲" name="创作歌曲">
      <div :style="{ height: (windowHeight-62) + 'px'}">
        <CreateSong></CreateSong>
      </div>
    </el-tab-pane>
    <el-tab-pane label="创建歌单" name="创建歌单">
      <div :style="{ height: (windowHeight-62) + 'px'}">
        <CreateSongList></CreateSongList>
      </div>
    </el-tab-pane>
  </el-tabs>

</template>
<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { EditSongVisible, SongDetailVisible } from '@/js/SongDetail.js'
import { WindowWidth } from '@/js/NavicatStatus.js'
import MyCreatedSongs from '@/components/CreateCenter_Components/MyCreatedSongs.vue'
import CreateSong from '@/components/CreateCenter_Components/CreateSong.vue'
import CreateSongList from '@/components/CreateCenter_Components/CreateSongList.vue'
import { GetMyCreatedSongs } from '@/js/MyCreates.js'

//当前触发的状态
const activeName = ref('我的创作')

const handleClick = (tab, event) => {
  console.log(tab, event)
}

//在跳转到其他页面的时候关闭当前的歌曲编辑
watch(() => activeName.value, () => {
  EditSongVisible.value = false;
  if(activeName.value==='我的创作'){
    GetMyCreatedSongs();
  }
})

//获取到当前窗口的长宽信息
const windowWidth = ref(window.innerWidth)
const windowHeight = ref(window.innerHeight)

const handleResize = () => {
  windowWidth.value = window.innerWidth
  windowHeight.value = window.innerHeight
  WindowWidth.value = windowWidth.value
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* 设置未被选中样式 */
::v-deep .el-tabs__item {
  font-size: 20px;
  line-height: 30px;
  text-align: center;
}
</style>