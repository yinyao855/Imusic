import instance from "@/js/axios.js";
import {ref} from "vue";


//首页展示的热门歌单
export const HomeView_HotSongLists = ref([]);
//首页展示的热门歌手
export const HomeView_Singers = ref([]);
//首页展示的热门歌曲
export const HomeView_HotSongs = ref([]);
//首页展示的最新歌曲
export const HomeView_NewSongs = ref([]);
//在最新歌曲界面展示的最新歌曲
export const HomeView_NewSongView_NewSongs = ref([]);


export const BeforeEnterHomeView = () => {
    GetHotSongLists();
    GetHotSingers();
    GetHotSongs();
    GetNewSongs();
    GetNewSongViewNewSongs();
}

const GetHotSongLists = () => {
    instance.get('feature/hotsonglists')
        .then(response => {
            HomeView_HotSongLists.value = response.data.data;
            const length=HomeView_HotSongLists.value.length;
            for(let i=0;i<length*2;++i){
              HomeView_HotSongLists.value.push(HomeView_HotSongLists.value[i]);
            }
        })
        .catch(error => {
            console.log(error);
        })
}

const GetHotSingers = () => {
    instance.get('feature/hotsingers')
        .then(response => {
            HomeView_Singers.value = response.data.data;
            const length=HomeView_Singers.value.length;
            for(let i=0;i<length*2;++i){
              HomeView_Singers.value.push(HomeView_Singers.value[i]);
            }
        })
        .catch(error => {
            console.log(error);
        })
}

//把秒数转成时间格式
export const SecondToTime = (InputSecond) => {
    const second = InputSecond % 60;
    const minute = Math.floor(InputSecond / 60);
    if (second < 10)
        return `${minute}:0${second}`;
    return `${minute}:${second}`;
}

const GetHotSongs = () => {
    instance.get('feature/hotsongs')
        .then(response => {
            HomeView_HotSongs.value = response.data.data;
            for (let i = 0; i < HomeView_HotSongs.value.length; ++i) {
                HomeView_HotSongs.value[i].duration = SecondToTime(parseInt(HomeView_HotSongs.value[i].duration));
            }
        })
        .catch(error => {
            console.log(error);
        })
}

const GetNewSongs = () => {
    instance.get('recommend/latest', {
        params: {
            num: 10,
        }
    })
        .then(response => {
            HomeView_NewSongs.value = response.data.data;
            for(let i=0;i<HomeView_NewSongs.value.length;++i){
                HomeView_NewSongs.value[i].duration = SecondToTime(parseInt(HomeView_NewSongs.value[i].duration));
            }
        })
        .catch(error => {
            console.log(error);
        })
}

//在最新歌曲界面展示的二十首歌曲
const GetNewSongViewNewSongs = () => {
    instance.get('recommend/latest', {
        params: {
            num: 20,
        }
    })
        .then(response => {
            HomeView_NewSongView_NewSongs.value = response.data.data;
            for(let i=0;i<HomeView_NewSongView_NewSongs.value.length;++i){
                HomeView_NewSongView_NewSongs.value[i].duration = SecondToTime(parseInt(HomeView_NewSongView_NewSongs.value[i].duration));
            }
        })
        .catch(error => {
            console.log(error);
        })
}

