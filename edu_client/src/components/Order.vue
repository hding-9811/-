<template>
    <div class="cart">
        <Header/>
        <div class="cart-info">
            <h3 class="cart-top">购物车结算 <span>共{{course_list.length}}门课程</span></h3>
            <div class="cart-title">
                <el-row>
                    <el-col :span="2">&nbsp;</el-col>
                    <el-col :span="10">课程</el-col>
                    <el-col :span="8">有效期</el-col>
                    <el-col :span="4">价格</el-col>
                </el-row>
            </div>
            <div class="cart-item" v-for="(course,index) in course_list" :key="index">
                <el-row>
                    <el-col :span="2" class="checkbox">&nbsp;&nbsp;</el-col>
                    <el-col :span="10" class="course-info">
                        <img :src="course.course_img" alt="">
                        <span>{{course.name}}</span>
                    </el-col>
                    <el-col :span="8"><span>{{course.expire_text}}</span></el-col>
                    <el-col :span="4" class="course-price">¥{{course.real_price}}</el-col>
                </el-row>
            </div>

            <div class="calc">
                <el-row class="pay-row">
                    <el-col :span="4" class="pay-col"><span class="pay-text">支付方式：</span></el-col>
                    <el-col :span="8">
                        <span class="alipay"><img src="../../static/image/alipay2.png" alt=""></span>
                        <!--                        <span class="alipay wechat"><img src="../../static/image/wechat.png" alt=""></span>-->
                    </el-col>
                    <el-col :span="8" class="count">实付款： <span>¥{{total_price}}</span></el-col>
                    <el-col :span="4" class="cart-pay" ><span @click="get_order">支付宝支付</span></el-col>
                </el-row>
            </div>
        </div>
        <Footer/>
    </div>
</template>

<script>
    export default {
        name: "Order",
        data() {
            return {
                course_list: [],
                total_price:''
            }
        },
        methods: {
            get_select_course() {
                let token = localStorage.user_token || sessionStorage.user_token;
                this.$axios({
                    url: this.$settings.HOST + "cart/opp/",
                    method: "get",
                    headers: {
                        "Authorization": "jwt " + token
                    }
                }).then(res => {
                    console.log(res.data.course_list);
                    let num = this.$route.params.id;
                    console.log(num)
                    this.course_list = res.data.course_list
                    this.total_price = res.data.total_price

                }).catch(error => {
                    console.log(error)
                })
            },

            // 获取订单详情
            get_order(){
                let token = localStorage.user_token || sessionStorage.user_token;
                this.$axios({
                    url:this.$settings.HOST + "order/option/",
                    method: "post",
                    data:{
                        pay_type: 1

                    },
                    headers: {
                        "Authorization": "jwt " + token
                    }
                }).then(res=>{
                    console.log(res.data)
                    this.$message.success("生成订单成功")
                    this.$axios({
                        url:this.$settings.HOST + "payments/all_pay/",
                        method:"get",
                        params:{
                            order_number:res.data.order_number,
                        }

                    }).then(res=>{
                        location.href = res.data
                    }).catch(error=>{
                        console.log(error.response)
                    })

                })
            },
        },
        created() {

            this.get_select_course()
        }
    }
</script>

<style scoped>
    .cart {
        margin-top: 80px;
    }

    .cart-info {
        overflow: hidden;
        width: 1200px;
        margin: auto;
    }

    .cart-top {
        font-size: 18px;
        color: #666;
        margin: 25px 0;
        font-weight: normal;
    }

    .cart-top span {
        font-size: 12px;
        color: #d0d0d0;
        display: inline-block;
    }

    .cart-title {
        background: #F7F7F7;
        height: 70px;
    }

    .calc {
        margin-top: 25px;
        margin-bottom: 40px;
    }

    .calc .count {
        text-align: right;
        margin-right: 10px;
        vertical-align: middle;
    }

    .calc .count span {
        font-size: 36px;
        color: #333;
    }

    .calc .cart-pay {
        margin-top: 5px;
        width: 110px;
        height: 38px;
        outline: none;
        border: none;
        color: #fff;
        line-height: 38px;
        background: #ffc210;
        border-radius: 4px;
        font-size: 16px;
        text-align: center;
        cursor: pointer;
    }

    .cart-item {
        height: 120px;
        line-height: 120px;
        margin-bottom: 30px;
    }

    .course-info img {
        width: 175px;
        height: 115px;
        margin-right: 35px;
        vertical-align: middle;
    }

    .alipay {
        display: inline-block;
        height: 48px;
    }

    .alipay img {
        height: 100%;
        width: auto;
    }

    .pay-text {
        display: block;
        text-align: right;
        height: 100%;
        line-height: 100%;
        vertical-align: middle;
        margin-top: 20px;
    }

    .course_name, .real_price, .original_price {
        display: inline-block;
        line-height: 140%;
    }

    .course_name .discount {
        color: #ffc210;
    }

    .original_price {
        color: #9b9b9b;
    }

    .course-price {
        line-height: 32px;
    }

    /*优惠券相关的样式*/
    .coupon-box {
        text-align: left;
        padding-bottom: 22px;
        padding-left: 30px;
        border-bottom: 1px solid #e8e8e8;
    }

    .coupon-box::after {
        content: "";
        display: block;
        clear: both;
    }

    .icon-box {
        float: left;
    }

    .icon-box .select-coupon {
        float: left;
        color: #666;
        font-size: 16px;
    }

    .icon-box::after {
        content: "";
        clear: both;
        display: block;
    }

    .select-icon {
        width: 20px;
        height: 20px;
        float: left;
    }

    .select-icon img {
        max-height: 100%;
        max-width: 100%;
        margin-top: 2px;
        transform: rotate(-90deg);
        transition: transform .5s;
    }

    .is_show_select {
        transform: rotate(0deg) !important;
    }

    .coupon-num {
        height: 22px;
        line-height: 22px;
        padding: 0 5px;
        text-align: center;
        font-size: 12px;
        float: left;
        color: #fff;
        letter-spacing: .27px;
        background: #fa6240;
        border-radius: 2px;
        margin-left: 20px;
    }

    .sum-price-wrap {
        float: right;
        font-size: 16px;
        color: #4a4a4a;
        margin-right: 45px;
    }

    .sum-price-wrap .sum-price {
        font-size: 18px;
        color: #fa6240;
    }

    .no-coupon {
        text-align: center;
        width: 100%;
        padding: 50px 0px;
        align-items: center;
        justify-content: center; /* 文本两端对其 */
        border-bottom: 1px solid rgb(232, 232, 232);
    }

    .no-coupon-tips {
        font-size: 16px;
        color: #9b9b9b;
    }

    .credit-box {
        height: 30px;
        margin-top: 40px;
        display: flex;
        align-items: center;
        justify-content: flex-end
    }

    .my_el_check_box {
        position: relative;
    }

    .my_el_checkbox {
        margin-right: 10px;
        width: 16px;
        height: 16px;
    }

    .discount {
        overflow: hidden;
    }

    .discount-num1 {
        color: #9b9b9b;
        font-size: 16px;
        margin-right: 45px;
    }

    .discount-num2 {
        margin-right: 45px;
        font-size: 16px;
        color: #4a4a4a;
    }

    .sun-coupon-num {
        margin-right: 45px;
        margin-bottom: 43px;
        margin-top: 40px;
        font-size: 16px;
        color: #4a4a4a;
        display: inline-block;
        float: right;
    }

    .sun-coupon-num span {
        font-size: 18px;
        color: #fa6240;
    }

    .coupon-list {
        margin: 20px 0;
    }

    .coupon-list::after {
        display: block;
        content: "";
        clear: both;
    }

    .coupon-item {
        float: left;
        margin: 15px 8px;
        width: 190px;
        height: 100px;
        padding: 5px;
        background-color: #fa3030;
        cursor: pointer;
    }

    .coupon-list .active {
        background-color: #fa9000;
    }

    .coupon-list .disable {
        cursor: not-allowed;
        background-color: #fa6060;
    }

    .coupon-condition {
        font-size: 12px;
        text-align: center;
        color: #fff;
    }

    .coupon-name {
        color: #fff;
        font-size: 24px;
        text-align: center;
    }

    .coupon-time {
        text-align: left;
        color: #fff;
        font-size: 12px;
    }

    .unselect {
        margin-left: 0px;
        transform: rotate(-90deg);
    }

    .is_selected {
        transform: rotate(-1turn) !important;
    }

</style>
