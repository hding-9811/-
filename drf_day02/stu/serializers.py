from rest_framework import serializers

from stu.models import Student


# 序列化器
class StuSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    # gender = serializers.IntegerField()
    num = serializers.IntegerField()

    # 自定义返回性别
    gender = serializers.SerializerMethodField()

    def get_gender(self, obj):

        return obj.get_gender_display()


# 反序列化器

class StuDeSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=8,
        min_length=4,
        error_messages={
            "max_length": "长度太长了",
            "min_length": "长度太短了",
        }
    )
    age = serializers.IntegerField()
    gender = serializers.IntegerField()
    num = serializers.IntegerField()

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
