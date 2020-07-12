import Vue from 'vue'
import Router from 'vue-router'
import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";


Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: "home",
            component: Home
        },
        {
            path: '/home',
            name: "home",
            component: Home
        },
        {
            path: "/login",
            name: "name",
            component: Login,
        },
        {
            path:"/register",
            name:"name",
            component:Register,
        },
    ]
})
