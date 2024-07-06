<script setup>
import {reactive, ref} from "vue";
import {createSong, curEditSong, editMode, setSongInfo} from "@/js/contentManager.js";
import axios from "axios";
import {ElMessage, ElMessageBox} from "element-plus";
import {THEME_CHOICES, SCENE_CHOICES, MOOD_CHOICES, STYLE_CHOICES, LANGUAGE_CHOICES} from "@/js/constant.js";
import {useUserStore} from "@/stores/user.js";
const userStore = useUserStore();

const dialogFormVisible = defineModel("visible");
const formLabelWidth = '140px'
const emit = defineEmits(['upInfo'])

const form = reactive({
  title: '',
  singer: '',
  introduction: '',
  tag_theme: '',
  tag_scene: '',
  tag_mood: '',
  tag_style: '',
  tag_language: '',
})

const songCover = ref('')
const songAudio = ref('')
const songLyric = ref('')
let lyricName = ''
let rawLyric = ''

function initForm() {
  if (editMode) {
    form.title = curEditSong.title
    form.singer = curEditSong.singer
    form.introduction = curEditSong.introduction
    form.tag_theme = curEditSong.tag_theme
    form.tag_scene = curEditSong.tag_scene
    form.tag_mood = curEditSong.tag_mood
    form.tag_style = curEditSong.tag_style
    form.tag_language = curEditSong.tag_language
    songCover.value = curEditSong.cover
    songAudio.value = curEditSong.audio
    fetchLyric(curEditSong.lyric)
    lyricName = getLyricName(curEditSong.lyric)
  } else {
    form.title = ''
    form.singer = ''
    form.introduction = ''
    form.tag_theme = ''
    form.tag_scene = ''
    form.tag_mood = ''
    form.tag_style = ''
    form.tag_language = ''
    songCover.value = ''
    songAudio.value = ''
    songLyric.value = ''
    lyricName = ''
    rawLyric = ''
  }
  coverList.value = []
  audioList.value = []
  lyricList.value = []
}

function fetchLyric(url) {
  axios.get(url, {
    params: {
      timestamp: Date.now() // 添加当前时间戳
    }
  })
      .then(res => {
        songLyric.value = res.data
        rawLyric = res.data
      })
      .catch(err => {
        songLyric.value = ''
        rawLyric = ''
        console.log(err)
      })
}

function getLyricName(url) {
  if (!url) {
    return ''
  }
  return url.split('/').pop()
}

const coverList = ref([])
const audioList = ref([])
const lyricList = ref([])

function handleSongCover(file) {
  songCover.value = URL.createObjectURL(file.raw)
}

function handleSongAudio(file) {
  songAudio.value = URL.createObjectURL(file.raw)
}

function handleSongLyric(file) {
  fetchLyric(URL.createObjectURL(file.raw))
  lyricName = file.raw.name
}

async function save() {
  const formData = new FormData();
  if (coverList.value.length > 0) {
    formData.append('cover', coverList.value[0].raw);
  }
  if (audioList.value.length > 0) {
    formData.append('audio', audioList.value[0].raw);
  }
  if (lyricList.value.length > 0 || songLyric.value !== rawLyric) {
    // 添加歌词，需将歌词内容写入文件
    const file = new Blob([songLyric.value], {type: 'text/plain'});
    formData.append('lyric', file, lyricName);
  }

  formData.append('tag_theme', form.tag_theme);
  formData.append('tag_scene', form.tag_scene);
  formData.append('tag_mood', form.tag_mood);
  formData.append('tag_style', form.tag_style);
  formData.append('tag_language', form.tag_language);
  formData.append('title', form.title);
  formData.append('singer', form.singer);
  formData.append('introduction', form.introduction);

  try {
    await setSongInfo(curEditSong.id, formData);
    emit('upInfo');
    dialogFormVisible.value = false;
  } catch (error) {
    console.error('Error saving song info:', error);
  }
}

async function create() {
  const formData = new FormData();
  if (form.title === '') {
    ElMessage.error('请输入歌曲名')
    return
  }
  if (form.singer === '') {
    ElMessage.error('请输入歌手名')
    return
  }
  if (coverList.value.length > 0) {
    formData.append('cover', coverList.value[0].raw);
  } else {
    ElMessage.warning('请上传歌曲封面')
  }
  if (audioList.value.length > 0) {
    formData.append('audio', audioList.value[0].raw);
  } else {
    ElMessage.warning('请上传歌曲音频')
  }
  if (lyricList.value.length > 0) {
    const file = new Blob([songLyric.value], {type: 'text/plain'});
    formData.append('lyric', file, lyricName);
  }

  formData.append('tag_theme', form.tag_theme);
  formData.append('tag_scene', form.tag_scene);
  formData.append('tag_mood', form.tag_mood);
  formData.append('tag_style', form.tag_style);
  formData.append('tag_language', form.tag_language);
  formData.append('title', form.title);
  formData.append('singer', form.singer);
  formData.append('introduction', form.introduction);
  formData.append('uploader', userStore.username);

  try {
    await createSong(formData);
    emit('upInfo');
    dialogFormVisible.value = false;
  } catch (error) {
    console.error('Error creating song:', error);
  }
}

const open = () => {
  ElMessageBox.confirm(
      editMode === 1 ? '确认修改吗？' : '确认上传吗?',
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
  <el-dialog v-model="dialogFormVisible" :title="editMode === 1 ? '编辑歌曲信息' : '上传歌曲'" width="700" @opened="initForm"
             style="max-height: 600px" class="overflow-y-auto">
    <el-form :model="form">
      <el-form-item label="歌曲名" :label-width="formLabelWidth">
        <el-input v-model="form.title"/>
      </el-form-item>
      <el-form-item label="歌手" :label-width="formLabelWidth">
        <el-input v-model="form.singer"/>
      </el-form-item>
      <el-form-item label="歌曲简介" :label-width="formLabelWidth">
        <el-input v-model="form.introduction" type="textarea" autosize/>
      </el-form-item>
      <!-- 歌曲标签 -->
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
      <!-- 歌曲封面 -->
      <el-form-item label="歌曲封面" :label-width="formLabelWidth">
        <el-upload
            list-type="text"
            action="none"
            accept="image/jpeg,image/png"
            :limit="1"
            v-model:file-list="coverList"
            :auto-upload="false"
            :on-change="handleSongCover"
        >
          <template #trigger>
            <el-button type="primary" size="small" plain>上传歌曲封面</el-button>
          </template>
          <template #tip>
            <div class="el-upload__tip">
              只能上传jpg/png文件，且不超过2MB
            </div>
          </template>
        </el-upload>
        <el-image v-if="songCover" :src="songCover" class="h-32 w-32"/>
      </el-form-item>
      <!-- 歌曲音频 -->
      <el-form-item label="歌曲音频" :label-width="formLabelWidth">
        <el-upload
            list-type="text"
            action="none"
            accept="audio/mp3"
            :limit="1"
            v-model:file-list="audioList"
            :auto-upload="false"
            :on-change="handleSongAudio"
        >
          <template #trigger>
            <el-button type="primary" size="small" plain>上传歌曲音频</el-button>
          </template>
          <template #tip>
            <div class="el-upload__tip">
              只能上传mp3文件，且不超过10MB
            </div>
          </template>
        </el-upload>
        <audio v-if="songAudio" :src="songAudio" controls class="w-full"/>
      </el-form-item>
      <!-- 歌词 -->
      <el-form-item label="歌词" :label-width="formLabelWidth">
        <el-upload
            list-type="text"
            action="none"
            accept=".lrc"
            :limit="1"
            v-model:file-list="lyricList"
            :auto-upload="false"
            :on-change="handleSongLyric"
        >
          <template #trigger>
            <el-button type="primary" size="small" plain>上传歌词</el-button>
          </template>
          <template #tip>
            <div class="el-upload__tip">
              只能上传lrc文件，且不超过1MB
            </div>
          </template>
        </el-upload>
        <el-input v-if="songLyric" v-model="songLyric" type="textarea" autosize/>
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