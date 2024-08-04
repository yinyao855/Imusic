import axios from 'axios'
import { EditLyricList, FullScreenLyricList, LyricContent, LyricList } from '@/js/SongDetail.js'
import { TimeStringToSecond } from '@/js/MusicPlayer.js'
import { ref } from 'vue'

//详情界面的歌词解析
export const GetDetailLyrics = (url) => {
  LyricList.value=[];
  console.log(url);
  axios.get(url)
    .then(response => {
      LyricContent.value = response.data
      const TmpLyricList = LyricContent.value.trim().split('\n')
      for (let i = 0; i < TmpLyricList.length; ++i) {
        let timestamp = TmpLyricList[i].split(']')[0].split('[')[1]
        let content = TmpLyricList[i].split(']')[1]
        let TmpDictionary = {}
        if(timestamp===undefined){
          continue;
        }
        TmpDictionary['content'] = content
        TmpDictionary['timestamp'] = TimeStringToSecond(timestamp)
        LyricList.value.push(TmpDictionary)
      }
      console.log(LyricList.value);
    })
    .catch(error => {
      console.log(error)
    })
}


//全屏播放界面的歌词解析
export const GetFullScreenLyric = (url) => {
  FullScreenLyricList.value=[];
  if(url===null){
    return;
  }
  axios.get(url)
    .then(response => {
      LyricContent.value = response.data
      const TmpLyricList = LyricContent.value.split('\n')
      for (let i = 0; i < TmpLyricList.length; ++i) {
        let timestamp = TmpLyricList[i].split(']')[0].split('[')[1]
        let content = TmpLyricList[i].split(']')[1]
        let TmpDictionary = {}
        TmpDictionary['content'] = content
        if(timestamp===undefined){
          continue;
        }
        TmpDictionary['timestamp'] = TimeStringToSecond(timestamp)
        FullScreenLyricList.value.push(TmpDictionary)
      }
    })
    .catch(error => {
      console.log(error)
    })
}


//编辑界面的歌词
export const GetEditLyrics = (url) => {
  EditLyricList.value=[]
  axios.get(url)
    .then(response => {
      LyricContent.value = response.data
      const TmpLyricList = LyricContent.value.trim().split('\n')
      for (let i = 0; i < TmpLyricList.length; ++i) {
        if (/\d\d/.test(TmpLyricList[i])) {
          let timestamp = TmpLyricList[i].split(']')[0].split('[')[1]
          let content = TmpLyricList[i].split(']')[1]
          let TmpDictionary = {}
          TmpDictionary['content'] = content
          TmpDictionary['timestamp'] = timestamp
          EditLyricList.value.push(TmpDictionary)
        }
      }
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


//将歌词列表转成文件
export const GenerateLRCFile = (lyric,title) => {
  let content = ''
  lyric.forEach(line => {
    content += `[${line.timestamp}] ${line.content}\n`
  })
  const lrcContent = ref('')
  lrcContent.value = content

  const blob = new Blob([lrcContent.value], { type: 'text/plain' })
  return new File([blob], title + '.lrc', { type: 'text/plain' })
}


//下载歌词文件
export const DownloadGeneratedFile = (file) => {
  if (file) {
    const url = URL.createObjectURL(file);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.name;
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }
};