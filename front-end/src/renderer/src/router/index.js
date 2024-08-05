import {createRouter, createWebHashHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/home',
            name: 'home',
            component: HomeView,
            children: [
                {
                    path: 'personalCenter',
                    name: 'personalCenter',
                    component: () => import('../frames/PersonalCenter_MainFrame.vue')
                },
                {
                    path: 'homeView',
                    name: 'homeView',
                    component: () => import('../frames/Home_MainFrame.vue')
                },
                {
                    path: 'explore',
                    name: 'explore',
                    component: () => import('../frames/Explore_MainFrame.vue')
                },
                {
                    path: 'create',
                    name: 'create',
                    component: () => import('../frames/Create_MainFrame.vue')
                },
                {
                    path: 'mySongLists',
                    name: 'mySongLists',
                    component: () => import('../frames/MySongLists_MainFrame.vue')
                },
                {
                    path: 'likeSongLists',
                    name: 'likeSongLists',
                    component: () => import('../frames/LikeSongLists_MainFrame.vue')
                },
                {
                    path: 'message',
                    name: 'message',
                    component: () => import('../frames/Message_MainFrame.vue')
                },
                {
                    path: 'aboutUs',
                    name: 'aboutUs',
                    component: () => import('../frames/AboutUs_MainFrame.vue')
                },
                {
                  path: 'settings',
                  name: 'settings',
                  component: () => import('../frames/Settings.vue')
                },
            ]
        },
        {
            path: '/',
            name: 'root',
            redirect: '/home/homeView'
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('../views/RegisterView.vue')
        },
        {
            path: '/forget-password',
            name: 'forget-password',
            component: () => import('../views/ForgetPasswordView.vue')
        },
    ]
})

export default router
