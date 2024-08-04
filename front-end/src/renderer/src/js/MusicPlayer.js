import {computed, ref} from 'vue';
import instance from "@/js/axios.js";
import {UserStore} from "@/stores/User.js";
import { GetFullScreenLyric } from '@/js/HandleLyrics.js'

//是否可见音乐播放器
export const MusicPlayerVisible = ref(false);
//当前播放的乐曲id
export const CurrentSongId = ref(0);
//当前播放的乐曲的详细信息
export const CurrentSongDetail = ref({});
//歌曲长度
export const Duration = ref(0);
//当前播放列表
export const CurrentPlayList = ref([]);
//当前是否在播放
export const IsPlaying = ref(false);
//当前播放的音乐的播放进度
export const CurrentTime = ref(0);
//当前播放的音乐的总时长
export const TotalTime = ref(0);
//当前播放的音乐的音量
export const Volume = computed(() => {
    return VolumePercent.value / 100;
});
//是否拖动了进度条
export const IsDragging = ref(false);
//当前播放类型
export const PlayType = ref(0);
//百分制音量
export const VolumePercent = ref(40);
//是否显示播放列表
export const PlayListVisible = ref(false);
//是否全屏播放
export const IsFullScreen = ref(false);
//播放方式的提示
export const MusicPlayModeDataTip = [
    '列表循环',
    '单曲循环',
    '随机播放'
]

//将字符串形式时间转换为秒数
export const TimeStringToSecond = (time) => {
    let tmp = time.split(':');
    return (parseInt(tmp[0]) * 60 + parseFloat(tmp[1])).toFixed(2);
}

//播放下一首歌
export const NextSong = () => {
    if (PlayType.value === 1) {
        CurrentTime.value = 0;
        return;
    }
    let index = CurrentPlayList.value.findIndex(item => item.id === CurrentSongId.value);
    if (index === CurrentPlayList.value.length - 1) {
        index = 0;
    } else {
        index++;
    }
    if (PlayType.value === 2) {
        index = Math.floor(Math.random() * CurrentPlayList.value.length);
    }
    CurrentSongId.value = CurrentPlayList.value[index].id;
    GetCurrentSongDetail();
}


//播放上一首歌
export const PreviousSong = () => {
    if (PlayType.value === 1) {
        CurrentTime.value = 0;
        return;
    }
    let index = CurrentPlayList.value.findIndex(item => item.id === CurrentSongId.value);
    if (index === 0) {
        index = CurrentPlayList.value.length - 1;
    } else {
        index--;
    }
    if (PlayType.value === 2) {
        index = Math.floor(Math.random() * CurrentPlayList.value.length);
    }
    CurrentSongId.value = CurrentPlayList.value[index].id;
    GetCurrentSongDetail();
}

//获取当前播放音乐的详细信息
export const GetCurrentSongDetail = () => {
    instance.get('/songs/info/' + CurrentSongId.value)
        .then(response => {
            CurrentSongDetail.value = response.data.data;
            GetFullScreenLyric(CurrentSongDetail.value.lyric);
            AddSongToCurrentPlayList(CurrentSongDetail.value);
            MusicPlayerVisible.value = true;
            Duration.value = parseInt(CurrentSongDetail.value.duration);
            CurrentTime.value = 0;
            //触发播放
            IsPlaying.value = false;
            IsPlaying.value = true;
        })
        .catch(error => {
            console.log(error);
        })
}

//向当前播放列表中添加音乐
export const AddSongToCurrentPlayList = (song) => {
    let tmp = CurrentPlayList.value.filter(item => item.id === song.id);
    if (tmp.length !== 0) {
        return;
    }
    CurrentPlayList.value.push(song);
}

//播放全部歌曲
export const PlayAll=(PlayList)=>{
    CurrentPlayList.value=PlayList;
    CurrentSongId.value=CurrentPlayList.value[0].id;
    GetCurrentSongDetail();
}

//立即播放当前歌曲
export const HandlePlayNow = (id) => {
    CurrentSongId.value = id;
    GetCurrentSongDetail(id);
    IsPlaying.value = false;
    IsPlaying.value = true;
}

//获取播放列表
export const GetPlayList = () => {
    if (UserStore().State === false) {
        CurrentPlayList.value = [];
        return;
    }
    instance.get('/feature/recent', {
        params: {
            num: -1,
        }
    })
        .then(response => {
            console.log(response.data);
            CurrentPlayList.value = response.data.data.songs;
            if (UserStore().State === false || CurrentPlayList.value.length === 0) {
                MusicPlayerVisible.value = false;
            } else {
                MusicPlayerVisible.value = true;
                CurrentSongId.value = CurrentPlayList.value[0].id;
                GetCurrentSongDetail();
            }
        })
        .catch(error => {
            console.log(error);
        })
}