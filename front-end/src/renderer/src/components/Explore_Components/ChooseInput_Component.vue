<template>
  <div class="mb-1">
    <div class="inline">{{ props.Title }}</div>
    <div class="radio-input">
      <label>
        <input v-model="selectedValue" :value="props.Values[0]" :name="props.Name" id="value-1" type="radio" checked="">
        <span>{{ props.Values[0] }}</span>
      </label>
      <label>
        <input v-model="selectedValue" :value="props.Values[1]" :name="props.Name" id="value-2" type="radio">
        <span>{{ props.Values[1] }}</span>
      </label>
      <label>
        <input v-model="selectedValue" :value="props.Values[2]" :name="props.Name" id="value-3" type="radio">
        <span>{{ props.Values[2] }}</span>
      </label>
      <label>
        <input v-model="selectedValue" :value="props.Values[3]" :name="props.Name" id="value-4" type="radio">
        <span>{{ props.Values[3] }}</span>
      </label>
      <label>
        <input v-model="selectedValue" :value="props.Values[4]" :name="props.Name" id="value-5" type="radio">
        <span>{{ props.Values[4] }}</span>
      </label>
      <label>
        <input v-model="selectedValue" :value="props.Values[5]" :name="props.Name" id="value-6" type="radio">
        <span>{{ props.Values[5] }}</span>
      </label>
      <span class="selection"></span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  Values: Array,
  Name: String,
  Title: String
})

const selectedValue = defineModel('CurrentValue') // 初始选中的值

</script>

<style scoped>
@import url('../../css/ChooseInput_Component.css');
</style>
