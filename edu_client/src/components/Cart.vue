<template>
    <div class="cart">
        <Header></Header>
        <div class="cart_info">
            <div class="cart_title">
                <span class="text">我的购物车</span>
                <span class="total">共4门课程</span>
            </div>
            <div class="cart_table">
                <div class="cart_head_row">
                    <span class="doing_row"></span>
                    <span class="course_row">课程</span>
                    <span class="expire_row">有效期</span>
                    <span class="price_row">单价</span>
                    <span class="do_more">操作</span>
                </div>
                <div class="cart_course_list">
                    <CartItem v-for="(course,index) in cart_list" :key="index" :course="course" @delete_course="del_cart(index)" @change_selected="get_total_price"></CartItem>


                </div>
                <div class="cart_footer_row">
                    <span class="cart_select"><label> <el-checkbox
                        v-model="checked"></el-checkbox><span>全选</span></label></span>
                    <span class="cart_delete"><i class="el-icon-delete"></i> <span>删除</span></span>
                    <span class="goto_pay"><router-link to="/cart/order">去结算</router-link></span>
                    <span class="cart_total">总计：¥{{total_price}}</span>
                </div>
            </div>
        </div>
        <Footer></Footer>
    </div>
</template>

<script>
    import CartItem from "./common/CartItem";
    import Header from "./common/Header";
    import Footer from "./common/Footer";

    export default {
        name: "Cart",
        data() {
            return {
                checked: "",
                cart_list: [],
                total_price: ""
            }
        },
        components: {
            CartItem, Header, Footer
        },
        methods: {

            // 判断是否登录
            check_user_login() {
                let token = localStorage.user_token || sessionStorage.user_token;

                if (!token) {
                    let self = this;
                    this.$confirm("对不器，请登录后在添加购物车", {
                        callback() {
                            self.$router.push("/login");
                        }
                    });
                    return false

                }
                return token
            },

            get_cart() {
                //获取购物车判断用户是否已经登录
                let token = this.check_user_login()
                this.$axios.get(`${this.$settings.HOST}cart/option/`, {
                    headers: {
                        "Authorization": "jwt " + token

                    }
                }).then(res => {
                    console.log(res.data)

                    this.cart_list = res.data
                    this.$store.commit("add_cart", this.cart_list.length);
                    this.get_total_price()
                }).catch(error => {
                    console.log(error.response)
                })
            },
            //
            get_total_price() {
                let total = 0;
                this.cart_list.forEach((course, key) => {
                    //判断购物车的商品是否被选中
                    if (course.selected) {
                        total += parseFloat(course.real_price)
                    }
                    this.total_price = total
                    console.log(this.total_price)

                })
            },

            //删除购物车商品

            del_cart(key){
                console.log(key)
                this.cart_list.splice(key,1)
                // 删除后更新购物车熟练
                this.$store.commit("add_cart" ,this.cart_list.length);

                // 删除后更新总价
                this.get_total_price()

            },

        },
        created() {
            this.get_cart()


        },




    }
</script>

<style scoped>
    .cart_info {
        width: 1200px;
        margin: 0 auto 200px;
    }

    .cart_title {
        margin: 25px 0;
    }

    .cart_title .text {
        font-size: 18px;
        color: #666;
    }

    .cart_title .total {
        font-size: 12px;
        color: #d0d0d0;
    }

    .cart_table {
        width: 1170px;
    }

    .cart_table .cart_head_row {
        background: #F7F7F7;
        width: 100%;
        height: 80px;
        line-height: 80px;
        padding-right: 30px;
    }

    .cart_table .cart_head_row::after {
        content: "";
        display: block;
        clear: both;
    }

    .cart_table .cart_head_row .doing_row,
    .cart_table .cart_head_row .course_row,
    .cart_table .cart_head_row .expire_row,
    .cart_table .cart_head_row .price_row,
    .cart_table .cart_head_row .do_more {
        padding-left: 10px;
        height: 80px;
        float: left;
    }

    .cart_table .cart_head_row .doing_row {
        width: 78px;
    }

    .cart_table .cart_head_row .course_row {
        width: 530px;
    }

    .cart_table .cart_head_row .expire_row {
        width: 188px;
    }

    .cart_table .cart_head_row .price_row {
        width: 162px;
    }

    .cart_table .cart_head_row .do_more {
        width: 162px;
    }

    .cart_footer_row {
        padding-left: 30px;
        background: #F7F7F7;
        width: 100%;
        height: 80px;
        line-height: 80px;
    }

    .cart_footer_row .cart_select span {
        margin-left: -7px;
        font-size: 18px;
        color: #666;
    }

    .cart_footer_row .cart_delete {
        margin-left: 58px;
    }

    .cart_delete .el-icon-delete {
        font-size: 18px;
    }

    .cart_delete span {
        margin-left: 15px;
        cursor: pointer;
        font-size: 18px;
        color: #666;
    }

    .cart_total {
        float: right;
        margin-right: 62px;
        font-size: 18px;
        color: #666;
    }

    .goto_pay {
        float: right;
        width: 159px;
        height: 80px;
        outline: none;
        border: none;
        background: #ffc210;
        font-size: 18px;
        color: #fff;
        text-align: center;
        cursor: pointer;
    }
</style>
