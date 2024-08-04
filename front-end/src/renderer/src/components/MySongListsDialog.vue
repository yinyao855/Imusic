<!--处理添加到歌单的对话框-->
<template>
  <el-dialog
    v-model="AddSongToMySongListVisible"
    :title="'我的歌单'"
    width="880"
    :before-close="handleClose"
  >
    <span></span>
    <template #footer>
      <div class="flex flex-wrap">
        <div v-for="(SongList,index) in MySongLists" :key="index" class="mx-2 my-2" @click="AddSongToMySongList(SongList.id,CurrentSongIdNeededToAdd)">
          <div>
            <el-card style="width: 200px" class="hover:bg-gray-200">
              <img :src="SongList.cover" alt="封面" class="m-auto">
              <template #footer>
                <div class="flex">
                  <el-popover
                    placement="top"
                    trigger="hover"
                    :content="SongList.title"
                    class="text-center"
                  >
                    <template #reference>
                      <div class="w-full flex">
                        <div class="mx-auto truncate w-40 text-center">{{ SongList.title }}</div>
                      </div>
                    </template>
                  </el-popover>
                </div>
              </template>
            </el-card>
          </div>
        </div>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {
  AddSongToMySongList,
  AddSongToMySongListVisible,
  CurrentSongIdNeededToAdd,
  MySongLists
} from '@/js/MySongList.js'
import { ElMessageBox } from 'element-plus'

const handleClose = () => {
  ElMessageBox.confirm(
    '是否要关闭窗口',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    AddSongToMySongListVisible.value = false;
    console.log('确认')
  }).catch(() => {
    console.log('取消')
  })
}
</script>

