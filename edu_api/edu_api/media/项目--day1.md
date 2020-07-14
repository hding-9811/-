# 项目--day1

## 1. 项目概念

### web项目类型

~~~markdown
1. 商城
	B2C bussiness to customer  企业直接对个人
	C2C customer to customer 个人对个人  二手交易平台
	B2B 企业对企业
	O2O online to  offline  线上对线下
2. 社交网站
3. 资讯论坛
4. 门户网站
5. 企业内部系统
6. 个人博客
~~~

### 企业项目开发流程

![](项目--day1.assets/image-20200708102432090.png)

## 2. 需求分析

~~~markdown
1. 首页
2. 用户模块
	登录 注册 注销
3. 课程模块
	课程列表 课程详情
4. 购物车
	商品添加  展示购物车列表  变更购物车
5. 订单模块
6. 个人中心
~~~

## 3. DRF环境搭建

### 项目创建

- 项目目录结构

~~~markdown
baizhi/
  ├── docs/          # 项目相关资料保存目录
  ├── edu_client/     # 前端项目目录
  ├── edu_api/      # 后端项目目录
       ├── logs/          # 项目运行时/开发时日志目录
       ├── manage.py
       ├── edu_api/      # 项目主应用，开发时的代码保存
       │    ├── apps/      # 开发者的代码保存目录，以模块[子应用]为目录保存
       │    ├── libs/      # 第三方类库的保存目录[第三方组件、模块]
       │    ├── settings/
       │         ├── develope.py   # 项目开发时的本地配置
       │         ├── production.py  # 项目上线时的运行配置
       │    ├── urls.py    # 总路由
       │    ├── utils/     # 多个模块[子应用]的公共函数类库[自己开发的组件]
~~~

![](项目--day1.assets/image-20200708111701541.png)

![](项目--day1.assets/image-20200708112448217.png)

### 项目日志配置

> 在项目运行过程中，可能会产生各种错误信息，为了方便记录项目在运行过程中所发生的问题，可以使用logging将所发生的日志记录记录到文件中

~~~python
# 项目的日志配置
LOGGING = {
    # 版本
    'version': 1,
    # 是否禁用已存在的日志器
    'disable_existing_loggers': False,
    # 格式化日志信息
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    # 日志的过滤信息
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理日志的方法
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            # 记录到文件中的日志等级
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置  日志的文件名  日志的保存目录
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/lesson_api.log"),
            # 日志文件的大小  100M
            'maxBytes': 100 * 1024 * 1024,
            # 日志文件的最大数量
            'backupCount': 10,
            # 日志的格式
            'formatter': 'verbose'
        },
    },
    # 日志对象，与django集成使用
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}
~~~

### 全局异常处理

~~~python
import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status

logger = logging.getLogger("django")


def exception_handler(exc, context):
    # 详细错误信息的定义
    error = "%s %s %s" % (context['view'], context['request'].method, exc)

    # 先让DRF处理异常 根据异常的返回值可以判断异常是否被处理
    response = drf_exception_handler(exc, context)
    # 如果返回值为None，代表DRF无法处理此时发生的异常  需要自定义处理
    if response is None:
        logger.error(error)
        return Response(
            {"error_msg": "程序内部错误，请稍等一会儿~"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=None)
        # return Response({"error_msg": error})

    # 如果Response不为空  说明异常信息已经被DRF处理了 直接返回即可
    return response

~~~

## 4. Vue-cli项目搭建

### 项目创建

~~~js
1. 创建项目安装对应的依赖

2. 配置项目
// axios配置
import axios from "axios";

Vue.prototype.$axios = axios;

//element-ui
import Element from "element-ui"
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(Element);
~~~

### 域名配置

> vi hosts
>
> 127.0.0.1 api.baizhishop.com  后台  allow_host
>
> 127.0.0.1 www.baizhishop.com  前台   config/index.js

~~~python
# 自定义settings
export default {
    "HOST": "http://api.baizhishop.com:9001/"
}
# main.js  自定义配置生效
import settings from "./settings";
Vue.prototype.$settings = settings;

# DRFsettings文件  后台
ALLOWED_HOSTS = [
    # 以后可以将域名换成真实的
    'api.baizhishop.com',
    'www.baizhishop.com',
]
~~~

## 5. 后台应用

- apps目录设置

> 在`apps`目录下创建子应用，以后应用都将存入此目录。
>
> 切换至apps目录下执行创建命令：`python ../../manage.py startapp home`

~~~python
# 修改默认的子应用的目录后，需要将apps 目录设置为全局的导包路径
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# 右键apps-->make directory as-->source root
~~~

- 跨域请求

~~~python
INSTALLED_APPS = [
	...
    'corsheaders',
]

'corsheaders.middleware.CorsMiddleware',

# 允许跨域请求
CORS_ORIGIN_ALLOW_ALL = True
~~~

## 6. 首页

### 轮播图

- 模型

~~~python
from django.db import models


class Banner(models.Model):
    """轮播图模型"""
    img = models.ImageField(upload_to="banner", max_length=255, verbose_name="轮播图图片")
    title = models.CharField(max_length=200, verbose_name="轮播图标题")
    link = models.CharField(max_length=300, verbose_name="图片链接")
    is_show = models.BooleanField(default=False, verbose_name="是否显示图片")
    orders = models.IntegerField(default=1, verbose_name="图片排序")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = "bz_banner"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

~~~

### Xadmin后台

> `pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2`

~~~python
# 安装
pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2

INSTALLED_APPS = [

    # x admin配置
    'xadmin',
    'crispy_forms',
    'reversion',

]

# 根路由
import xadmin
from xadmin.plugins import xversion

xversion.register_models()

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
]

# xadmin创建完成后需要迁移
python manage.py makemigrations
python manage.py migrate
~~~

- xadmin

~~~python
import xadmin
from xadmin import views


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "百知教育"  # 设置站点标题
    site_footer = "北京百知教育科技有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)

# 将banner注册到后台  列表显示的字段
class BannerInfo(object):
    list_display = ["title", "orders", "is_show"]


xadmin.site.register(Banner, BannerInfo)
~~~

# 任务：

~~~markdown
1. 完成前后台搭建与配置
2. 完成轮播图与导航栏信息的展示
~~~

