//处理搜索操作以及搜索界面

import {ref} from 'vue';
import instance from "@/js/axios.js";
import {SecondToTime} from "@/js/BeforeEnterHomeView.js";
import {UserStore} from "@/stores/User.js";

//是否展示搜索结果
export const SearchResultVisible = ref(false);
//搜索结果
export const SearchResult = ref([]);
//搜索关键字
export const SearchContent = ref('');

//查询搜索结果
export const Search = () => {
    instance.get('/search/songs', {
        params: {
            keyword: SearchContent.value,
            username:UserStore().Username
        }
    })
        .then(response => {
            console.log(response.data);
            SearchResult.value = response.data.data;
            for(let i=0;i<SearchResult.value.length;++i){
                SearchResult.value[i].duration=SecondToTime(parseInt(SearchResult.value[i].duration));
            }
            SearchResultVisible.value = true;
        })
        .catch(error => {
            console.log(error);
        })
}