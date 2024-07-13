import {createRouter, createWebHistory} from 'vue-router'
import accountSettings from '../views/accountSettings.vue'
import homePage from '../views/homePage.vue'
import login from '../views/login.vue'
import cartPage from '../views/cartPage.vue'
import myOrders from '../views/myOrders.vue'

const routes = [
    {
        path:'/',
        name:'homePage',
        component:homePage
    },
    {
        path:'/settings',
        name:'account-settings',
        component:accountSettings
    },
    {
        path:'/login',
        name:'login',
        component:login
    },
    {
        path:'/myCart',
        name:'myCart',
        component:cartPage
    },
    {
        path:'/myOrders',
        name:'myOrders',
        component:myOrders
    }
];

const router = createRouter({
    history:createWebHistory(),
    routes,
});


export default router;