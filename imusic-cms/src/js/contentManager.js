// 管理歌曲、歌单、歌手、用户页面信息
import instance from "@/js/axiosConfig.js";
import {ElMessage, ElNotification} from "element-plus";

// 编辑模式，0为新建，1为修改
let editMode = 0

let curEditUer = {}
let curEditSong = {}

function setEditMode(mode) {
    editMode = mode
}

function getUserInfo(username, role) {
    instance.get(`/users/info/${username}`)
        .then((response) => {
            if (response.data.success === true) {
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

function getSongInfo(songId) {
    instance.get(`/songs/info/${songId}`)
        .then((response) => {
            if (response.data.success === true) {
                curEditSong = response.data.data
            }
            else {
                ElMessage.error(response.data.message)
            }
        })
        .catch((error) => {
            console.log(error)
        })
}

function setUserInfo(username, formData) {
    return new Promise((resolve, reject) => {
        instance.post(`users/update/${username}`, formData)
            .then(r => {
                if (r.data.success === true) {
                    ElNotification({
                        title: 'Success',
                        message: '用户信息修改成功',
                        type: 'success'
                    });
                    resolve(r.data); // Resolve with data if successful
                } else {
                    ElNotification({
                        title: 'Error',
                        message: r.data.message,
                        type: 'error'
                    });
                    reject(r.data.message); // Reject with error message
                }
            })
            .catch((error) => {
                console.log(error);
                reject(error); // Reject with error object
            });
    });
}

function changeUserRole(username, role) {
    return new Promise((resolve, reject) => {
        const formData = new FormData();
        formData.append('role', role);
        formData.append('dir_user', username);

        instance.post('users/change-role', formData)
            .then(r => {
                if (r.data.success === true) {
                    ElNotification({
                        title: 'Success',
                        message: '用户角色修改成功',
                        type: 'success'
                    });
                    resolve(r.data); // Resolve with data if successful
                } else {
                    ElNotification({
                        title: 'Error',
                        message: r.data.message,
                        type: 'error'
                    });
                    reject(r.data.message); // Reject with error message
                }
            })
            .catch((error) => {
                console.log(error);
                reject(error); // Reject with error object
            });
    });
}

function setSongInfo(songId, formData) {
    return new Promise((resolve, reject) => {
        instance.post(`songs/update/${songId}`, formData)
            .then(r => {
                if (r.data.success === true) {
                    ElNotification({
                        title: 'Success',
                        message: '歌曲信息修改成功',
                        type: 'success'
                    });
                    resolve(r.data);
                } else {
                    ElNotification({
                        title: 'Error',
                        message: r.data.message,
                        type: 'error'
                    });
                    reject(r.data.message);
                }
            })
            .catch((error) => {
                console.log(error);
                reject(error);
            });
    });
}

// 上传歌曲
function createSong(formData) {
    return new Promise((resolve, reject) => {
        instance.post('songs/upload', formData)
            .then(r => {
                if (r.data.success === true) {
                    ElNotification({
                        title: 'Success',
                        message: '歌曲上传成功',
                        type: 'success'
                    });
                    resolve(r.data);
                } else {
                    ElNotification({
                        title: 'Error',
                        message: r.data.message,
                        type: 'error'
                    });
                    reject(r.data.message);
                }
            })
            .catch((error) => {
                console.log(error);
                reject(error);
            });
    });
}

export {
    curEditUer,
    curEditSong,
    editMode,
    getUserInfo,
    getSongInfo,
    setEditMode,
    setUserInfo,
    setSongInfo,
    changeUserRole,
    createSong
}