<script setup>
import {reactive, ref} from "vue";
import {ElMessage} from "element-plus";
import {curEditUer} from "@/js/contentManager.js";
import {Plus} from "@element-plus/icons-vue";

const dialogFormVisible = defineModel("visible");
const formLabelWidth = '140px'

const form = reactive({
  email: '',
  bio: '',
  role: '',
})

const userAvatar = ref('')

function tempSave() {
  console.log('tempSave')
  ElMessage.success('暂存成功')
}

function initForm() {
  console.log('initForm')
  // console.log(curEditUer.avatar)
  form.email = curEditUer.email
  form.bio = curEditUer.bio
  form.role = curEditUer.role
  userAvatar.value = curEditUer.avatar
}

function handleAvatarSuccess(res, file) {
  console.log(res)
  userAvatar.value = URL.createObjectURL(file.raw)
}

function beforeAvatarUpload(file) {
  const isJPG = file.type === 'image/jpeg'
  const isPNG = file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG && !isPNG) {
    ElMessage.error('上传头像图片只能是 JPG 格式!')
  }
  if (!isLt2M) {
    ElMessage.error('上传头像图片大小不能超过 2MB!')
  }
  return (isJPG || isPNG) && isLt2M
}

function handlePictureCardPreview(file) {
  console.log(file)
}

function handleRemove(file) {
  console.log(file)
}

function save() {
  console.log('save')
}

</script>

<template>
  <el-dialog v-model="dialogFormVisible" title="编辑用户信息" width="500" @opened="initForm">
    <el-form :model="form">
      <el-form-item label="用户邮箱" :label-width="formLabelWidth">
        <el-input v-model="form.email"/>
      </el-form-item>
      <el-form-item label="用户简介" :label-width="formLabelWidth">
        <el-input v-model="form.bio" type="textarea" autosize/>
      </el-form-item>
      <!-- 用户头像 -->
      <el-form-item label="用户头像" :label-width="formLabelWidth">
        <el-upload
            class="avatar-uploader"
            list-type="picture-card"
            action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
        >
          <el-image v-if="userAvatar" :src="userAvatar" class="h-32 w-32" alt="用户头像"/>
          <el-icon v-else><Plus /></el-icon>
        </el-upload>
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
        <el-button @click="tempSave">暂存</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>

</style>