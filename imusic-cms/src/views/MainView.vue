<script setup>
import {Expand, Fold} from "@element-plus/icons-vue";
import {removeTab, editableTabs, editableTabsValue} from '@/js/tabManager';

const isCollapse = defineModel('isCollapse');
</script>

<template>
  <div class="w-full h-full flex-col p-4">
    <div>
      <div @click="isCollapse = !isCollapse">
        <el-icon v-if="isCollapse" size="24">
          <Expand/>
        </el-icon>
        <el-icon v-if="!isCollapse" size="24">
          <Fold/>
        </el-icon>
      </div>
    </div>
    <div>
      <el-tabs
          v-model="editableTabsValue"
          type="card"
          closable
          @tab-remove="removeTab"
      >
        <el-tab-pane
            v-for="item in editableTabs"
            :key="item.name"
            :label="item.title"
            :name="item.name"
        >
          <component :is="item.content"></component>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<style scoped>

</style>