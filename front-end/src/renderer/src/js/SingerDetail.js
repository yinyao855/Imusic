import instance from '@/js/axios.js'
import { ref } from 'vue'
import { SecondToTime } from '@/js/BeforeEnterHomeView.js'

//歌手详情
export const SingerDetail = ref({})
//是否展示歌手详情
export const SingerDetailVisible=ref(false);

//获取歌手详情
export const GetSingerDetail = (id) => {
  instance.get('/singer/getsongs/' + id)
    .then(response => {
      SingerDetail.value = response.data.data
      for (let i = 0; i < SingerDetail.value.songs.length; ++i) {
        SingerDetail.value.songs[i].duration = SecondToTime(parseInt(SingerDetail.value.songs[i].duration))
      }
      SingerDetailVisible.value=true;
      console.log(SingerDetail.value)
    })
    .catch(error => {
      console.log(error.response.data)
    })
}