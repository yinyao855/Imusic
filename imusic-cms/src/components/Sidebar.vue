<script setup>
import {addTab} from "@/js/tabManager.js";
import {
  Menu as IconMenu,
  Setting,
  House, User, Files, Headset, Star,
} from '@element-plus/icons-vue'

const isCollapse = defineModel('isCollapse')

const handleSelect = (key, keyPath) => {
  console.log(key)
  addTab(key)
}
</script>

<template>
  <el-menu
      default-active="1"
      class="el-menu-vertical-demo h-full"
      :collapse="isCollapse"
      @select="handleSelect"
  >
    <el-menu-item index="1">
      <el-icon><House /></el-icon>
      <template #title>我的主页</template>
    </el-menu-item>
    <el-sub-menu index="2">
      <template #title>
        <el-icon><icon-menu /></el-icon>
        <span>资源管理</span>
      </template>
      <el-menu-item index="2-1">
        <el-icon><Headset /></el-icon>
        歌曲管理
      </el-menu-item>
      <el-menu-item index="2-2">
        <el-icon><Files /></el-icon>
        歌单管理
      </el-menu-item>
      <el-menu-item index="2-3">
        <el-icon><Star /></el-icon>
        歌手管理
      </el-menu-item>
      <el-menu-item index="2-4">
        <el-icon><User /></el-icon>
        用户管理
      </el-menu-item>
    </el-sub-menu>
    <el-menu-item index="3">
      <el-icon><setting /></el-icon>
      <template #title>设置</template>
    </el-menu-item>
  </el-menu>
</template>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
</style>