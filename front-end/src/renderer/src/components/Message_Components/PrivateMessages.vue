<script setup>
import { computed, onMounted, onUpdated, ref,onUnmounted } from 'vue'
import {
  CurrentFriendMessage,
  GetFriendMessage,
  GetPrivateMessages,
  MyMessageList,
  onLoading,
  SendPrivateMessage
} from '@/js/Message.js'
import { MusicPlayerVisible } from '@/js/MusicPlayer.js'
import { UserStore } from '@/stores/User.js'

onMounted(GetPrivateMessages)

//对话部分的引用
const MessageRef = ref(null)
//输入栏里的消息
const Content = ref('')
//当前聊天的人
const CurrentFriend = ref('我的聊天')
//当前聊天的人的头像
const CurrentFriendAvatar = ref('')
//是否显示当前的聊天
const MessageVisible=ref(false);


//是否已经聚焦了聊天框
const IsFocus = ref(false);
//点击了enter之后的操作
const HandleEnter=()=>{
  if(IsFocus.value){
    ThisPageGetFriendMessage(CurrentFriend.value,CurrentFriendAvatar.value);
  }
}

const MessageHeight = computed(() => {
  return windowInnerHeight.value - 171;
})


// 监听窗口大小变化
const windowInnerHeight = ref(window.innerHeight-(MusicPlayerVisible.value === true ? 128 : 0));
const handleResize = () => {
  const tmp=MusicPlayerVisible.value === true ? 128 : 0;
  windowInnerHeight.value = window.innerHeight-tmp;
};

onMounted(() => {
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});

//中转
const ThisPageGetFriendMessage = (friendName, friendAvatar) => {
  CurrentFriend.value = friendName
  CurrentFriendAvatar.value = friendAvatar
  GetFriendMessage(friendName)
  MessageVisible.value=true;
}

//发送消息
const SendMessage = () => {
  if (Content.value === '') {
    return
  }
  let NewMessage
  NewMessage = {
    sender: UserStore().Username,
    receiver: CurrentFriend.value,
    content: Content.value,
    send_date: '片刻之前',
    orient: 'right'
  }
  CurrentFriendMessage.value.push(NewMessage)
  SendPrivateMessage(CurrentFriend.value, Content.value)
  Content.value = ''
}

onUpdated(() => {
  if(MessageRef.value!==null)
  MessageRef.value.scrollTop = MessageRef.value.scrollHeight
})

onMounted(()=>{
  MessageVisible.value=false;
  CurrentFriend.value='我的聊天'
})
</script>

<template>
  <div class="w-full h-full flex flex-row">
    <div class="w-[30%] h-full overflow-auto block bg-[#faf3ee]">
      <div class="w-full border-t"></div>
      <div class="w-full border-b h-20 flex hover:bg-gray-300/50 transition-colors ease-in duration-300"
           v-for="(MyMessage,index) in MyMessageList" :key="index"
           @click="ThisPageGetFriendMessage(MyMessage.friend,MyMessage.friend_avatar)">
        <img :src="MyMessage.friend_avatar" alt="头像"
             class="h-16 rounded-xl aspect-square inline-block my-auto ml-2" />
        <div class="my-auto ml-2 flex-1 w-20">
          <div class="font-bold text-lg text-gray-600 mb-2">
            {{ MyMessage.friend }}
          </div>
          <div class="text-sm truncate ...">
            {{ MyMessage.last_message.content }}
          </div>
        </div>
        <div class="my-auto mr-2">
          {{ MyMessage.last_message.send_date }}
        </div>
      </div>
      <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
    </div>
    <div class="w-[70%] h-full">
      <div class="w-full h-12 text-center text-lg border-2 flex">
        <div class="m-auto">{{ CurrentFriend }}</div>
      </div>
      <div class="w-full flex" :style="{height:`${MessageHeight}px`}"  v-if="!MessageVisible">
        <img src="../icons/Chat_Icon.svg" alt="聊天" class="m-auto w-32 h-32">
      </div>
      <div class="w-full overflow-auto flex flex-wrap" :style="{height:`${MessageHeight}px`}" v-if="MessageVisible">
        <div class="w-full h-full flex" v-if="onLoading">
          <span class="loading loading-spinner loading-lg m-auto text-primary"></span>
        </div>
        <div class="w-full overflow-y-scroll" :ref="el=>MessageRef=el" :style="{ height: `${MessageHeight}px` }" v-else>
          <div class="w-full h-16 my-2 px-3" v-for="(Message,index) in CurrentFriendMessage" :key="index">
            <div :class="{'chat':true, 'chat-start':Message.orient==='left','chat-end':Message.orient==='right'}">
              <div class="chat-image avatar">
                <div class="w-10 rounded-full">
                  <img
                    alt="头像"
                    :src="Message.orient==='left'?CurrentFriendAvatar:UserStore().Avatar" />
                </div>
              </div>
              <div class="chat-header">
                {{ Message.sender }}
                <time class="text-xs opacity-50">{{ Message.send_date }}</time>
              </div>
              <div
                :class="{'chat-bubble':true,'chat-bubble-primary':Message.orient==='left','chat-bubble-success':Message.orient==='right'}">
                {{ Message.content }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex p-2" v-if="MessageVisible">
        <input v-model="Content" class="flex-1 p-2 border-2 rounded-lg" placeholder="输入消息" @focus="IsFocus=true" @blur="IsFocus=false" @keydown.enter="HandleEnter">
        <div class="w-32 bg-blue-500 hover:bg-blue-600 transition-colors ease-in duration-300 h-12 rounded-xl ml-2 flex"
             @click="SendMessage">
          <div class="m-auto text-white">发送</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>