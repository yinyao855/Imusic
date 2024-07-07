<script setup>
import {onMounted, reactive, ref, watch} from "vue";
import instance from "@/js/axiosConfig.js";
import {Search} from "@element-plus/icons-vue";
import EditSongList from "@/components/EditSongList.vue";
import {getSongListInfo, setEditMode} from "@/js/contentManager.js";
import {ElMessage, ElMessageBox} from "element-plus";
import ManageSong from "@/components/ManageSong.vue";

const musicList = ref([])
let rowData = []

const indexMethod = (index) => {
  return index + 1
}

function getSongList() {
  instance.get('/songlists/alldata')
      .then(res => {
        musicList.value = res.data.data
        state.total = res.data.data.length
        rowData = res.data.data
      })
      .catch(err => {
        console.log(err)
      })
}

const state = reactive({
  page: 1,
  limit: 10,
  total: 0
})

//改变页码
const handleCurrentChange = (e) => {
  state.page = e;
};
//改变页数限制
const handleSizeChange = (e) => {
  state.limit = e;
};

// 表格搜索
const choice = ref('')
const input = ref('')

const options = [
  {
    value: 'title',
    label: '歌单名'
  },
  {
    value: 'owner',
    label: '创建者'
  },
  {
    value: 'create_date',
    label: '上传日期'
  }
]

// 搜索
const search = () => {
  if (choice.value === '' || input.value === '') {
    musicList.value = rowData
    state.total = musicList.value.length
  } else {
    musicList.value = musicList.value.filter(item => {
      return item[choice.value].includes(input.value)
    })
    state.total = musicList.value.length
  }
}

// 编辑歌单
const editVisible = ref(false)
const manageVisible = ref(false)

function editSongList(row) {
  getSongListInfo(row.id)
  setEditMode(1)
  editVisible.value = true
}

function newSongList() {
  setEditMode(0)
  editVisible.value = true
}

// 删除歌单
const open = (row) => {
  ElMessageBox.confirm(
      '确认删除该歌单吗？',
      '消息提示',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(() => {
        deleteSongList(row)
      })
}

function deleteSongList(row) {
  instance.delete(`/songlists/delete/${row.id}`)
      .then(res => {
        if (res.data.success === true) {
          ElMessage.success('歌单删除成功')
        } else {
          ElMessage.success('歌单删除失败')
        }
        getSongList()
      })
      .catch(err => {
        console.log(err)
      })
}

// 管理歌曲
function manageSongs(row) {
  getSongListInfo(row.id)
  manageVisible.value = true
}

const tableData = () => {
  return musicList.value.filter(
      (item, index) =>
          index < state.page * state.limit &&
          index >= state.limit * (state.page - 1)
  );
};

// 创建日期格式化
const dateFormater = (row, column, cellValue) => {
  if (cellValue) {
    return new Date(cellValue).toLocaleDateString()
  } else {
    return '--'
  }
}

onMounted(() => {
  getSongList()
})

// 如果input为空，显示所有数据
watch(input, (val) => {
  if (val === '') {
    musicList.value = rowData
    state.total = musicList.value.length
  }
})
</script>

<template>
  <div class="w-full h-full">
    <!-- 编辑歌单 -->
    <EditSongList v-model:visible="editVisible" @upInfo="getSongList"/>
    <!-- 管理歌曲 -->
    <ManageSong v-model:visible="manageVisible"/>
    <div class="w-full flex">
      <h1 class="m-auto text-2xl font-black">歌单资源管理</h1>
    </div>
    <div class="h-8 mb-2 flex mt-3">
      <el-text class="mr-2" size="large">筛选条件</el-text>
      <el-select v-model="choice" placeholder="Select" style="width: 120px" class="mr-3">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"/>
      </el-select>
      <el-input v-model="input" style="width: 240px" class="mr-3" clearable
                placeholder="Type something" :prefix-icon="Search" @keydown.enter="search"/>
      <el-button type="success" plain @click="search">搜索</el-button>
      <el-button type="primary" plain @click="newSongList">创建歌单</el-button>
    </div>
    <div>
      <el-table :data="tableData()" border max-height="450">
        <el-table-column type="index" fixed :index="indexMethod"/>
        <el-table-column prop="title" fixed label="歌单名" width="180"/>
        <el-table-column label="封面图" width="150">
          <template #default="scope">
            <el-image :src="scope.row.cover" :preview-src-list="[scope.row.cover]"
                      preview-teleported class="w-16 h-16 m-auto"/>
          </template>
        </el-table-column>
        <el-table-column prop="like" label="收藏人数" sortable width="180"/>
        <el-table-column prop="owner" label="创建者" width="180"/>
        <el-table-column prop="create_date" label="创建日期" :formatter="dateFormater" sortable width="180"/>
        <el-table-column label="操作" fixed="right" width="180">
          <template #default="scope">
            <el-button type="primary" link @click="editSongList(scope.row)">编辑</el-button>
            <el-button type="success" link @click="manageSongs(scope.row)">管理歌曲</el-button>
            <el-button type="danger" link @click="open(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="mt-5">
      <el-pagination
          background
          layout="prev, pager, next , total, sizes"
          :total="state.total"
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
          v-model:current-page="state.page"
          v-model:page-size="state.limit"
      />
    </div>
  </div>
</template>

<style scoped>

</style>