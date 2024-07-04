<script setup>
import {onMounted, reactive, ref, watch} from "vue";
import instance from "@/js/axiosConfig.js";
import {Search} from "@element-plus/icons-vue";
import EditUser from "@/components/EditUser.vue";
import {getUserInfo} from "@/js/contentManager.js";

const userList = ref([])
let rowData = []

const indexMethod = (index) => {
  return index + 1
}

function getUserList() {
  instance.get('/users/alldata')
      .then(res => {
        userList.value = res.data.data
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
    value: 'username',
    label: '用户名'
  },
  {
    value: 'email',
    label: '邮箱'
  },
  {
    value: 'registration_date',
    label: '注册日期'
  }
]

// 搜索
const search = () => {
  if (choice.value === '' || input.value === '') {
    userList.value = rowData
    state.total = userList.value.length
  } else {
    userList.value = userList.value.filter(item => {
      return item[choice.value].includes(input.value)
    })
    state.total = userList.value.length
  }
}

// 编辑用户
const editVisible = ref(false)
function editUser(row) {
  getUserInfo(row.username, row.role)
  editVisible.value = true
}

const tableData = () => {
  return userList.value.filter(
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

// 创建日期格式化
const dateFormater = (row, column, cellValue) => {
  if (cellValue) {
    return new Date(cellValue).toLocaleDateString()
  } else {
    return '--'
  }
}

onMounted(() => {
  getUserList()
})

// 如果input为空，显示所有数据
watch(input, (val) => {
  if (val === '') {
    userList.value = rowData
    state.total = userList.value.length
  }
})
</script>

<template>
  <div class="w-full h-full">
    <!-- 编辑用户 -->
    <EditUser v-model:visible="editVisible"/>
    <div class="w-full flex">
      <h1 class="m-auto text-2xl font-black">用户资源管理</h1>
    </div>
    <div class="h-8 mb-2 flex mt-3">
      <el-text class="mr-2" size="large">筛选条件</el-text>
      <el-select v-model="choice" placeholder="Select" style="width: 120px" class="mr-3">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"/>
      </el-select>
      <el-input v-model="input" style="width: 240px" class="mr-3" clearable
                placeholder="Type something" :prefix-icon="Search" @keydown.enter="search"/>
      <el-button type="success" plain @click="search">搜索</el-button>
    </div>
    <div>
      <el-table :data="tableData()" border max-height="450">
        <el-table-column type="index" fixed :index="indexMethod"/>
        <el-table-column prop="username" fixed label="用户名" width="180"/>
        <el-table-column prop="email" label="邮箱" show-overflow-tooltip width="180"/>
        <el-table-column label="用户头像" width="150">
          <template #default="scope">
            <el-image v-if="scope.row.avatar" :src="scope.row.avatar" :preview-src-list="[scope.row.avatar]"
                      preview-teleported class="w-16 h-16 m-auto">
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="bio" label="个人介绍" show-overflow-tooltip :formatter="formatter" width="180"/>
        <el-table-column prop="follower_count" label="粉丝" sortable width="180"/>
        <el-table-column prop="following_count" label="关注用户数" sortable width="180"/>
        <el-table-column prop="registration_date" label="注册日期" :formatter="dateFormater" sortable width="180"/>
        <el-table-column fixed="right" label="用户身份" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.role === 'admin'" type="success">管理员</el-tag>
            <el-tag v-else type="info">普通用户</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="180">
          <template #default="scope">
            <el-button type="primary" link @click="editUser(scope.row)">编辑</el-button>
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