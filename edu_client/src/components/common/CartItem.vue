<template>
    <div class="cart_item">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img src="../../../static/image/python.jpg" alt="">
            <span><router-link :to="'/course/detail/'+course.id">{{course.name}}</router-link></span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                <el-option :label="item.expire_text" :value="item.id" :key="item.id" v-for="item in course.expire_list">

                </el-option>

            </el-select>
        </div>
        <div class="cart_column column_4">¥{{course.price.toFixed(2)}}</div>
        <div class="cart_column column_4"><a href="javascript:void (0)" @click="delete_course">删除</a></div>
    </div>
</template>

<script>
    export default {
        name: "CartItem",
        //接收父组件传递过来的课程参数
        props: ["course"],
        watch: {
            //通过检测selected的变化 改变当前选中的状态
            "course.selected": function () {
                this.change_selected()
            },
            //切换课程有效期
            "course.expire_id":function () {
                this.change_expire()

            }
        },
        methods: {

            //切换状态
            change_selected() {
                let token = localStorage.user_token || sessionStorage.user_id
                this.$axios.patch(`${this.$settings.HOST}cart/option/`, {
                    selected: this.course.selected,
                    course_id: this.course.id,
                }, {
                    headers: {
                        "Authorization": "jwt " + token
                    }
                }).then(res => {
                    this.$message.success(res.data.message)

                }).catch(error => {
                    this.$message.error(error.response)
                })
            },

            //删除
            delete_course() {
                let token = localStorage.user_token || sessionStorage.user_id
                this.$axios({
                    url: this.$settings.HOST + "cart/option/",
                    method: "delete",
                    data: {
                        course_id: this.course.id

                    },
                    headers: {
                        "Authorization": "jwt " + token
                    }
                }).then(res => {
                    this.$message.success(res.data.message)
                }).catch(error => {
                    this.$message.error(error.response)
                })
            },

            change_expire() {
                let token = sessionStorage.user_token || localStorage.user_token
                this.$axios({
                    url: this.$settings.HOST + "cart/option/",
                    method: "put",
                    data: {
                        expire_id: this.course.expire_id,
                        course_id: this.course.id,
                    },
                    headers: {
                        "Authorization": "jwt " + token,
                    }
                }).then(res=>{
                    console.log(res.data)
                    this.course.real_price = res.data.real_price;
                    this.$message.success("切换有效期成功")

                }).catch(error=>{
                    console.log(error)
                })
            }
        },
        data() {
            return {
                expire: "1个月有效",
            }
        }
    }
</script>

<style scoped>
    .cart_item::after {
        content: "";
        display: block;
        clear: both;
    }

    .cart_column {
        float: left;
        height: 250px;
    }

    .cart_item .column_1 {
        width: 88px;
        position: relative;
    }

    .my_el_checkbox {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        top: 0;
        margin: auto;
        width: 16px;
        height: 16px;
    }

    .cart_item .column_2 {
        padding: 67px 10px;
        width: 520px;
        height: 116px;
    }

    .cart_item .column_2 img {
        width: 175px;
        height: 115px;
        margin-right: 35px;
        vertical-align: middle;
    }

    .cart_item .column_3 {
        width: 197px;
        position: relative;
        padding-left: 10px;
    }

    .my_el_select {
        width: 117px;
        height: 28px;
        position: absolute;
        top: 0;
        bottom: 0;
        margin: auto;
    }

    .cart_item .column_4 {
        padding: 67px 10px;
        height: 116px;
        width: 142px;
        line-height: 116px;
    }

</style>
