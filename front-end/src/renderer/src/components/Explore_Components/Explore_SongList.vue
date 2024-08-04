<script setup>
import ChooseInput_Component_0 from '@/components/Explore_Components/ChooseInput_Component.vue'
import ChooseInput_Component_1 from '@/components/Explore_Components/ChooseInput_Component.vue'
import ChooseInput_Component_2 from '@/components/Explore_Components/ChooseInput_Component.vue'
import ChooseInput_Component_3 from '@/components/Explore_Components/ChooseInput_Component.vue'
import ChooseInput_Component_4 from '@/components/Explore_Components/ChooseInput_Component.vue'
import {
  ExploreSongLists,
  GetTagSongLists,
  LanguageOptions,
  MoodOptions,
  SceneOptions,
  StyleOptions,
  ThemeOptions
} from '@/js/Explore_Choose.js'
import { onMounted, ref, watch } from 'vue'
import { GetSongListDetail } from '@/js/SongList.js'
import { MusicPlayerVisible } from '@/js/MusicPlayer.js'

//五个选择框的值
const LanguageValue = ref('默认')
const ThemeValue = ref('默认')
const SceneValue = ref('默认')
const MoodValue = ref('默认')
const StyleValue = ref('默认')


//监听选择框的变化
watch(LanguageValue, () => {
  GetTagSongLists(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
watch(ThemeValue, () => {
  GetTagSongLists(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
watch(SceneValue, () => {
  GetTagSongLists(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
watch(MoodValue, () => {
  GetTagSongLists(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
watch(StyleValue, () => {
  GetTagSongLists(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
onMounted(() => {
  GetTagSongLists(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
</script>

<template>
  <div class="w-full h-full overflow-auto">
    <!--    一系列单选框-->
    <div class="w-full flex flex-wrap">
      <div class="w-1/2 flex">
        <div class="mx-auto">
          <ChooseInput_Component_0 :Values="LanguageOptions" :Name="'SongListLanguage'" :Title="'语言'"
                                   v-model:CurrentValue="LanguageValue"></ChooseInput_Component_0>
        </div>
      </div>
      <div class="w-1/2 flex">
        <div class="mx-auto">
          <ChooseInput_Component_1 :Values="ThemeOptions" :Name="'SongListTheme'" :Title="'主题'"
                                   v-model:CurrentValue="ThemeValue"
          ></ChooseInput_Component_1>
        </div>
      </div>
      <div class="w-1/2 flex">
        <div class="mx-auto">
          <ChooseInput_Component_2 :Values="SceneOptions" :Name="'SongListScene'" :Title="'场景'"
                                   v-model:CurrentValue="SceneValue"
          ></ChooseInput_Component_2>
        </div>
      </div>
      <div class="w-1/2 flex">
        <div class="mx-auto">
          <ChooseInput_Component_3 :Values="MoodOptions" :Name="'SongListMood'" :Title="'心情'"
                                   v-model:CurrentValue="MoodValue"
          ></ChooseInput_Component_3>
        </div>
      </div>
      <div class="w-1/2 flex">
        <div class="mx-auto">
          <ChooseInput_Component_4 :Values="StyleOptions" :Name="'SongListStyle'" :Title="'风格'"
                                   v-model:CurrentValue="StyleValue"
          ></ChooseInput_Component_4>
        </div>
      </div>
    </div>
    <!--歌单部分-->
    <div class="w-full flex flex-wrap mt-2">
      <div class="card card-compact bg-base-100 w-72 shadow-xl mx-4 h-72 my-2" v-for="(SongList,index) in ExploreSongLists"
           :key="index" @click="GetSongListDetail(SongList.id)">
        <figure class="relative">
          <img
            :src="SongList.cover"
            alt="封面"
            class="h-[200px]"
          />
          <div
            class="w-full h-full absolute hover:bg-gray-400/40 transition-colors ease-in duration-300 cursor-pointer"></div>
        </figure>
        <div class="card-body">
          <div class="text-xl">{{ SongList.title }}</div>
          <div>
            <span>创建者：{{ SongList.owner }}</span>
            <span>・</span>
            <span>{{ SongList.create_date }}</span>
          </div>
        </div>
      </div>
      <div class="w-full h-32" v-if="MusicPlayerVisible"></div>
    </div>
  </div>
</template>

<style scoped>

</style>