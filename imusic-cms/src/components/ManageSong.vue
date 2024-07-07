<script setup>
import {curEditSongList, deleteSongFromSongList} from "@/js/contentManager.js";
import {ref} from "vue";
import {ElMessageBox} from "element-plus";

const dialogFormVisible = defineModel("visible");

const songData = ref([])

function initForm() {
  songData.value = curEditSongList.songs
}

const indexMethod = (index) => {
  return index + 1
}

function remove(row) {
  deleteSongFromSongList(curEditSongList.id, row.id);
  curEditSongList.songs = curEditSongList.songs.filter(item => item.id !== row.id);
  songData.value = curEditSongList.songs;
}

const open = (row) => {
  ElMessageBox.confirm(
      `确认从 ${curEditSongList.title} 中移除歌曲 ${row.title} 吗？`,
      '消息提示',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(() => {
        remove(row)
      })
}
</script>

<template>
  <el-dialog v-model="dialogFormVisible" title="管理歌曲" width="600" @opened="initForm"
             style="max-height: 600px" class="overflow-y-auto">
    <el-table :data="songData" border max-height="450">
      <el-table-column type="index" fixed :index="indexMethod"/>
      <el-table-column prop="title" fixed label="歌曲名" width="180"/>
      <el-table-column prop="singer" label="歌手" width="180"/>
      <el-table-column label="操作">
        <template #default="{row}">
          <el-button type="danger" plain @click="open(row)">移除歌曲</el-button>
        </template>
      </el-table-column>
    </el-table>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">关闭</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>

</style>