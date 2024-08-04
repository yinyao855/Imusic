import {ref} from "vue";

export const Contents = ref('')
export const ContentDetails = ref({})

const s1 = ref([])
const s2 = ref([])

// 分解听歌周报 Contents
export const getListeningReportContents = () => {
// 您在_至_这段时间内，共听歌_首，累计听歌时长_
    s1.value = Contents.value.split("您在")
    s2.value = s1.value[1].split("这段时间内")
    ContentDetails.value['StartDateAndEndDate'] = s2.value[0]
    s1.value = Contents.value.split("共听歌")
    s2.value = s1.value[1].split("首")
    ContentDetails.value['SongsNumber'] = s2.value[0]
    s1.value = Contents.value.split("累计听歌时长")
    s2.value = s1.value[1].split("分钟")
    ContentDetails.value['Duration'] = s2.value[0]
    ContentDetails.value['Duration'] = ContentDetails.value['Duration'] + "分钟"

// 您最常听的歌曲是_，共播放_次
    s1.value = Contents.value.split("您最常听的歌曲是")
    s2.value = s1.value[1].split("，")
    ContentDetails.value['FavoriteSong'] = s2.value[0]
    s1.value = Contents.value.split("共播放")
    s2.value = s1.value[1].split("次")
    ContentDetails.value['SongPlayTimes'] = s2.value[0]

// 您最常听的歌手是_，共听过他/她的_首歌曲，分别是_
    s1.value = Contents.value.split("您最常听的歌手是")
    s2.value = s1.value[1].split("，")
    ContentDetails.value['FavoriteSinger'] = s2.value[0]
    s1.value = Contents.value.split("共听过他/她的")
    s2.value = s1.value[1].split("首歌曲")
    ContentDetails.value['SingerPlayTimes'] = s2.value[0]
    s1.value = Contents.value.split("分别是")
    s2.value = s1.value[1].split("。")
    ContentDetails.value['SingerPlaySongs'] = s2.value[0]

// 您喜欢听的歌曲风格为_
    s1.value = Contents.value.split("您喜欢听的歌曲风格为")
    s2.value = s1.value[1].split("。")
    ContentDetails.value['FavoriteStyle'] = s2.value[0]

    console.log(ContentDetails['StartDateAndEndDates'])
}

// 分解创作周报 Contents
export const getCreationReportContents = () => {
    console.log(Contents.value)
    // 您在_这段时间内，共上传歌曲_首，创建歌单_个
    s1.value = Contents.value.split("您在")
    s2.value = s1.value[1].split("这段时间内")
    ContentDetails.value['StartDateAndEndDate'] = s2.value[0];
    s1.value = Contents.value.split("共上传歌曲")
    s2.value = s1.value[1].split("首")
    ContentDetails.value['SongsNumber'] = s2.value[0];
    s1.value = Contents.value.split("创建歌单")
    s2.value = s1.value[1].split("个")
    ContentDetails.value['SongListsNumber'] = s2.value[0];

    // 您上传的歌曲有_
    s1.value = Contents.value.split("您上传的歌曲有")
    s2.value = s1.value[1].split("。")
    ContentDetails.value['UploadSongs'] = s2.value[0];

    // 您创建的歌单有修改。
    s1.value = Contents.value.split("您创建的歌单")
    s2.value = s1.value[1].split("。")
    ContentDetails.value['CreateSongLists'] = s2.value[0];

    // 您上传的歌曲共获得_个喜欢，创建的歌单共获得_个收藏
    s1.value = Contents.value.split("您上传的歌曲共获得")
    s2.value = s1.value[1].split("个喜欢")
    ContentDetails.value['FavoriteSongsNumber'] = s2.value[0];
    s1.value = Contents.value.split("创建的歌单共获得")
    s2.value = s1.value[1].split("个收藏")
    ContentDetails.value['FavoriteSongListsNumber'] = s2.value[0];
}