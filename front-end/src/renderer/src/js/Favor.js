//添加喜爱歌曲
import {UserStore} from "@/stores/User.js";
import {OpenMessage} from "@/js/Notification.js";
import instance from "@/js/axios.js";
import { CheckLogin } from '@/js/MySongList.js'

export const AddFavorSong=(id)=>{
    if(!CheckLogin()){
        return;
    }
    const formData=new FormData();
    formData.append('song_id',id);
    instance.post('/like/songs/add',formData)
        .then(response=>{
            console.log(response.data);
        })
        .catch(error=>{
            console.log(error);
        });
}

//删除喜爱歌曲
export const DeleteFavorSong=(id)=>{
    if(!CheckLogin()){
        return;
    }
    const formData=new FormData();
    formData.append('song_id',id);
    instance.post('/like/songs/delete',formData)
        .then(response=>{
            console.log(response.data);
        })
        .catch(error=>{
            console.log(error);
        });
}