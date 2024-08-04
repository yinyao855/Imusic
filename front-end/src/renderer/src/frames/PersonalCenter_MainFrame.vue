<script setup>
import UploadImage from "@/components/UploadImage.vue";
import {UserStore} from "@/stores/User.js";
import {MusicPlayerVisible} from "@/js/MusicPlayer.js";
import {ref, watch} from 'vue'
import instance from "@/js/axios.js";
import router from '@/router/index.js'
import { ActiveIndex } from '@/js/NavicatStatus.js'

const user_store = UserStore();
//展示的头像
const ShowImage = ref(user_store.Avatar);
//展示的个性签名
const ShowBio = ref(user_store.bio);
//是否要展示确认修改按钮
const ShowChangeButton = ref(false);
//头像图片
const AvatarFile=ref(null);

watch(() => ShowImage.value, () => {
  ShowChangeButton.value = ShowImage.value !== user_store.Avatar || ShowBio.value !== user_store.bio;
});
watch(() => ShowBio.value, () => {
  ShowChangeButton.value = ShowImage.value !== user_store.Avatar || ShowBio.value !== user_store.bio;
});

//确定修改
const ConfirmChange=()=>{
  const formData=new FormData();
  if(ShowImage.value!==user_store.Avatar){
    formData.append('avatar',AvatarFile.value);
  }
  formData.append('bio',ShowBio.value);
  instance.post('/users/update/'+user_store.Username,formData)
      .then(response=>{
        if(response.data.success===true){
          user_store.Avatar=ShowImage.value;
          user_store.bio=ShowBio.value;
          ShowChangeButton.value=false;
        }
      })
      .catch(error=> {
        console.log(error);
      });
}


//退出登录
const LogOut=()=>{
  const user_store=UserStore();
  ActiveIndex.value=1;
  user_store.State=false;
  user_store.Username='';
  user_store.email='';
  user_store.bio='';
  router.push('/home/homeView');
}
</script>

<template>
  <div class="w-full h-screen">
    <div class="h-full overflow-auto bg-[#FAF7F5]">
      <div class="w-full flex mt-4">
        <UploadImage class="mx-8" v-model:ShowImage="ShowImage" v-model:AvatarFile="AvatarFile" :UploadImageId="'PersonalCenter'"></UploadImage>
        <div class="flex flex-wrap">
          <div class="text-3xl my-auto w-full">用户名：{{ user_store.Username }}</div>
          <div class="w-full text-lg">
            注册时间:{{ user_store.Registration_date }}
          </div>
        </div>
      </div>

      <div class="flex">
        <div class="w-3/5 mx-auto">
          <div class="flex flex-col mt-4">
            <div class="text-xl">个性签名</div>
            <div class="flex">
              <textarea v-model="ShowBio" class="w-full h-32 p-2 border-2 rounded-lg"
                        placeholder="请输入个性签名"></textarea>
            </div>
          </div>
          <div class="flex flex-col mt-4">
            <div class="text-xl">邮箱</div>
            <div class="flex">
              <input v-model="user_store.email" class="w-full p-2 border-2 rounded-lg" placeholder="请输入邮箱"
                     disabled>
            </div>
          </div>
          <div class="flex flex-col mt-4">
            <div class="text-xl">角色</div>
            <div class="flex">
              <input :value="user_store.Role==='user'?'用户':'管理员'" class="w-full p-2 border-2 rounded-lg"
                     placeholder="请输入角色" disabled>
            </div>
          </div>
          <div class="w-full my-4 flex">
            <div class="flex m-auto">
              <div class="btn bg-blue-500 hover:bg-blue-600 px-4 mx-2" v-if="ShowChangeButton" @click="ConfirmChange">
                <div class="tracking-widest mx-4">确定修改</div>
              </div>
              <div class="btn bg-red-300 hover:bg-red-400 px-4 mx-2" v-if="ShowChangeButton">
                <div class="tracking-widest mx-4">取消修改</div>
              </div>
              <div class="btn bg-gray-300 hover:bg-gray-400 px-4 mx-2" @click="LogOut">
                <div class="tracking-widest mx-4">退出登录</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
    </div>
  </div>
</template>

<style scoped>

</style>