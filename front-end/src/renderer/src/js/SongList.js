import { ref } from 'vue';
import instance from '@/js/axios.js'
import { UserStore } from '@/stores/User.js'
import { SecondToTime } from '@/js/BeforeEnterHomeView.js'
import { MySubscribeUsers } from '@/js/SubscribeUser.js'
import { SongDetail } from '@/js/SongDetail.js'

//是否展示SongList组件
export const SongListVisible=ref(false);
//当前SongList编号
export const SongListId=ref(0);
//当前SongList内容
export const SongListDetail=ref({});

//获取到当前SongList内容
export function GetSongListDetail(id){
    SongListId.value=id;
    instance.get('/songlists/info/'+id,{
      params:{
        username:UserStore().Username
      }
    })
      .then(response=>{
        SongListDetail.value=response.data.data;
        for(let i=0;i<SongListDetail.value.songs.length;++i){
          SongListDetail.value.songs[i].duration=SecondToTime(parseInt(SongListDetail.value.songs[i].duration));
        }
        //标志为歌单模式
        SongListDetail.value['mode']=1;
        SongListDetail.value.create_date=SongListDetail.value.create_date.split(' ')[0];
        SongListDetail.value.introduction=SongListDetail.value.introduction==='null'?'无简介':SongListDetail.value.introduction;
        SongListVisible.value=true;
        SongListDetail.value['isSubscribed'] = MySubscribeUsers.value.filter((item) => {
          return item.username === SongListDetail.value.owner
        }).length > 0;
        console.log(SongListDetail.value);
      })
      .catch(error=>{
        console.log(error);
      });
}

//添加用户喜爱歌单
export const AddLikeSongList=(id)=>{
  const formData=new FormData();
  formData.append('songlist_id',id);
  instance.post('/like/songlists/add',formData)
    .then(response=>{
      console.log(response.data);
    })
    .catch(error=>{
      console.log(error);
    });
}

//删除用户喜爱歌单
export const DeleteLikeSongList=(id)=>{
  const formData=new FormData();
  formData.append('songlist_id',id);
  instance.post('/like/songlists/delete',formData)
    .then(response=>{
      console.log(response.data);
    })
    .catch(error=>{
      console.log(error);
    });
}