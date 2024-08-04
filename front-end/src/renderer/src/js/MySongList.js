import { ref } from 'vue'
import { UserStore } from '@/stores/User.js'
import instance from '@/js/axios.js'
import { OpenMessage } from '@/js/Notification.js'

//我创建的歌单
export const MySongLists = ref([])
//当前要添加到歌单中的歌曲
export const CurrentSongIdNeededToAdd = ref(0)
//是否展示当前的弹出框
export const AddSongToMySongListVisible = ref(false)

//获取到我创建的歌单
export const GetMySongLists = () => {
  if(!CheckLogin()){
    return;
  }
  instance.get('/users/songlists', {
    params: {
      username: UserStore().Username
    }
  })
    .then(response => {
      MySongLists.value = response.data.data
      for(let i=0;i<MySongLists.value.length;++i){
        MySongLists.value[i].create_date=MySongLists.value[i].create_date.split(' ')[0]
      }
      console.log(MySongLists.value)
    })
    .catch(error => {
      console.log(error)
    })
}


//添加歌曲到我的歌单
export const AddSongToMySongList = (songlist_id, song_id) => {
  const formData = new FormData()
  formData.append('songlist_id', songlist_id)
  formData.append('song_id', song_id)
  instance.post('/songlists/addsong', formData)
    .then(response => {
      console.log(response.data)
      if (response.data.success === true) {
        OpenMessage('添加成功', 'success')
      } else {
        OpenMessage('添加失败', 'error')
      }
    })
    .catch(error => {
      console.log(error)
    })
}

//打开弹出框
export const ActiveDialog=(id)=>{
  if(!CheckLogin()){
    return;
  }
  CurrentSongIdNeededToAdd.value=id;
  GetMySongLists();
  AddSongToMySongListVisible.value=true;
}


export const CheckLogin=()=>{
  if(UserStore().State===false){
    OpenMessage('请先登录','error');
    return false;
  }
  return true;
}
