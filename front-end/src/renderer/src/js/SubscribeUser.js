import { ref } from 'vue'
import instance from '@/js/axios.js'
import { UserStore } from '@/stores/User.js'

//我关注的用户
export const MySubscribeUsers = ref([])


// 关注用户
export const SubscribeUser=(id)=>{
  const formData=new FormData();
  formData.append('username',id);
  instance.post('/users/follow',formData)
    .then(response=>{
      console.log(response.data)
      GetMySubscribeUsers();
    })
    .catch(error=>{
      console.log(error.response.data)
    });
}

//获取我关注的用户
export const GetMySubscribeUsers=()=>{
  instance.get('/users/followings',{
    params:{
      username:UserStore().Username
    }
  })
    .then(response=>{
      console.log(response.data.data);
      MySubscribeUsers.value=response.data.data
    })
    .catch(error=>{
      console.log(error.response.data)
    });
}