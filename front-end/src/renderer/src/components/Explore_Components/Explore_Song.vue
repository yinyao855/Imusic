<script setup>
import ChooseInput_Component_0 from '@/components/Explore_Components/ChooseInput_Component.vue'
import ChooseInput_Component_1 from '@/components/Explore_Components/ChooseInput_Component.vue'
import ChooseInput_Component_2 from '@/components/Explore_Components/ChooseInput_Component.vue'
import ChooseInput_Component_3 from '@/components/Explore_Components/ChooseInput_Component.vue'
import ChooseInput_Component_4 from '@/components/Explore_Components/ChooseInput_Component.vue'
import {
  ExploreSongs,
  GetTagSongs,
  LanguageOptions,
  MoodOptions,
  SceneOptions,
  StyleOptions,
  ThemeOptions
} from '@/js/Explore_Choose.js'
import { onMounted, ref, watch } from 'vue'
import SongTable from '@/components/SongTable.vue'
import { MusicPlayerVisible } from '@/js/MusicPlayer.js'

//五个选择框的值
const LanguageValue = ref('默认')
const ThemeValue = ref('默认')
const SceneValue = ref('默认')
const MoodValue = ref('默认')
const StyleValue = ref('默认')


//监听选择框的变化
watch(LanguageValue, () => {
  GetTagSongs(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
watch(ThemeValue, () => {
  GetTagSongs(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
watch(SceneValue, () => {
  GetTagSongs(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
watch(MoodValue, () => {
  GetTagSongs(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
watch(StyleValue, () => {
  GetTagSongs(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
onMounted(() => {
  GetTagSongs(LanguageValue.value, ThemeValue.value, SceneValue.value, MoodValue.value, StyleValue.value)
})
</script>

<template>
  <div class="w-full h-full overflow-auto">
    <!--    一系列单选框-->
    <div class="w-full flex flex-wrap">
      <div class="w-1/2 flex">
        <div class="mx-auto">
          <ChooseInput_Component_0 :Values="LanguageOptions" :Name="'SongLanguage'" :Title="'语言'"
                                   v-model:CurrentValue="LanguageValue"></ChooseInput_Component_0>
        </div>
      </div>
      <div class="w-1/2 flex">
        <div class="mx-auto">
          <ChooseInput_Component_1 :Values="ThemeOptions" :Name="'SongTheme'" :Title="'主题'"
                                   v-model:CurrentValue="ThemeValue"
          ></ChooseInput_Component_1>
        </div>
      </div>
      <div class="w-1/2 flex">
        <div class="mx-auto">
          <ChooseInput_Component_2 :Values="SceneOptions" :Name="'SongScene'" :Title="'场景'"
                                   v-model:CurrentValue="SceneValue"
          ></ChooseInput_Component_2>
        </div>
      </div>
      <div class="w-1/2 flex">
        <div class="mx-auto">
          <ChooseInput_Component_3 :Values="MoodOptions" :Name="'SongMood'" :Title="'心情'"
                                   v-model:CurrentValue="MoodValue"
          ></ChooseInput_Component_3>
        </div>
      </div>
      <div class="w-1/2 flex">
        <div class="mx-auto">
          <ChooseInput_Component_4 :Values="StyleOptions" :Name="'SongStyle'" :Title="'风格'"
                                   v-model:CurrentValue="StyleValue"
          ></ChooseInput_Component_4>
        </div>
      </div>
    </div>
    <!--歌曲部分-->
    <div>
      <SongTable :Songs="ExploreSongs"></SongTable>
    </div>
    <div class="w-full h-32" v-if="MusicPlayerVisible"></div>
  </div>
</template>

<style scoped>

</style>