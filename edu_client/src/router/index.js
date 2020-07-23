import Vue from 'vue'
import Router from 'vue-router'
import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import Course from "../components/Course";
import CourseDetail from "../components/CourseDetail";
import Cart from "../components/Cart";
import Order from "../components/Order";
import OrderSuccess from "../components/OrderSuccess";
import OrderList from "../components/OrderList";


Vue.use(Router)

export default new Router({
    mode:"history",
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
            path: "/register",
            name: "name",
            component: Register,
        },
        {
            path: "/python",
            name: "Course",
            component: Course
        },
        {
            path: "/course/detail",
            name: "Detail",
            component: CourseDetail
        },
        {
            path: "/cart",
            name: 'Cart',
            component: Cart,
        },
        {
            path: "/course/detail/:id",
            name: "Detail",
            component: CourseDetail
        },
        {
            path: "/cart/order",
            name: "Order",
            component: Order
        },
        {
            path: "/cart/order/:id",
            name: "Order",
            component: Order
        },
        {
            path: "/payments/result",
            name: "OrderSuccess",
            component: OrderSuccess,
        },
        {
            path:"/list",
            name:"OrderList",
            component:OrderList,
        },

    ]
})
