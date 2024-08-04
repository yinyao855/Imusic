<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { SongDetailVisible } from '@/js/SongDetail.js'
import { WindowWidth } from '@/js/NavicatStatus.js'
import CommentMessages from '@/components/Message_Components/CommentMessages.vue'
import PrivateMessages from '@/components/Message_Components/PrivateMessages.vue'
import SystemMessages from "@/components/Message_Components/SystemMessages.vue";


//当前触发的状态
const activeName = ref('系统通知')

//获取到当前窗口的长宽信息
const windowWidth = ref(window.innerWidth);
const windowHeight = ref(window.innerHeight);

const handleResize = () => {
  windowWidth.value = window.innerWidth;
  windowHeight.value = window.innerHeight;
  WindowWidth.value=windowWidth.value;
};

onMounted(() => {
  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
});
</script>

<template>
  <el-tabs v-if="!SongDetailVisible" v-model="activeName" class="demo-tabs ml-4 mt-2">
    <el-tab-pane label="系统通知" name="系统通知">
      <div :style="{ height: (windowHeight-62) + 'px'}">
        <SystemMessages></SystemMessages>
      </div>
    </el-tab-pane>
    <el-tab-pane label="评论通知" name="评论通知">
      <div :style="{ height: (windowHeight-62) + 'px'}">
        <CommentMessages></CommentMessages>
      </div>
    </el-tab-pane>
    <el-tab-pane label="我的私信" name="我的私信">
      <div :style="{ height: (windowHeight-62) + 'px'}">
        <PrivateMessages></PrivateMessages>
      </div>
    </el-tab-pane>
    <el-tab-pane label="投诉通知" name="投诉通知">
      <div :style="{ height: (windowHeight-62) + 'px'}">

      </div>
    </el-tab-pane>
    <el-tab-pane label="申诉通知" name="申诉通知">
      <div :style="{ height: (windowHeight-62) + 'px'}">

      </div>
    </el-tab-pane>
  </el-tabs>
</template>

<style scoped>
/* 设置未被选中样式 */
::v-deep .el-tabs__item {
  font-size: 20px;
  line-height: 30px;
  text-align: center;
}
</style>