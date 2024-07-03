<script setup>
import Sidebar from "@/components/Sidebar.vue";
import Header from "@/components/Header.vue";
import MainView from "@/views/MainView.vue";
import {ref} from "vue";

const isCollapse = ref(false)
</script>

<template>
  <div class="common-layout">
    <el-container class="h-screen">
      <el-header class="p-0 border-blue-400 border-b-2">
        <Header />
      </el-header>
      <el-container>
        <el-aside width="auto">
          <Sidebar v-model:isCollapse="isCollapse"/>
        </el-aside>
        <el-main class="p-0">
          <MainView v-model:isCollapse="isCollapse"/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>

</style>