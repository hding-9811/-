from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.settings import APISettings
from app.models import Employee
from .serializers import EmployeeSerializer
from rest_framework.response import Response


# Create your views here.

class EmployeeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        if user_id:
            # 查询单个
            emp_obj = Employee.objects.get(pk=user_id)
            # 查询出的单个员工对象无法直接序列化，需要使用序列化器完成
            # .data 将序列化器的数据打包成字典

            emp_ser = EmployeeSerializer(emp_obj)
            data = emp_ser.data
            return Response({
                "status": 200,
                "msg": "查询单个员工成功",
                "results": data
            })
        else:
            # 查询所有
            # 员工对象无法直接序列化返回到前台
            emp_list = Employee.objects.all()

            # TODO 使用序列化器完成多个员工序列化 需要指定 many=True
            emp_list_ser = EmployeeSerializer(emp_list, many=True).data

            return Response({
                "status": 200,
                "msg": "查询所有员工成功",
                "results": emp_list_ser
            })

    def post(self, request, *args, **kwargs):

        """
        新增单个对象

        """
        user_data = request.data

        # TODO 前端发送的数据需要入库时必须对前台的数据进行校验
        if not isinstance(user_data,dict) or user_data == {}:
            return Response({
                "status": 501,
                "msg":"数据有误"
            })
