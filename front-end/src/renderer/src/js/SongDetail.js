import instance from '@/js/axios.js'
import { ref } from 'vue'
import { GetDetailLyrics, GetEditLyrics } from '@/js/HandleLyrics.js'
import { MySubscribeUsers } from '@/js/SubscribeUser.js'

//当前歌曲id
export const SongId = ref(0)
//当前歌曲详细信息
export const SongDetail = ref({})
//是否显示歌曲详情
export const SongDetailVisible = ref(false)
//歌词内容
export const LyricContent = ref('')
//歌词列表
export const LyricList = ref([])
//是否显示编辑歌曲界面
export const EditSongVisible = ref(false)
//编辑歌曲界面显示的歌曲信息
export const EditSongDetail = ref({})
//编辑歌曲界面的歌词列表
export const EditLyricList = ref([])
//全屏播放界面的歌词列表
export const FullScreenLyricList = ref([])

//获取到歌曲详情界面的歌曲详情
export const GetSongDetail = () => {
  instance.get('/songs/info/' + SongId.value)
    .then(response => {
      SongDetail.value = response.data.data
      // console.log(SongDetail.value)
      SongDetail.value.upload_date = SongDetail.value.upload_date.split(' ')[0]
      console.log(MySubscribeUsers.value.filter((item) => {
        return item.username === SongDetail.value.uploader
      }).length);
      SongDetail.value['isSubscribed'] = MySubscribeUsers.value.filter((item) => {
        return item.username === SongDetail.value.uploader
      }).length > 0;
      SongDetail.value.introduction = SongDetail.value.introduction === null ? '无简介' : SongDetail.value.introduction
      GetDetailLyrics(SongDetail.value.lyric)
    })
    .catch(error => {
      console.log(error)
    })
}

//获取到编辑歌曲界面的歌曲详情
export const GetEditSongDetail = () => {
  instance.get('/songs/info/' + SongId.value)
    .then(response => {
      EditSongDetail.value = response.data.data
      EditSongDetail.value.upload_date = EditSongDetail.value.upload_date.split(' ')[0]
      EditSongDetail.value.introduction = EditSongDetail.value.introduction === null ? '无简介' : EditSongDetail.value.introduction
      GetEditLyrics(EditSongDetail.value.lyric)
    })
    .catch(error => {
      console.log(error)
    })
}

//展示歌曲详情
export const ShowSongDetail = (id) => {
  SongId.value = id
  SongDetailVisible.value = true
}


//展示编辑歌曲界面
export const ShowEditSong = (id) => {
  console.log(id)
  SongId.value = id
  EditSongVisible.value = true
}


