<template>
  <el-tabs v-if="!SongDetailVisible" v-model="activeName" class="demo-tabs ml-4 mt-2">
    <el-tab-pane label="歌曲" name="歌曲">
      <div :style="{ height: (windowHeight-62) + 'px'}">
        <Explore_Song></Explore_Song>
      </div>
    </el-tab-pane>
    <el-tab-pane label="歌单" name="歌单">
      <div :style="{ height: (windowHeight-62) + 'px'}">
        <Explore_SongList></Explore_SongList>
      </div>
    </el-tab-pane>
  </el-tabs>

</template>
<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { SongDetailVisible } from '@/js/SongDetail.js'
import { WindowWidth } from '@/js/NavicatStatus.js'
import Explore_Song from '@/components/Explore_Components/Explore_Song.vue'
import Explore_SongList from '@/components/Explore_Components/Explore_SongList.vue'

//当前触发的状态
const activeName = ref('歌曲')

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