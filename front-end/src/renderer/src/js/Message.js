import { computed, ref } from 'vue'
import instance from '@/js/axios.js'
import { UserStore } from '@/stores/User.js'

//总的未读信息条数
export const MessageNotRead = computed(() => {
  return AllMessage.value.filter((item) => !item.is_read).length
})

//系统通知未读信息条数
export const SystemMessageNotRead = computed(() => {
  return SystemMessageList.value.filter((item) => !item.is_read).length
})

//评论通知未读信息条数
export const CommentMessageNotRead = computed(() => {
  return CommentMessageList.value.filter((item) => !item.is_read).length
})

//我的私信未读信息条数
export const MyMessageNotRead = computed(() => {
  return MyMessageList.value.filter((item) => !item.is_read).length
})

//投诉通知未读信息条数
export const ReportMessageNotRead = computed(() => {
  return ReportMessageList.value.filter((item) => !item.is_read).length
})

//申诉通知未读信息条数
export const AppealMessageNotRead = computed(() => {
  return AppealMessageList.value.filter((item) => !item.is_read).length
})

//所有消息
export const AllMessage = ref([])

//系统通知列表
export const SystemMessageList = ref([])

//评论通知列表
export const CommentMessageList = ref([])

//我的私信列表
export const MyMessageList = ref([])
//当前选中的好友的私信
export const CurrentFriendMessage = ref([])

//投诉通知列表
export const ReportMessageList = ref([])

//申诉通知
export const AppealMessageList = ref([])


export const Avatars = ref([])

//获取全部的消息
export const GetAllMessage = () => {
  instance.get('/messages/')
    .then(response => {
      // console.log(response.data);
      //获取到的全部信息
      AllMessage.value = response.data.data
      for (let i = 0; i < AllMessage.value.length; ++i) {
        AllMessage.value[i].send_date = AllMessage.value[i].send_date.split(' ')[0]
      }
      SystemMessageList.value = AllMessage.value.filter((item) => item.type === 1)
      CommentMessageList.value = AllMessage.value.filter((item) => {
        return item.type === 2 || item.type === 3 || item.type === 4
      })
      ReportMessageList.value = AllMessage.value.filter((item) => item.type === 6)
      AppealMessageList.value = AllMessage.value.filter((item) => item.type === 7)
    })
    .catch(error => {
      console.log(error)
    })
}


//获取每条消息的头像
const GetAvatar = () => {
  for (let i = 0; i < AllMessage.value.length; ++i) {
    instance.get('/users/info/' + AllMessage.value[i].sender)
      .then(response => {
        AllMessage.value[i]['Avatar'] = response.data.data.avatar
      })
      .catch(error => {
        console.log(error)
      })
  }
}


//是否加载出私信
export const onLoading = ref(false)


//获取私信
export const GetPrivateMessages = () => {
  instance.get('/messages/chats')
    .then(response => {
      MyMessageList.value = response.data.data
      for (let i = 0; i < MyMessageList.value.length; ++i) {
        MyMessageList.value[i].last_message.send_date = TurnProperTime(MyMessageList.value[i].last_message.send_date)
      }
      console.log(MyMessageList.value)
    })
    .catch(error => {
      console.log(error)
    })
}


//获取对应朋友的私信
export const GetFriendMessage = (friendName) => {
  onLoading.value = true
  instance.get('/messages/private', {
    params: {
      friend: friendName
    }
  })
    .then(response => {
      CurrentFriendMessage.value = response.data.data
      for (let i = 0; i < CurrentFriendMessage.value.length; ++i) {
        CurrentFriendMessage.value[i].send_date = TurnProperTime(CurrentFriendMessage.value[i].send_date)
        CurrentFriendMessage.value[i]['orient'] = CurrentFriendMessage.value[i].sender === UserStore().Username ? 'right' : 'left'
      }
      console.log(CurrentFriendMessage.value)
      onLoading.value = false
    })
    .catch(error => {
      console.log(error)
    })
}


//发送消息
export const SendPrivateMessage = (friendName, content) => {
  const formData = new FormData()
  formData.append('receiver', friendName)
  formData.append('content', content)
  instance.post('/messages/send', formData)
    .then(response => {
      console.log(response.data)
    })
    .catch(error => {
      console.log(error)
    })
}

//获取到当前的时间
const GetCurrentDateTime = () => {
  const now = new Date()

  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')

  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}


//将时间转为一个合适的显示方式
const TurnProperTime = (InputTime) => {
  const currentTime = GetCurrentDateTime()
  if (currentTime.split(' ')[0] === InputTime.split(' ')[0]) {
    const currentHour = parseInt(currentTime.split(' ')[1].split(':')[0])
    const inputHour = parseInt(InputTime.split(' ')[1].split(':')[0])
    if (currentHour - inputHour < 1) {
      return '刚刚'
    } else if (currentHour - inputHour < 24) {
      return currentHour - inputHour + '小时前'
    }
  }
  const currentYear = parseInt(currentTime.split(' ')[0].split('-')[0])
  const inputYear = parseInt(InputTime.split(' ')[0].split('-')[0])
  if (currentYear === inputYear) {
    return InputTime.split(' ')[0].split('-')[1] + '月' + InputTime.split(' ')[0].split('-')[2]+'日'
  }
  return InputTime.split(' ')[0].split('-')[0]+'年'+InputTime.split(' ')[0].split('-')[1] + '月' + InputTime.split(' ')[0].split('-')[2]+'日'
}