<script setup>
import {curEditSong, addSongToSongList} from "@/js/contentManager.js";
import {ref} from "vue";
import {ElMessageBox} from "element-plus";
import instance from "@/js/axiosConfig.js";

const dialogFormVisible = defineModel("visible");

const songData = ref([])
const songListData = ref([])

function initForm() {
  songData.value = curEditSong
  getSongList()
}

const indexMethod = (index) => {
  return index + 1
}

function getSongList() {
  instance.get('/songlists/alldata')
      .then(res => {
        songListData.value = res.data.data
      })
      .catch(err => {
        console.log(err)
      })
}

function add(row) {
  addSongToSongList(row.id, curEditSong.id)
}

const open = (row) => {
  ElMessageBox.confirm(
      `确认将歌曲 ${curEditSong.title} 添加到歌单 ${row.title} 吗？`,
      '消息提示',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(() => {
        add(row)
        dialogFormVisible.value = false
      })
}
</script>

<template>
  <el-dialog v-model="dialogFormVisible" title="添到歌单" width="500" @opened="initForm"
             style="max-height: 600px" class="overflow-y-auto">
    <el-table :data="songListData" border max-height="450">
      <el-table-column type="index" fixed :index="indexMethod"/>
      <el-table-column prop="title" fixed label="歌单名" width="180"/>
      <el-table-column label="操作">
        <template #default="{row}">
          <el-button type="success" plain @click="open(row)">添加到歌单</el-button>
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