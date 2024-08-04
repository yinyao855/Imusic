<script setup>
import AboutUs_Card_0 from '@/components/AboutUs_Components/AboutUs_Card.vue'
import AboutUs_Card_1 from '@/components/AboutUs_Components/AboutUs_Card.vue'
import AboutUs_Card_2 from '@/components/AboutUs_Components/AboutUs_Card.vue'
import AboutUs_Card_3 from '@/components/AboutUs_Components/AboutUs_Card.vue'
import AboutUs_Card_4 from '@/components/AboutUs_Components/AboutUs_Card.vue'

import { AboutUsInformation } from '@/js/AboutUsInformation.js'
import { MusicPlayerVisible } from '@/js/MusicPlayer.js'
</script>

<template>
  <div class="w-full h-full overflow-auto flex flex-wrap">
    <div class="flex m-auto">
      <AboutUs_Card_0 :name="AboutUsInformation[0].name" :description="AboutUsInformation[0].description"
                      :url="AboutUsInformation[0].url" class="mx-4 my-4"></AboutUs_Card_0>
      <AboutUs_Card_1 :name="AboutUsInformation[1].name" :description="AboutUsInformation[1].description"
                      :url="AboutUsInformation[1].url" class="mx-4 my-4"></AboutUs_Card_1>
      <AboutUs_Card_2 :name="AboutUsInformation[2].name" :description="AboutUsInformation[2].description"
                      :url="AboutUsInformation[2].url" class="mx-4 my-4"></AboutUs_Card_2>
    </div>
    <div class="flex m-auto">
      <AboutUs_Card_3 :name="AboutUsInformation[3].name" :description="AboutUsInformation[3].description"
                      :url="AboutUsInformation[3].url" class="mx-4 my-4"></AboutUs_Card_3>
      <AboutUs_Card_4 :name="AboutUsInformation[4].name" :description="AboutUsInformation[4].description"
                      :url="AboutUsInformation[4].url" class="mx-4 my-4"></AboutUs_Card_4>
    </div>
    <div class="w-full h-32" v-if="MusicPlayerVisible"></div>
  </div>
</template>

<style scoped>

</style>