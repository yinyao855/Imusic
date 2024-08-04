<script setup>

import { MusicPlayerVisible } from '@/js/MusicPlayer.js'
import { CommentMessageList } from '@/js/Message.js'
</script>

<template>
  <div class="w-full h-full">
    <div class="w-full h-full overflow-auto block bg-[#faf3ee]">
      <div class="w-full border-t"></div>
      <div class="w-full border-b h-20 flex hover:bg-gray-300/50 transition-colors ease-in duration-300"
           v-for="(Message,index) in CommentMessageList" :key="index" onclick="report.showModal()"
           @click="">
        <img :src="Message.message_cover" alt="头像"
             class="h-16 rounded-xl aspect-square inline-block my-auto ml-2" />
        <div class="w-4">
          <img v-if="!Message.is_read" src="../icons/Message_Unread_Icon.svg" alt="未读红点"
               class="h-2 w-2 inline-block rounded-full align-top mt-1"/>
        </div>
        <div class="my-auto ml-2 flex-1 w-20">
          <div class="font-bold text-lg text-gray-600 mb-2">
            {{ Message.sender }}
          </div>
          <div class="text-sm truncate ...">
            {{ Message.content }}
          </div>
        </div>
        <div class="my-auto mr-2">
          {{ Message.send_date }}
        </div>
      </div>
      <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
    </div>
  </div>
</template>

<style scoped>

</style>