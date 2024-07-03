// src/utils/tabManager.js
import { shallowRef } from 'vue';
import MusicView from '@/views/MusicView.vue';
import MyHomeView from "@/views/MyHomeView.vue";
import MusicListView from "@/views/MusicListView.vue";
import UserView from "@/views/UserView.vue";
import SettingsView from "@/views/SettingsView.vue";

const tabList = {
    '1': ['我的主页', MyHomeView],
    '2-1': ['歌曲管理', MusicView],
    '2-2': ['歌单管理', MusicListView],
    '2-4': ['用户管理', UserView],
    '3': ['设置', SettingsView],
}

let tabIndex = 1;

const editableTabsValue = shallowRef('1');
const editableTabs = shallowRef([
    {
        title: '我的主页',
        name: '1',
        content: MyHomeView,
    },
]);

const addTab = (type) => {
    // 如果type不在tabList中，直接返回
    if (!tabList[type]) return;
    const newTabName = `${++tabIndex}`;
    editableTabs.value.push({
        title: tabList[type][0],
        name: newTabName,
        content: tabList[type][1],
    });
    editableTabsValue.value = newTabName;
};

const removeTab = (targetName) => {
    const tabs = editableTabs.value;
    let activeName = editableTabsValue.value;
    if (activeName === targetName) {
        tabs.forEach((tab, index) => {
            if (tab.name === targetName) {
                const nextTab = tabs[index + 1] || tabs[index - 1];
                if (nextTab) {
                    activeName = nextTab.name;
                }
            }
        });
    }

    editableTabsValue.value = activeName;
    editableTabs.value = tabs.filter((tab) => tab.name !== targetName);
};

export { editableTabsValue, editableTabs, addTab, removeTab };
