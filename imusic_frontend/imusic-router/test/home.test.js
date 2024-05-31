// 引入需要的库和组件
import { mount } from '@vue/test-utils'
import Home from '@/views/Home.vue'
import {createPinia} from "pinia";
describe('Home.vue', () => {
    it('renders correctly', () => {
        // 创建一个新的 Pinia 实例
        const pinia = createPinia();

        // 在挂载组件时将 Pinia 实例添加到 Vue 应用中
        const wrapper = mount(Home, {
            global: {
                plugins: [pinia],
            },
        });

        expect(wrapper.element).toMatchSnapshot();
    });
    //测试点击事件
    it('click event', async () => {
        // 创建一个新的 Pinia 实例
        const pinia = createPinia();

        // 在挂载组件时将 Pinia 实例添加到 Vue 应用中
        const wrapper = mount(Home, {
            global: {
                plugins: [pinia],
            },
        });

        // 触发点击事件

    });

});