<template>

  <Search_Input v-if="!SongDetailVisible"></Search_Input>
  <el-tabs v-if="!SongDetailVisible" v-model="activeName" class="demo-tabs ml-4 mt-2">
    <el-tab-pane label="推荐" name="推荐">
      <div :style="{ height: (windowHeight-62) + 'px'}">
        <Transition name="slide">
          <SearchResult v-if='SearchResultVisible'></SearchResult>
          <HomeView_Recommend v-else></HomeView_Recommend>
        </Transition>
      </div>
    </el-tab-pane>
    <el-tab-pane label="最新上传" name="最新上传">
      <div :style="{ height: (windowHeight-62) + 'px'}">
        <Transition name="slide">
          <SearchResult v-if='SearchResultVisible'></SearchResult>
          <HomeView_NewestSongs v-else></HomeView_NewestSongs>
        </Transition>
      </div>
    </el-tab-pane>
  </el-tabs>

</template>
<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import HomeView_Recommend from '@/components/HomeView_Components/HomeView_Recommend.vue'
import HomeView_NewestSongs from '@/components/HomeView_Components/HomeView_NewestSongs.vue'
import { SongDetailVisible } from '@/js/SongDetail.js'
import Search_Input from '@/components/HomeView_Components/Search_Input.vue'
import SearchResult from '@/components/SearchResult.vue'
import { SearchResultVisible } from '@/js/Search.js'
import { WindowWidth } from '@/js/NavicatStatus.js'

//当前触发的状态
const activeName = ref('推荐')

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