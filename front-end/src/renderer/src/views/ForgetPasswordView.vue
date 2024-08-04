<!--忘记密码-->
<script setup>
import {ref, watch} from "vue";
import {OpenNotification} from "@/js/Notification.js";
import instance, {setAuthToken} from "@/js/axios.js";
import router from "@/router/index.js";
import {UserStore} from "@/stores/User.js";


const user_store = UserStore();

const onSubmit = () => {
  if (email.value === '') {
    OpenNotification('更改失败', '请输入邮箱');
  } else if (VerifyPassword.value === '') {
    OpenNotification('更改失败', '请输入验证码');
  } else if (username.value === '') {
    OpenNotification('更改失败', '请输入用户名');
  } else if (password.value === '') {
    OpenNotification('更改失败', '请输入密码');
  } else if (repeatPassword.value !== password.value) {
    OpenNotification('更改失败', '两次密码不相符');
  } else {
    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('new_password', password.value);
    formData.append('verification_code', VerifyPassword.value);
    formData.append('email', email);
    //等待用户接口传出
    instance.post('/users/change-pwd', formData)
        .then(response => {
          if (response.data.success === true) {
            OpenNotification('密码修改成功');
            router.push('/login');
          } else {
            OpenNotification('密码修改失败', response.data.message);
          }
        })
        .catch(error => {
          console.log(error);
        })
  }
}

const username = ref('');
const password = ref('');
const repeatPassword = ref('');
const email = ref('');
// 验证码
const VerifyPassword = ref('');
//验证码按钮中显示的内容
const Content = ref('获取验证码');
const timeLeft = ref(60);
//是否显示倒计时部分
const ShowCountDown = ref(false);


watch(timeLeft, () => {
  let time = timeLeft.value;
  if (time === 0) {
    ShowCountDown.value = false;
    Content.value = '重新获取';
  }
})

let interval = null;

//进入倒计时
const startCountdown = () => {
  const formData = new FormData();
  formData.append('email', email.value);
  let emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (emailPattern.test(email.value) === false) {
    OpenNotification('无法发送', '请输入合法邮箱')
    return;
  }

  //发送验证码

  ShowCountDown.value = true;
  clearInterval(interval);
  timeLeft.value = 60;
  interval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--;
    } else {
      clearInterval(interval);
    }
  }, 1000);

  instance.post('/users/send-code', formData)
      .then(response => {
        if (response.data.success === true) {
          OpenNotification('验证码发送成功', '');
          user_store.token = response.data.token;
          setAuthToken(user_store.token);
        } else {
          OpenNotification('验证码发送失败', response.data.message);
        }
      })
      .catch(error => {
        console.log(error);
      })
}


//输入框是否聚焦
const isFocused = ref(false);
//监听enter键
const EnterOperation = () => {
  if (isFocused.value) {
    onSubmit();
  }
}
</script>

<template>
  <div class="flex w-full h-full use_font">
    <div class="m-auto">
      <div class="relative flex flex-col p-4 text-black bg-white border-2 rounded-lg" style="width: 33rem">
        <div class="text-2xl font-bold mb-2 text-[#1e0e4b] text-center">欢迎来到 <span
            class="bg-gradient-to-r from-[#7747ff]  to-[#A349A4] bg-clip-text text-transparent">Imusic</span></div>
        <div class="text-sm font-normal mb-4 text-center text-[#1e0e4b]">忘记密码</div>
        <form class="flex flex-col gap-3">
          <div class="block relative">
            <label class="block text-gray-600 cursor-text text-sm leading-[140%] font-normal mb-2"
                   for="email">邮箱</label>
            <input id="email" v-model="email"
                   class="rounded border border-gray-200 text-sm w-full font-normal leading-[18px] text-black tracking-[0px] appearance-none block h-11 m-0 p-[11px] focus:ring-2 ring-offset-2  ring-gray-900 outline-0"
                   type="text"
                   @blur="isFocused=false" @focus="isFocused=true" @keydown.enter="EnterOperation">
          </div>
          <div class="block relative">
            <label class="block text-gray-600 cursor-text text-sm leading-[140%] font-normal mb-2"
                   for="VerifyPassword">
              验证码
            </label>
            <div class="flex w-full">
              <input id="VerifyPassword" v-model="VerifyPassword"
                     class="rounded border border-gray-200 text-sm flex-1 font-normal leading-[18px] text-black tracking-[0px] appearance-none block h-11 m-0 p-[11px] focus:ring-2 ring-offset-2  ring-gray-900 outline-0"
                     type="text" @blur="isFocused=false" @focus="isFocused=true" @keydown.enter="EnterOperation">
              <div v-if="!ShowCountDown" class="btn ml-2 w-32 btn-secondary" @click="startCountdown">{{ Content }}</div>
              <div class="flex">
              <span v-if="ShowCountDown" class="countdown font-mono text-2xl text-black px-4 my-auto">
            <span :style="{ '--value': timeLeft }"></span>
              </span>
                <div class="flex h-full">
                  <div v-if="ShowCountDown" class="text-sm my-auto">秒后重新获取</div>
                </div>
              </div>
            </div>
          </div>
          <div class="block relative">
            <label class="block text-gray-600 cursor-text text-sm leading-[140%] font-normal mb-2"
                   for="username">账户</label>
            <input id="username" v-model="username"
                   class="rounded border border-gray-200 text-sm w-full font-normal leading-[18px] text-black tracking-[0px] appearance-none block h-11 m-0 p-[11px] focus:ring-2 ring-offset-2  ring-gray-900 outline-0"
                   type="text" @blur="isFocused=false" @focus="isFocused=true" @keydown.enter="EnterOperation">
          </div>
          <div class="block relative">
            <label class="block text-gray-600 cursor-text text-sm leading-[140%] font-normal mb-2"
                   for="password">新密码</label>
            <input id="password" v-model="password"
                   class="rounded border border-gray-200 text-sm w-full font-normal leading-[18px] text-black tracking-[0px] appearance-none block h-11 m-0 p-[11px] focus:ring-2 ring-offset-2 ring-gray-900 outline-0"
                   type="password" @blur="isFocused=false" @focus="isFocused=true" @keydown.enter="EnterOperation">

          </div>

          <div class="block relative">
            <label class="block text-gray-600 cursor-text text-sm leading-[140%] font-normal mb-2"
                   for="repeat_password">重复密码</label>
            <input id="repeat_password" v-model="repeatPassword"
                   class="rounded border border-gray-200 text-sm w-full font-normal leading-[18px] text-black tracking-[0px] appearance-none block h-11 m-0 p-[11px] focus:ring-2 ring-offset-2 ring-gray-900 outline-0"
                   type="password" @blur="isFocused=false" @focus="isFocused=true" @keydown.enter="EnterOperation">

          </div>
        </form>
        <button class="bg-[#7747ff] w-max mx-auto px-6 py-2 rounded text-white text-sm font-normal my-2"
                @click="onSubmit">重置密码
        </button>
        <div class="text-sm text-center mt-[1.6rem]">已经有帐号了？ <a class="text-sm text-[#7747ff]"
                                                                      href="/login">转到登录</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>