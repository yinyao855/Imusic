<!--关于我们的卡片-->
<script setup>
const props = defineProps({
  name: String,
  description: String,
  url: String
})
</script>

<template>
  <div class="card">
    <div class="container">
      <div class="w-full h-full flex">
        <img :src="props.url" alt="头像" class="rounded-full aspect-square w-[90%] m-auto">
      </div>
    </div>
    <div class="card-header">
      <span class="w-1/2 mt-2">{{ props.description }}</span>
    </div>
    <span class="temp">{{ props.name }} </span>
  </div>
</template>

<style scoped>
@import url('../../css/AboutUs_Card.css');
</style>