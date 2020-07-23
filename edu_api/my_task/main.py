import os
import django

from celery import Celery

# 主程序

# 创建selery实例对象
app = Celery("edu")

# 把celery和django进行结合，识别并加载django的配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE","edu_api.settings.develop")
django.setup()

# 通过创建的实例对象加载配置
app.config_from_object("my_task.config")

# 将添加任务到实例对象中 自动找到该目录下的tasks文件中的任务

app.autodiscover_tasks(["my_task.sms","my_task.file","my_task.change_order"])
