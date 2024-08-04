import { ref } from "vue";
import { UserStore } from '@/stores/User.js'
import instance from '@/js/axios.js'

//用户喜爱的歌单
export const LikeSongLists = ref([]);

//获取用户喜爱的歌单
export const GetLikeSongLists = () => {
    instance.get('/like/songlists', {
        params: {
            username: UserStore().Username
        }
    })
        .then(response => {
            LikeSongLists.value = response.data.data;
            for(let i=0;i<LikeSongLists.value.length;++i){
                LikeSongLists.value[i].create_date=LikeSongLists.value[i].create_date.split(' ')[0];
            }
        })
        .catch(error => {
            console.log(error);
        });
}