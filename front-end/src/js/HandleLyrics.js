import axios from 'axios'
import { EditLyricList, FullScreenLyricList, LyricContent, LyricList } from '@/js/SongDetail.js'
import { TimeStringToSecond } from '@/js/MusicPlayer.js'
import { ref } from 'vue'

//详情界面的歌词解析
export const GetDetailLyrics = (url) => {
  axios.get(url)
    .then(response => {
      let lyric = []
      LyricContent.value = response.data
      const TmpLyricList = LyricContent.value.trim().split('\n')
      for (let i = 0; i < TmpLyricList.length; ++i) {
        let timestamp = TmpLyricList[i].split(']')[0].split('[')[1]
        let content = TmpLyricList[i].split(']')[1]
        let TmpDictionary = {}
        TmpDictionary['content'] = content
        TmpDictionary['timestamp'] = TimeStringToSecond(timestamp)
        lyric.push(TmpDictionary)
      }
      LyricList.value = lyric
    })
    .catch(error => {
      console.log(error)
    })
}


//全屏播放界面的歌词解析
export const GetFullScreenLyric = (url) => {
  axios.get(url)
    .then(response => {
      let lyric = []
      LyricContent.value = response.data
      const TmpLyricList = LyricContent.value.trim().split('\n')
      for (let i = 0; i < TmpLyricList.length; ++i) {
        let timestamp = TmpLyricList[i].split(']')[0].split('[')[1]
        let content = TmpLyricList[i].split(']')[1]
        let TmpDictionary = {}
        TmpDictionary['content'] = content
        TmpDictionary['timestamp'] = TimeStringToSecond(timestamp)
        lyric.push(TmpDictionary)
      }
      FullScreenLyricList.value = lyric
    })
    .catch(error => {
      console.log(error)
    })
}


//编辑界面的歌词
export const GetEditLyrics = (url) => {
  axios.get(url)
    .then(response => {
      let lyric = []
      LyricContent.value = response.data
      const TmpLyricList = LyricContent.value.trim().split('\n')
      for (let i = 0; i < TmpLyricList.length; ++i) {
        if (/\d\d/.test(TmpLyricList[i])) {
          let timestamp = TmpLyricList[i].split(']')[0].split('[')[1]
          let content = TmpLyricList[i].split(']')[1]
          let TmpDictionary = {}
          TmpDictionary['content'] = content
          TmpDictionary['timestamp'] = timestamp
          lyric.push(TmpDictionary)
        }
      }
      EditLyricList.value = lyric
      console.log(EditLyricList.value)
    })
    .catch(error => {
      console.log(error)
    })
}

//处理的歌词文件
export const UploadedLyricList = ref([])

//解析歌词文件
export const parseLRCFile = (file) => {
  const reader = new FileReader()
  reader.onload = (event) => {
    const lrcText = event.target.result
    UploadedLyricList.value = parseLRCContent(lrcText)
  }
  reader.readAsText(file)
}

//将字符串解析为歌词列表
const parseLRCContent = (lrcText) => {
  const lines = lrcText.split('\n')
  const parsedLyrics = []
  lines.forEach(line => {
    if (/\d\d/.test(line)) {
      const tmp = line.split(']')[0].split('[')[1]
      const minute=tmp.split(':')[0]+':';
      const second=parseFloat(tmp.split(':')[1]).toFixed(2);
      const timestamp=minute+second.toString();
      const content = line.split(']')[1]
      parsedLyrics.push({ timestamp, content })
    }
  })
  return parsedLyrics
}