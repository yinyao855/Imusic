import instance from '@/js/axios.js'
import { UserStore } from '@/stores/User.js'
import { SongListDetail, SongListVisible } from '@/js/SongList.js'
import { SecondToTime } from '@/js/BeforeEnterHomeView.js'

//获取到喜爱的歌曲
export const GetLikeSongs=()=>{
  instance.get('/like/songs',{
    params:{
      username:UserStore().Username
    }
  })
    .then(response=>{
        SongListDetail.value['songs']=response.data.data;
        for(let i=0;i<SongListDetail.value.songs.length;++i){
            SongListDetail.value.songs[i].duration=SecondToTime(parseInt(SongListDetail.value.songs[i].duration));
        }
        SongListDetail.value['title']='喜爱的歌曲';
        SongListDetail.value['create_date']=UserStore().Registration_date;
        SongListDetail.value['introduction']='无简介';
        SongListDetail.value['cover']='/LikeSongs.png';
        SongListDetail.value['owner']=UserStore().Username;
        //标志为喜爱的歌曲模式
        SongListDetail.value['mode']=0;
        SongListVisible.value=true;
    })
    .catch(error=>{
      console.log(error);
    })
}