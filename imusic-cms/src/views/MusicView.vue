<script setup>
import {onMounted, reactive, ref, watch} from "vue";
import instance from "@/js/axiosConfig.js";
import {Search} from "@element-plus/icons-vue";
import {getSongInfo, setEditMode} from "@/js/contentManager.js";
import EditSong from "@/components/EditSong.vue";

const musicList = ref([])
let rowData = []

const indexMethod = (index) => {
  return index + 1
}

function getMusic() {
  // console.log('getMusic')
  instance.get('/songs/alldata')
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
    label: '歌曲名'
  },
  {
    value: 'singer',
    label: '歌手'
  },
  {
    value: 'uploader',
    label: '上传者'
  },
  {
    value: 'upload_date',
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

// 编辑歌曲
const editVisible = ref(false)
function editSong(row) {
  getSongInfo(row.id)
  setEditMode(1)
  editVisible.value = true
}

function newSong() {
  setEditMode(0)
  editVisible.value = true
}

const tableData = () => {
  return musicList.value.filter(
      (item, index) =>
          index < state.page * state.limit &&
          index >= state.limit * (state.page - 1)
  );
};

const formatter = (row, column, cellValue) => {
  if(cellValue && cellValue !== "null"){ //不包含值为 0 的情况 另做判断
    return cellValue
  }else if(cellValue === 0){ //cellValue会自动将0值过滤出来不展示 单独做判断
    return 0
  }else{
    return '--' //没有值时展示 --
  }
}

// 上传日期格式化
const dateFormater = (row, column, cellValue) => {
  if (cellValue) {
    return new Date(cellValue).toLocaleDateString()
  } else {
    return '--'
  }
}

// 时长格式化
const durationFormater = (row, column, cellValue) => {
  if (cellValue) {
    const minute = Math.floor(cellValue / 60)
    const second = Math.floor(cellValue % 60)
    return `${minute}:${second}`
  } else {
    return '--'
  }
}

onMounted(() => {
  getMusic()
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
    <!-- 编辑歌曲 -->
    <EditSong v-model:visible="editVisible" @upInfo="getMusic"/>
    <div class="w-full flex">
      <h1 class="m-auto text-2xl font-black">音乐资源管理</h1>
    </div>
    <div class="h-8 mb-2 flex mt-3">
      <el-text class="mr-2" size="large">筛选条件</el-text>
      <el-select v-model="choice" placeholder="Select" style="width: 120px" class="mr-3">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"/>
      </el-select>
      <el-input v-model="input" style="width: 240px" class="mr-3" clearable
                placeholder="Type something" :prefix-icon="Search" @keydown.enter="search"/>
      <el-button type="success" plain @click="search">搜索</el-button>
      <el-button type="primary" plain @click="newSong">上传歌曲</el-button>
    </div>
    <div>
      <el-table :data="tableData()" border style="width: 100%" max-height="450">
        <el-table-column type="index" fixed :index="indexMethod"/>
        <el-table-column prop="title" fixed label="歌曲名" width="180"/>
        <el-table-column prop="singer" label="歌手" width="180"/>
        <el-table-column prop="introduction" label="介绍" show-overflow-tooltip :formatter="formatter" width="180"/>
        <el-table-column prop="duration" label="时长" :formatter="durationFormater" width="180"/>
        <el-table-column prop="like" label="喜欢人数" sortable width="180"/>
        <el-table-column prop="uploader" label="上传者" width="180"/>
        <el-table-column prop="upload_date" label="上传日期" :formatter="dateFormater" sortable width="180"/>
        <el-table-column label="操作" fixed="right" width="180">
          <template #default="scope">
            <el-button type="primary" link @click="editSong(scope.row)">编辑</el-button>
            <el-button type="danger" link>删除</el-button>
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