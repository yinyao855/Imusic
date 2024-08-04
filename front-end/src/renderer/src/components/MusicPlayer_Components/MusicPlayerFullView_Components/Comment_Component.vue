<!--评论部分-->
<script setup>
import { onUpdated, ref } from 'vue'
import { Comments, SendComment } from '@/js/Comment.js'
import { CheckLogin } from '@/js/MySongList.js'
import { CurrentSongDetail } from '@/js/MusicPlayer.js'


//消息框的引用
const MessageRef = ref(null)
//是否聚焦
const IsFocus = ref(false)
//点击发送
const SendMessage = () => {
  if(!CheckLogin()){
    return;
  }
  if(Content.value===''){
    return;
  }
  SendComment(CurrentSongDetail.value.id,Content.value);
  Content.value='';
}
//按下enter键
const HandleEnter = () => {
  SendMessage()
}

//输入框中的内容
const Content = ref('')

//点赞
const AddLike = (id,index) => {
  if(!CheckLogin()){
    return;
  }
  Comments.value[index]['is_favor']=true;
  Comments.value[index].like++;
}

//取消点赞
const DeleteLike = (id,index) => {
  if(!CheckLogin()){
    return;
  }
  Comments.value[index]['is_favor']=false;
  Comments.value[index].like--;
}

//自动滚到最后面
onUpdated(() => {
  if(MessageRef.value!==null)
    MessageRef.value.scrollTop = MessageRef.value.scrollHeight
})
</script>

<template>
  <div class="w-full h-full flex">
    <div class="w-3/5 h-[90%] block m-auto">
      <div class="w-full h-[90%] overflow-y-scroll rounded-3xl bg-white/40 p-2" :ref="el=>MessageRef=el">
        <div class="w-full flex flex-wrap" v-for="(Comment,index) in Comments" :key="index">
          <div class="w-full flex">
            <img src="/xht.jpg" alt="头像" class="w-10 rounded-full aspect-square">
            <div class="ml-2 my-auto">
              {{ Comment.user }}
              <div class="text-sm text-gray-600">
                {{ Comment.comment_date }}
              </div>
            </div>
          </div>
          <div class="w-full ml-12 tracking-wide">
            {{ Comment.content }}
          </div>
          <div class="w-full ml-12">
            <img src="../../icons/NotLike_Thrust_Icon.svg" alt="没点赞" class="w-4 h-4 inline-block" v-if="!Comment.is_favor" @click="AddLike(Comment.id,index)">
            <img src="../../icons/Like_Thrust_Icon.svg" alt="点赞" class="w-4 h-4 inline-block" v-else @click="DeleteLike(Comment.id,index)">
            {{Comment.like}}
          </div>
          <div class="w-full border-t my-2 border-t-gray-400"></div>
        </div>
      </div>
      <div class="h-[10%] w-full">
        <div class="flex p-2">
          <input v-model="Content" class="flex-1 p-2 border-2 rounded-lg" placeholder="输入消息" @focus="IsFocus=true"
                 @blur="IsFocus=false" @keydown.enter="HandleEnter">
          <div
            class="w-32 bg-blue-500 hover:bg-blue-600 transition-colors ease-in duration-300 h-12 rounded-xl ml-2 flex"
            @click="SendMessage">
            <div class="m-auto text-white">发送</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>