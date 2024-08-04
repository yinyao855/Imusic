<!--输入框组件-->
<script setup>
import {ref} from "vue";
import {OpenMessage} from "@/js/Notification.js";
import {Search, SearchContent} from "@/js/Search.js";

//输入框是否聚焦
const isFocused = ref(false);

const SearchOperation = () => {
  if(SearchContent.value===''){
    OpenMessage('搜索内容不能为空','error');
  }
  else{
    Search();
  }
}
</script>

<template>
  <div class="z-20 fixed top-1 right-2">
    <div class="group">
      <svg viewBox="0 0 24 24" aria-hidden="true" class="icon">
        <g>
          <path
              d="M21.53 20.47l-3.66-3.66C19.195 15.24 20 13.214 20 11c0-4.97-4.03-9-9-9s-9 4.03-9 9 4.03 9 9 9c2.215 0 4.24-.804 5.808-2.13l3.66 3.66c.147.146.34.22.53.22s.385-.073.53-.22c.295-.293.295-.767.002-1.06zM3.5 11c0-4.135 3.365-7.5 7.5-7.5s7.5 3.365 7.5 7.5-3.365 7.5-7.5 7.5-7.5-3.365-7.5-7.5z"
          ></path>
        </g>
      </svg>
      <input class="input" type="search" placeholder="搜索歌手/歌曲" v-model="SearchContent" @focus="isFocused=true"
             @blur="isFocused=false" @keydown.enter="SearchOperation"/>
      <div
          class="rounded-md bg-blue-400 hover:bg-blue-500 w-20 text-center h-10 flex transition-colors ease-in duration-300">
        <div class="m-auto" @click="SearchOperation">搜索</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.group {
  display: flex;
  line-height: 28px;
  align-items: center;
  position: relative;
  max-width: 290px;
}

.input {
  width: 100%;
  height: 40px;
  line-height: 28px;
  padding: 0 1rem 0 2.5rem;
  border: 1px solid rgba(128, 128, 128, 0.46);
  border-radius: 8px;
  outline: none;
  background-color: #f3f3f4;
  color: #0d0c22;
  transition: 0.3s ease;
}

.input::placeholder {
  color: #9e9ea7;
}

.input:focus,
input:hover {
  outline: none;
  border-color: rgba(247, 127, 0, 0.4);
  background-color: #fff;
  box-shadow: 0 0 0 4px rgb(247 127 0 / 10%);
}

.icon {
  position: absolute;
  left: 1rem;
  fill: #9e9ea7;
  width: 1rem;
  height: 1rem;
}
</style>