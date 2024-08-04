import { ref } from 'vue';
import instance from '@/js/axios.js'

//所有的评论
export const Comments=ref([]);
//是否展示评论
export const CommentsVisible=ref(false);

//获取所有的评论
export const GetComments=(SongId)=>{
  instance.get('/songs/comments',{
    params:{
      songID:SongId
    }
  })
    .then(response=>{
      Comments.value=response.data.data;
      console.log(Comments.value);
      CommentsVisible.value=true;
    })
    .catch(error=>{
      console.log(error);
    })
}


//发评论
export const SendComment=(songID,content)=>{
  const formData=new FormData();
  formData.append('songID',songID);
  formData.append('content',content);
  instance.post('/comments/add',formData)
    .then(response=>{
      console.log(response.data);
      GetComments(songID);
    })
    .catch(error=>{
      console.log(error);
    })
}