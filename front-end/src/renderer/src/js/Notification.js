//显示弹出的消息提醒框
import {ElMessage, ElNotification} from "element-plus";
import {h} from "vue";

//右侧上部弹出框
export const OpenNotification = (title, message) => {
    ElNotification({
        title: title,
        message: h('i', {style: 'color: teal'}, message),
        duration: 2000,
    })
}


//正上方弹出框
export const OpenMessage = (message, type) => {
    ElMessage({
        message: message,
        type: type,
    });
}