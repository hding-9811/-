<template>
    <div class="course">
        <Header></Header>
        <div class="main">
            <!-- 筛选条件 -->
            <div class="condition">
                <ul class="cate-list">
                    <li class="title">课程分类:</li>
                    <li @click="category=0" :class="category==0?'this':''">全部</li>
                    <li v-for="cate in category_list" @click="category=cate.id" :class="category==cate.id?'this':''">
                        {{cate.name}}
                    </li>
                    <!--                    <li class="this">全部</li>-->
                    <!--                    <li>Python全栈</li>-->
                    <!--                    <li>Java进阶</li>-->
                    <!--                    <li>Php编程</li>-->
                    <!--                    <li>开发工具</li>-->
                    <!--                    <li>GoLang</li>-->
                    <!--                    <li>大数据训练营</li>-->
                    <!--                    <li>知识论坛</li>-->
                </ul>

                <div class="ordering">
                    <ul>
                        <li class="title">筛&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;选:</li>
                        <li class="default this" @click="change_order_type('id')" :class="change_order_class('id')">默认
                        </li>
                        <li class="hot this" @click="change_order_type('students')"
                            :class="change_order_class('students')">人气
                        </li>
                        <li class="price this" @click="change_order_type('price')" :class="change_order_class('price')">
                            价格
                        </li>
                    </ul>
                    <p class="condition-result">共21个课程</p>
                </div>

            </div>
            <!-- 课程列表 -->
            <div class="course-list">
                <div class="course-item" v-for="course in course_list">
                    <div class="course-image">

                        <a href="javascript:void (0)" @click="redirect(course.id)"> <img src=static/image/03.png alt=""></a>
                    </div>
                    <div class="course-info">
                        <!--                        <router-link :to="/course/detail/">{{course.name}}</router-link>-->
                        <a href="javascript:void (0)" @click="redirect(course.id)"> {{course.name}}</a>
                        <h3>{{course.name}} <span><img src="" alt="">{{course.students}}人已加入学习</span></h3>
                        <p class="teather-info">huxz 百知教育教学总监 <span>共{{course.lessons}}课时/{{course.lessons==course.pub_lessons?'更新完成':`已更新${course.pub_lessons}课时`}}</span>
                        </p>
                        <ul class="lesson-list">
                            <li v-for="(lesson,key) in course.lesson_list" :key="key">
                                <span class="lesson-title">
                                {{key+1}} | 第{{key+1}}节：{{lesson.name}}
                                </span> <span class="free" v-if="lesson.free_trail">免费</span></li>

                        </ul>
                        <div class="pay-box">
                            <span class="discount-type">{{course.discount_name}}</span>
                            <span class="discount-price" v-if="course.real_price != course.price">￥{{course.real_price}}元</span>
                            <span class="original-price">原价：{{course.price}}元</span>
                            <span class="buy-now">立即购买</span>
                        </div>
                    </div>
                </div>

            </div>
        </div>
        <el-pagination
            background
            layout="prev, pager, next, sizes"
            :page-size="filters.size"
            :page-sizes="[2, 3, 5, 10]"
            @current-change="change_page"
            @size-change="size_change"
            :total="total">
        </el-pagination>

        <Footer></Footer>
    </div>
</template>

<script>
    export default {
        name: "Course",
        data() {
            return {
                category_list: [],  // 分类列表
                course_list: [],     //  课程列表
                category: 0,
                total: 0,   //  课程总数量
                // course_category: "",    // 分类id
                // 对数据进行过滤
                filters: {
                    type: "id", // 筛选类型
                    orders: "desc", // 排序类型  desc降序 asc  升序
                    page: 1, // 分页的页码
                    size: 2,    // 每页展示的数量
                },
            }
        },
        // 用于监听页面上某个值发生改变时做对应的操作
        watch: {
            // 监听category是否发生了改变  一旦发生改变说明用户要查看另一个分类的课程
            category() {
                // 重新查询课程
                this.get_course_list();
            },
        },
        methods: {
            // 获取所有课程的信息
            get_course_list() {
                // 如果根据过滤条件进行分页  则需要重新指定分页的值
                let filters = {
                    // 切换分页后的页码
                    page: this.filters.page,
                    size: this.filters.size,
                };

                // 完成排序
                if (this.filters.orders === "desc") {
                    filters.ordering = "-" + this.filters.type;
                } else {
                    filters.ordering = this.filters.type;
                }

                // 判断是否要根据分类id'查询对应的课程
                if (this.category > 0) {
                    filters.course_category = this.category;
                }
                console.log(this.category);
                this.$axios.get(`${this.$settings.HOST}course/list_filter/`, {
                    params: filters
                }).then(response => {
                    console.log(response.data);
                    // 分页之前的
                    // this.course_list = response.data;
                    this.course_list = response.data.results;
                    // 分页总数量
                    this.total = response.data.count;
                }).catch(error => {
                    console.log(error.response);
                })
            },
            // 获取所有分类信息
            get_all_category() {
                this.$axios.get(`${this.$settings.HOST}course/category/`).then(response => {
                    this.category_list = response.data;
                })
            },
            // 改变排序的条件
            change_order_type(type) {
                console.log(type);
                // 通过click事件更改排序的条件
                if (this.filters.type === type && this.filters.orders === "asc") {
                    this.filters.orders = 'desc';
                } else if (this.filters.type === type && this.filters.orders === "desc") {
                    this.filters.orders = 'asc';
                }
                // 更改排序方式
                this.filters.type = type;
                // 重新获取排序的结果
                this.get_course_list();

            },
            // 控制高亮效果
            change_order_class(type) {
                // 更改选中的高亮效果
                if (this.filters.type === type && this.filters.orders === "asc") {
                    return "this asc";
                } else if (this.filters.type === type && this.filters.orders === "desc") {
                    return "this desc";
                } else {
                    return "";
                }
            },

            // 分页
            change_page(page) {
                this.filters.page = page;
                this.get_course_list();
            },

            // 改变每页展示的课程数量
            size_change(size) {
                this.filters.size = size;
                // 改变每页展示的数量后必须重置页面
                this.filters.page = 1;
                this.get_course_list();
            },

            // 跳转页面
            redirect(id) {
                this.$router.push({
                    path: "/course/detail",
                    query: {
                        id: id
                    }
                })


            },

        },
        created() {
            this.get_all_category();
            this.get_course_list();
        }
    }
</script>

<style scoped>
    .course {
        background: #f6f6f6;
    }

    .course .main {
        width: 1100px;
        margin: 35px auto 0;
    }

    .course .condition {
        margin-bottom: 35px;
        padding: 25px 30px 25px 20px;
        background: #fff;
        border-radius: 4px;
        box-shadow: 0 2px 4px 0 #f0f0f0;
    }

    .course .cate-list {
        border-bottom: 1px solid #333;
        border-bottom-color: rgba(51, 51, 51, .05);
        padding-bottom: 18px;
        margin-bottom: 17px;
    }

    .course .cate-list::after {
        content: "";
        display: block;
        clear: both;
    }

    .course .cate-list li {
        float: left;
        font-size: 16px;
        padding: 6px 15px;
        line-height: 16px;
        margin-left: 14px;
        position: relative;
        transition: all .3s ease;
        cursor: pointer;
        color: #4a4a4a;
        border: 1px solid transparent; /* transparent 透明 */
    }

    .course .cate-list .title {
        color: #888;
        margin-left: 0;
        letter-spacing: .36px;
        padding: 0;
        line-height: 28px;
    }

    .course .cate-list .this {
        color: #ffc210;
        border: 1px solid #ffc210 !important;
        border-radius: 30px;
    }

    .course .ordering::after {
        content: "";
        display: block;
        clear: both;
    }

    .course .ordering ul {
        float: left;
    }

    .course .ordering ul::after {
        content: "";
        display: block;
        clear: both;
    }

    .course .ordering .condition-result {
        float: right;
        font-size: 14px;
        color: #9b9b9b;
        line-height: 28px;
    }

    .course .ordering ul li {
        float: left;
        padding: 6px 15px;
        line-height: 16px;
        margin-left: 14px;
        position: relative;
        transition: all .3s ease;
        cursor: pointer;
        color: #4a4a4a;
    }

    .course .ordering .title {
        font-size: 16px;
        color: #888;
        letter-spacing: .36px;
        margin-left: 0;
        padding: 0;
        line-height: 28px;
    }

    .course .ordering .this {
        color: #ffc210;
    }

    .course .ordering .price {
        position: relative;
    }

    .course .ordering .price::before,
    .course .ordering .price::after {
        cursor: pointer;
        content: "";
        display: block;
        width: 0px;
        height: 0px;
        border: 5px solid transparent;
        position: absolute;
        right: 0;
    }

    .course .ordering .price::before {
        border-bottom: 5px solid #aaa;
        margin-bottom: 2px;
        top: 2px;
    }

    .course .ordering .price::after {
        border-top: 5px solid #aaa;
        bottom: 2px;
    }

    .course .course-item:hover {
        box-shadow: 4px 6px 16px rgba(0, 0, 0, .5);
    }

    .course .course-item {
        width: 1050px;
        background: #fff;
        padding: 20px 30px 20px 20px;
        margin-bottom: 35px;
        border-radius: 2px;
        cursor: pointer;
        box-shadow: 2px 3px 16px rgba(0, 0, 0, .1);
        /* css3.0 过渡动画 hover 事件操作 */
        transition: all .2s ease;
    }

    .course .course-item::after {
        content: "";
        display: block;
        clear: both;
    }

    /* 顶级元素 父级元素  当前元素{} */
    .course .course-item .course-image {
        float: left;
        width: 423px;
        height: 210px;
        margin-right: 30px;
    }

    .course .course-item .course-image img {
        width: 100%;
    }

    .course .course-item .course-info {
        float: left;
        width: 596px;
    }

    .course-item .course-info h3 {
        font-size: 26px;
        color: #333;
        font-weight: normal;
        margin-bottom: 8px;
    }

    .course-item .course-info h3 span {
        font-size: 14px;
        color: #9b9b9b;
        float: right;
        margin-top: 14px;
    }

    .course-item .course-info h3 span img {
        width: 11px;
        height: auto;
        margin-right: 7px;
    }

    .course-item .course-info .teather-info {
        font-size: 14px;
        color: #9b9b9b;
        margin-bottom: 14px;
        padding-bottom: 14px;
        border-bottom: 1px solid #333;
        border-bottom-color: rgba(51, 51, 51, .05);
    }

    .course-item .course-info .teather-info span {
        float: right;
    }

    .course-item .lesson-list::after {
        content: "";
        display: block;
        clear: both;
    }

    .course-item .lesson-list li {
        float: left;
        width: 44%;
        font-size: 14px;
        color: #666;
        padding-left: 22px;
        /* background: url("路径") 是否平铺 x轴位置 y轴位置 */
        background: url("/static/image/play-icon-gray.svg") no-repeat left 4px;
        margin-bottom: 15px;
    }

    .course-item .lesson-list li .lesson-title {
        /* 以下3句，文本内容过多，会自动隐藏，并显示省略符号 */
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        display: inline-block;
        max-width: 200px;
    }

    .course-item .lesson-list li:hover {
        background-image: url("/static/image/play-icon-yellow.svg");
        color: #ffc210;
    }

    .course-item .lesson-list li .free {
        width: 34px;
        height: 20px;
        color: #fd7b4d;
        vertical-align: super;
        margin-left: 10px;
        border: 1px solid #fd7b4d;
        border-radius: 2px;
        text-align: center;
        font-size: 13px;
        white-space: nowrap;
    }

    .course-item .lesson-list li:hover .free {
        color: #ffc210;
        border-color: #ffc210;
    }

    .course-item .pay-box::after {
        content: "";
        display: block;
        clear: both;
    }

    .course-item .pay-box .discount-type {
        padding: 6px 10px;
        font-size: 16px;
        color: #fff;
        text-align: center;
        margin-right: 8px;
        background: #fa6240;
        border: 1px solid #fa6240;
        border-radius: 10px 0 10px 0;
        float: left;
    }

    .course-item .pay-box .discount-price {
        font-size: 24px;
        color: #fa6240;
        float: left;
    }

    .course-item .pay-box .original-price {
        text-decoration: line-through;
        font-size: 14px;
        color: #9b9b9b;
        margin-left: 10px;
        float: left;
        margin-top: 10px;
    }

    .course-item .pay-box .buy-now {
        width: 120px;
        height: 38px;
        background: transparent;
        color: #fa6240;
        font-size: 16px;
        border: 1px solid #fd7b4d;
        border-radius: 3px;
        transition: all .2s ease-in-out;
        float: right;
        text-align: center;
        line-height: 38px;
    }

    .course-item .pay-box .buy-now:hover {
        color: #fff;
        background: #ffc210;
        border: 1px solid #ffc210;
    }

    .el-pagination {
        text-align: center;
        padding-top: 20px;
        padding-bottom: 50px;
    }
</style>
