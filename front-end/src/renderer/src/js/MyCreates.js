import { ref } from 'vue';
import instance from '@/js/axios.js'
import { UserStore } from '@/stores/User.js'
import { SecondToTime } from '@/js/BeforeEnterHomeView.js'

//上传的所有歌曲
export const MyCreatedSongs=ref([]);


//获取我上传的所有歌曲
export const GetMyCreatedSongs=()=>{
  instance.get('/users/songs',{
    params:{
      username:UserStore().Username
    }
  })
    .then(response=>{
      MyCreatedSongs.value=response.data.data;
      for(let i=0;i<MyCreatedSongs.value.length;++i){
        MyCreatedSongs.value[i].duration=SecondToTime(parseInt(MyCreatedSongs.value[i].duration));
        MyCreatedSongs.value[i].upload_date=MyCreatedSongs.value[i].upload_date.split(' ')[0];
      }
      console.log(MyCreatedSongs.value);
    })
    .catch(error=>{
      console.log(error);
    });
}