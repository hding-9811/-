from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from stu.models import Student
from stu.serializers import StuDeSerializer, StuSerializer



class StudentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        if id:
            stu_obj = Student.objects.get(pk=id)
            data = StuSerializer(stu_obj).data
            if stu_obj:
                return Response({
                    "status": 200,
                    "msg": "查询单个学生成功",
                    "results": data
                })
        else:
            stu_obj = Student.objects.all()
            stu_list = StuSerializer(stu_obj,many=True).data
            return Response({
                "status": 200,
                "msg": "查询所有学生成功",
                "results": stu_list
            })

    def post(self, request, *args, **kwargs):
        user_data = request.data
        if not isinstance(user_data, dict) or user_data == {}:
            return Response({
                "status": 501,
                "msg": "数据有误"

            })

        serializer = StuDeSerializer(data=user_data)
        if serializer.is_valid():
            stu_obj = serializer.save()
            return Response({
                "status": 201,
                "msg": "学生添加成功",
                "results": StuSerializer(stu_obj).data
            })
        else:
            return Response({
                "status": 501,
                "msg": "用户创建失败",
                # 验证失败后错误信息包含在 .errors中
                "results": serializer.errors
            })
