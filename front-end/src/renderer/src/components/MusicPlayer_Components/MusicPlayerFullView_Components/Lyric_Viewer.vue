<template>
  <div class="w-full h-full flex" :ref="el => LyricPanel = el" @wheel="handleScroll">
    <div class="overflow-hidden w-4/5 h-[90%] m-auto">
        <ul :style="{ transform: `translateY(-${Offset}px)`,transition: `transform 0.5s ease` }" class="px-[56px] h-full">
          <li v-for="(lyricContent, index) in lyricList" :key="index"
              :class="{ 'current-lyric': index === currentIndex, 'NotCurrent-lyric': index !== currentIndex, 'text-center py-1 hover:hover:bg-gray-300/30 transition-colors ease-in duration-100 rounded-lg': true }"
              :ref="el => lyricRefs[index] = el" @click="ChangeLyricIndex(index)">
            {{ lyricContent.content }}
          </li>
        </ul>
    </div>
  </div>
</template>

<script>
import {ref, watch} from 'vue';
import { FullScreenLyricList } from '@/js/SongDetail.js'
import {CurrentTime,IsDragging} from "@/js/MusicPlayer.js";
import { CommentsVisible } from '@/js/Comment.js'

export default {
  setup() {
    const lyricList = ref(FullScreenLyricList);
    //当前歌词列表对应的引用
    const lyricRefs = ref([]);
    //当前歌词面板对应的引用
    const LyricPanel = ref(null);
    //当前歌词索引
    const currentIndex = ref(0);
    //当前偏移量
    const Offset = ref(0);

    const GetCurrentIndex = () => {
      let index = 0;
      if(lyricList.value.length<=1){
        return 0;
      }
      if (parseInt(lyricList.value[lyricList.value.length - 1].timestamp) <= CurrentTime.value) {
        return lyricList.value.length - 1;
      }
      for (let i = 0; i < lyricList.value.length - 1; i++) {
        if (parseInt(lyricList.value[i + 1].timestamp) > CurrentTime.value && parseInt(lyricList.value[i].timestamp) <= CurrentTime.value) {
          index = i;
        }
      }
      return index;
    }

    //处理滑动操作
    const handleScroll=(event)=> {
      Offset.value+=event.deltaY;
    }

    //获取当前偏移量
    const GetOffset = () => {
      Offset.value = 0;
      for (let i = 0; i < currentIndex.value - 1; i++) {
        Offset.value += lyricRefs.value[i].clientHeight;
      }
      Offset.value += lyricRefs.value[currentIndex.value].clientHeight / 2;
      if (Offset.value < LyricPanel.value.clientHeight * 0.4) {
        Offset.value = 0;
      } else {
        Offset.value -= LyricPanel.value.clientHeight * 0.4;
      }
    }

    //点击歌词之后切换
    const ChangeLyricIndex=(index)=>{
      CurrentTime.value=parseInt(lyricList.value[index].timestamp);
      IsDragging.value=true;
    }

    watch(CurrentTime, () => {
      currentIndex.value = GetCurrentIndex();
    });

    watch(CommentsVisible,()=>{
      currentIndex.value = GetCurrentIndex();
    })

    watch(FullScreenLyricList, () => {
      console.log('change');
      lyricList.value = FullScreenLyricList.value;
    });

    watch(currentIndex, () => {
      GetOffset();
    });

    return {
      lyricList,
      lyricRefs,
      currentIndex,
      LyricPanel,
      Offset,
      handleScroll,
      ChangeLyricIndex
    };
  }
};
</script>

<style scoped>
.NotCurrent-lyric {
  width: 100%;
  font-weight: 550;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.5s;
  font-size: 27px; /* 歌词字体大小 */
}

.current-lyric {
  width: 100%;
  color: white;
  font-weight: 700;
  font-size: 36px; /* 高亮行的字体大小 */
}
</style>
