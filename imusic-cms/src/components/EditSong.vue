<script setup>
import {reactive, ref} from "vue";
import {curEditSong, editMode, setSongInfo} from "@/js/contentManager.js";
import axios from "axios";
import {ElMessageBox} from "element-plus";

const dialogFormVisible = defineModel("visible");
const formLabelWidth = '140px'
const emit = defineEmits(['upInfo'])

const form = reactive({
  title: '',
  singer: '',
  introduction: '',
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
    songCover.value = curEditSong.cover
    songAudio.value = curEditSong.audio
    fetchLyric(curEditSong.lyric)
    lyricName = getLyricName(curEditSong.lyric)
  }
  else{
    form.title = ''
    form.singer = ''
    form.introduction = ''
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
  axios.get(url)
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

  formData.append('title', form.title);
  formData.append('singer', form.singer);
  formData.append('introduction', form.introduction);

  try {
    await setSongInfo(curEditSong.id, formData);
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
  <el-dialog v-model="dialogFormVisible" title="编辑歌曲信息" width="700" @opened="initForm"
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