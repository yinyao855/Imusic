<script setup>

import {ref} from 'vue'
import {SystemMessageList} from "@/js/Message.js";
import {Contents, getListeningReportContents, getCreationReportContents} from "@/js/SystemMessage.js";
import {MusicPlayerVisible} from "@/js/MusicPlayer.js";
import SystemMessages_ListeningReport from "@/components/Message_Components/SystemMessages_ListeningReport.vue";
import SystemMessages_CreationReport from "@/components/Message_Components/SystemMessages_CreationReport.vue";

const currentReportTitle = ref("")

// 切换当前点击的周报（听歌周报/创作周报）
const clickReport = (clickedMessage) => {
  currentReportTitle.value = clickedMessage.title
  Contents.value = clickedMessage.content
  if (currentReportTitle.value === '听歌周报') {
    getListeningReportContents()
  } else if (currentReportTitle.value === '创作周报') {
    getCreationReportContents()
  }
}

</script>

<template>
  <div class="w-full h-full">
    <div class="w-full h-full overflow-auto block bg-[#faf3ee]">
      <div class="w-full border-t"></div>
      <div class="w-full border-b h-20 flex hover:bg-gray-300/50 transition-colors ease-in duration-300"
           v-for="(Message,index) in SystemMessageList" :key="index" onclick="report.showModal()"
           @click="clickReport(Message)">
        <img v-if="Message.title==='创作周报'" src="../icons/Message_System_Creation_Report_Icon.svg" alt="创作周报"
             class="h-16 rounded-xl aspect-square inline-block my-auto ml-2 bg-rose-300 p-1"/>
        <img v-if="Message.title==='听歌周报'" src="../icons/Message_System_Listening_Report.svg" alt="听歌周报"
             class="h-16 rounded-xl aspect-square inline-block my-auto ml-2 bg-cyan-300 p-1"/>
        <div class="w-4">
          <img v-if="!Message.is_read" src="../icons/Message_Unread_Icon.svg" alt="未读红点"
               class="h-2 w-2 inline-block rounded-full align-top mt-1"/>
        </div>
        <div class="my-auto ml-2 flex-1 w-20">
          <div class="font-bold text-lg text-gray-600 mb-2">
            {{ Message.title }}
          </div>
        </div>
        <div class="my-auto mr-2">
          {{ Message.send_date }}
        </div>
        <!--        <img :src="Message.Avatar" alt="头像"-->
        <!--             class="h-14 rounded-xl aspect-square inline-block -ml-3"/>-->
      </div>
      <div class="h-32 w-full" v-if="MusicPlayerVisible"></div>
    </div>
  </div>

  <!--  听歌周报-->
  <dialog id="report" class="modal">
    <div class="modal-box">
      <form method="dialog">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
      </form>
      <SystemMessages_ListeningReport
          v-show="currentReportTitle==='听歌周报'"></SystemMessages_ListeningReport>
      <SystemMessages_CreationReport
          v-show="currentReportTitle==='创作周报'"></SystemMessages_CreationReport>
    </div>
  </dialog>
</template>

<style scoped>

</style>