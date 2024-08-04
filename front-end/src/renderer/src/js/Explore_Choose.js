import { ref } from 'vue'
import instance from '@/js/axios.js'
import { SecondToTime } from '@/js/BeforeEnterHomeView.js'

//语言的选项
export const LanguageOptions = [
  '默认',
  '英语',
  '日语',
  '粤语',
  '国语',
  '韩语'
]

//主题的选项
export const ThemeOptions = [
  '默认',
  '背景音乐',
  '经典老歌',
  'KTV金曲',
  '游戏配乐',
  '电影配乐'
]

//场景的选项
export const SceneOptions = [
  '默认',
  '咖啡馆',
  '运动',
  '睡前',
  '旅行',
  '派对'
]


//心情的选项
export const MoodOptions = [
  '默认',
  '伤感',
  '安静',
  '思念',
  '宣泄',
  '开心'
]


//风格的选项
export const StyleOptions = [
  '默认',
  '摇滚',
  '民谣',
  '轻音乐',
  '电音',
  '流行'
]


//探索界面展示的歌曲
export const ExploreSongs = ref([])
//探索界面展示的歌单
export const ExploreSongLists = ref([])


//获取在当前条件下的歌曲
export const GetTagSongs = (language, theme, scene, mood, style) => {
  let web=GetWeb('/search/songs?',language,theme,scene,mood,style,'/songs/alldata');
  instance.get(web)
    .then(response=>{
      ExploreSongs.value = response.data.data;
      let length = ExploreSongs.value.length;
      for (let i = 0; i < length; ++i) {
        ExploreSongs.value[i].duration = SecondToTime(parseInt(ExploreSongs.value[i].duration));
      }
    })
    .catch(error=>{
      console.log(error);
    })
}

//获取到当前的web
const GetWeb=(web,language,theme,scene,mood,style,delault)=>{
  let flag = 0;
  if (language !== '默认') {
    if (flag===0) {
      web = web + 'tag_language=' + language;
    } else {
      web = web + '&tag_language=' + language;
    }
    flag = 1;
  }
  if(theme !== '默认'){
    if (flag === 0) {
      web = web + 'tag_theme=' + theme;
    } else {
      web = web + '&tag_theme=' + theme;
    }
    flag = 1;
  }
  if(scene !== '默认'){
    if (flag === 0) {
      web = web + 'tag_scene=' + scene;
    } else {
      web = web + '&tag_scene=' + scene;
    }
    flag = 1;
  }
  if(mood !== '默认'){
    if (flag === 0) {
      web = web + 'tag_mood=' + mood;
    } else {
      web = web + '&tag_mood=' + mood;
    }
    flag = 1;
  }
  if(style !== '默认'){
    if (flag === 0) {
      web = web + 'tag_style=' + style;
    } else {
      web = web + '&tag_style=' + style;
    }
  }
  if(flag===0){
    web=delault;
  }
  return web;
}



//获取在当前条件下的歌曲
export const GetTagSongLists = (language, theme, scene, mood, style) => {
  let web=GetWeb('/search/songlists?',language,theme,scene,mood,style,'/songlists/alldata');
  instance.get(web)
    .then(response=>{
      ExploreSongLists.value = response.data.data;
      console.log(ExploreSongLists.value);
    })
    .catch(error=>{
      console.log(error);
    })
}


