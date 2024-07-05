<script setup>
import {reactive, ref} from "vue";
import {curEditUer, editMode, setUserInfo, changeUserRole} from "@/js/contentManager.js";
import {ElMessageBox} from "element-plus";

const dialogFormVisible = defineModel("visible");
const formLabelWidth = '140px'
const emit = defineEmits(['upInfo'])

const form = reactive({
  email: '',
  bio: '',
  role: '',
})

const rules = {
  email: [
    {required: true, message: '请输入用户邮箱', trigger: 'blur'},
    {type: 'email', message: '邮箱格式不正确', trigger: 'blur'}
  ],
  bio: [
    {required: true, message: '请输入用户简介', trigger: 'blur'}
  ]
}

const userAvatar = ref('')

function initForm() {
  if (editMode) {
    form.email = curEditUer.email
    form.bio = curEditUer.bio
    form.role = curEditUer.role
    userAvatar.value = curEditUer.avatar
  }
  fileList.value = []
}

const fileList = ref([])

function handleAvatar(file) {
  userAvatar.value = URL.createObjectURL(file.raw)
}

async function save() {
  const formData = new FormData();
  // console.log(fileList.value)
  if (fileList.value.length > 0) {
    formData.append('avatar', fileList.value[0].raw);
  }
  formData.append('email', form.email);
  formData.append('bio', form.bio);

  try {
    await setUserInfo(curEditUer.username, formData);
    if (form.role !== curEditUer.role) {
      await changeUserRole(curEditUer.username, form.role);
    }
    emit('upInfo');
    dialogFormVisible.value = false;
  } catch (error) {
    console.error('Error saving user info:', error);
  }
}

const open = () => {
  ElMessageBox.confirm(
      '确认修改吗？',
      '消息提示',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(() => {
        save()
      })
}
</script>

<template>
  <el-dialog v-model="dialogFormVisible" title="编辑用户信息" width="500" @opened="initForm">
    <el-form :model="form" :rules="rules">
      <el-form-item label="用户邮箱" :label-width="formLabelWidth">
        <el-input v-model="form.email"/>
      </el-form-item>
      <el-form-item label="用户简介" :label-width="formLabelWidth">
        <el-input v-model="form.bio" type="textarea" autosize/>
      </el-form-item>
      <!-- 用户头像 -->
      <el-form-item label="用户头像" :label-width="formLabelWidth">
        <el-upload
            list-type="text"
            action="none"
            accept="image/jpeg,image/png"
            :limit="1"
            v-model:file-list="fileList"
            :auto-upload="false"
            :on-change="handleAvatar"
        >
          <template #trigger>
            <el-button type="primary" size="small">上传头像</el-button>
          </template>
          <template #tip>
            <div class="el-upload__tip">
              只能上传jpg/png文件，且不超过2MB
            </div>
          </template>
        </el-upload>
        <el-image v-if="userAvatar" :src="userAvatar" class="h-32 w-32"/>
      </el-form-item>
      <el-form-item label="用户身份" :label-width="formLabelWidth">
        <el-select v-model="form.role" placeholder="选择身份">
          <el-option label="管理员" value="admin"/>
          <el-option label="普通用户" value="user"/>
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="open">确认</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>

</style>