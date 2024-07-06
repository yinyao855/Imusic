<script setup>
import {reactive, ref} from "vue";
import {createSongList, curEditSongList, editMode, setSongListInfo} from "@/js/contentManager.js";
import {ElMessage, ElMessageBox} from "element-plus";
import {THEME_CHOICES, SCENE_CHOICES, MOOD_CHOICES, STYLE_CHOICES, LANGUAGE_CHOICES} from "@/js/constant.js";
import {useUserStore} from "@/stores/user.js";
const userStore = useUserStore();

const dialogFormVisible = defineModel("visible");
const formLabelWidth = '140px'
const emit = defineEmits(['upInfo'])

const form = reactive({
  title: '',
  introduction: '',
  tag_theme: '',
  tag_scene: '',
  tag_mood: '',
  tag_style: '',
  tag_language: '',
})

const songListCover = ref('')

function initForm() {
  if (editMode) {
    form.title = curEditSongList.title
    form.introduction = curEditSongList.introduction
    form.tag_theme = curEditSongList.tag_theme
    form.tag_scene = curEditSongList.tag_scene
    form.tag_mood = curEditSongList.tag_mood
    form.tag_style = curEditSongList.tag_style
    form.tag_language = curEditSongList.tag_language
    songListCover.value = curEditSongList.cover
  } else {
    form.title = ''
    form.introduction = ''
    form.tag_theme = ''
    form.tag_scene = ''
    form.tag_mood = ''
    form.tag_style = ''
    form.tag_language = ''
    songListCover.value = ''
  }
  coverList.value = []
}

const coverList = ref([])

function handleSongListCover(file) {
  songListCover.value = URL.createObjectURL(file.raw)
}

async function save() {
  const formData = new FormData();
  if (coverList.value.length > 0) {
    formData.append('cover', coverList.value[0].raw);
  }

  formData.append('tag_theme', form.tag_theme);
  formData.append('tag_scene', form.tag_scene);
  formData.append('tag_mood', form.tag_mood);
  formData.append('tag_style', form.tag_style);
  formData.append('tag_language', form.tag_language);
  formData.append('title', form.title);
  formData.append('introduction', form.introduction);

  try {
    await setSongListInfo(curEditSongList.id, formData);
    emit('upInfo');
    dialogFormVisible.value = false;
  } catch (error) {
    console.error('Error saving song info:', error);
  }
}

async function create() {
  const formData = new FormData();
  if (form.title === '') {
    ElMessage.error('请输入歌单名')
    return
  }
  if (coverList.value.length > 0) {
    formData.append('cover', coverList.value[0].raw);
  } else {
    ElMessage.warning('请上传歌单封面')
  }

  formData.append('tag_theme', form.tag_theme);
  formData.append('tag_scene', form.tag_scene);
  formData.append('tag_mood', form.tag_mood);
  formData.append('tag_style', form.tag_style);
  formData.append('tag_language', form.tag_language);
  formData.append('title', form.title);
  formData.append('introduction', form.introduction);
  formData.append('owner', userStore.username);

  try {
    await createSongList(formData);
    emit('upInfo');
    dialogFormVisible.value = false;
  } catch (error) {
    console.error('Error creating song:', error);
  }
}

const open = () => {
  ElMessageBox.confirm(
      editMode === 1 ? '确认修改吗？' : '确认创建吗?',
      '消息提示',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(() => {
        (editMode === 1 ? save : create)();
      })
}
</script>

<template>
  <el-dialog v-model="dialogFormVisible" :title="editMode === 1 ? '编辑歌单信息' : '创建歌单'" width="700" @opened="initForm"
             style="max-height: 600px" class="overflow-y-auto">
    <el-form :model="form">
      <el-form-item label="歌单名" :label-width="formLabelWidth">
        <el-input v-model="form.title"/>
      </el-form-item>
      <el-form-item label="歌单简介" :label-width="formLabelWidth">
        <el-input v-model="form.introduction" type="textarea" autosize/>
      </el-form-item>
      <!-- 歌单标签 -->
      <el-form-item label="主题标签" :label-width="formLabelWidth">
        <el-select v-model="form.tag_theme" placeholder="请选择标签">
          <el-option v-for="item in THEME_CHOICES" :key="item" :value="item"/>
        </el-select>
      </el-form-item>
      <el-form-item label="场景标签" :label-width="formLabelWidth">
        <el-select v-model="form.tag_scene" placeholder="请选择标签">
          <el-option v-for="item in SCENE_CHOICES" :key="item" :value="item"/>
        </el-select>
      </el-form-item>
      <el-form-item label="情感标签" :label-width="formLabelWidth">
        <el-select v-model="form.tag_mood" placeholder="请选择标签">
          <el-option v-for="item in MOOD_CHOICES" :key="item" :value="item"/>
        </el-select>
      </el-form-item>
      <el-form-item label="风格标签" :label-width="formLabelWidth">
        <el-select v-model="form.tag_style" placeholder="请选择标签">
          <el-option v-for="item in STYLE_CHOICES" :key="item" :value="item"/>
        </el-select>
      </el-form-item>
      <el-form-item label="语言标签" :label-width="formLabelWidth">
        <el-select v-model="form.tag_language" placeholder="请选择标签">
          <el-option v-for="item in LANGUAGE_CHOICES" :key="item" :value="item"/>
        </el-select>
      </el-form-item>
      <!-- 歌单封面 -->
      <el-form-item label="歌曲封面" :label-width="formLabelWidth">
        <el-upload
            list-type="text"
            action="none"
            accept="image/jpeg,image/png"
            :limit="1"
            v-model:file-list="coverList"
            :auto-upload="false"
            :on-change="handleSongListCover"
        >
          <template #trigger>
            <el-button type="primary" size="small" plain>上传歌单封面</el-button>
          </template>
          <template #tip>
            <div class="el-upload__tip">
              只能上传jpg/png文件，且不超过2MB
            </div>
          </template>
        </el-upload>
        <el-image v-if="songListCover" :src="songListCover" class="h-32 w-32"/>
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