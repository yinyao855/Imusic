// 管理歌曲、歌单、歌手、用户页面信息
import instance from "@/js/axiosConfig.js";
import {ElMessage} from "element-plus";

const userList = {}
let curEditUer = {}

function getUserInfo(username, role) {
    instance.get(`/users/info/${username}`)
        .then((response) => {
            if (response.data.success === true) {
                // console.log(response.data)
                userList[username] = response.data.data
                curEditUer = response.data.data
                curEditUer.role = role
            }
            else {
                ElMessage.error(response.data.message)
            }
        })
        .catch((error) => {
            console.log(error)
        })
}

export {userList, curEditUer, getUserInfo}