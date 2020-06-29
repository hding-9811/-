from rest_framework import serializers


# 定义序列化器类 跟模型moles对应的
from app.models import Employee
from drf_day02 import settings


# 序列化器

class EmployeeSerializer(serializers.Serializer):
    """
    需要为每个model编写一个单独的序列化器类
    根据指定的字段名去模型中匹配并一一序列化
    """
    username = serializers.CharField()
    password = serializers.CharField()
    # gender = serializers.IntegerField()
    # pic = serializers.ImageField()

    # 自定义字段  返回盐 使用SerializerMethodField来定义
    salt = serializers.SerializerMethodField()

    # 自定义段的属性名随意 但为字段提供的方法名必须是get_字段名
    # get_字段名：是为自定义的字段提供的方法 self是参与序列化的模型
    # 方法的返回值就是当前字段返回到的返回值

    def get_salt(self, obj):
        return "salt"

    # 自定义性别的返回值
    gender = serializers.SerializerMethodField()

    def get_gender(self, obj):
        return "{}{}{}".format("http://127.0.0.1:8000", settings.MEDIA_URL, str(obj.pic))
