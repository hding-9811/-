from django.shortcuts import render
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from api.pagination import MyPageNumberPaginarion, MyLimitPagination
from api.filter import ComputerFilterSet

from api.serializer import ComputerModelSerializer

# Create your views here.
from api.models import Computer


# 游标分页

class ComputerListAPIView(ListAPIView):
    queryset = Computer.objects.all()
    serializer_class = ComputerModelSerializer
    # 通过此参数配置过滤器类
    filter_backends = [SearchFilter, OrderingFilter]
    # 指定搜索条件
    # search_fields = ["name", "price"]
    # 指定排序条件
    ordering = ["price"]

    # 指定分页器
    # pagination_class = MyPageNumberPaginarion
    # pagination_class = MyLimitPagination

    filter_class = ComputerFilterSet
