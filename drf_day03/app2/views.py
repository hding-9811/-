from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from app.models import Book
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework import generics
from rest_framework import viewsets
from app2.models import User

from .serializers import BookModelSerializer, UserSerializers
from utils.response import APIResponse


class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        book_list = Book.objects.filter(is_delete=False)
        data_ser = BookModelSerializer(book_list, many=True).data

        return APIResponse(results=data_ser)


# GenericAPIView继承了APIView,两者完全兼容

class BookGenericAPIView(GenericAPIView,
                         ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin):
    # 获取当前视图所操作的模型宇序列化器
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    # 指定获取单挑信息的主键名称
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        # 获取book模型的所有数据
        book_list = self.get_queryset()
        # 获取要使用的序列化器
        data_ter = self.get_serializer(book_list, many=True, context={"request": request})
        # 获取序列化后的数据
        data = data_ter.data

        return APIResponse(results=data)

    def get(self, request, *args, **kwargs):
        book_obj = self.get_object()
        data_ser = self.get_serializer(book_obj)
        data = data_ser.data
        return APIResponse(results=data)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(results=response.data)

        # 单局部改

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)
        # 通过继承DestroyModelMixin 获取self

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return APIResponse(http_status=status.HTTP_204_NO_CONTENT)


class UserGenericViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    print(queryset)
    serializer_class = UserSerializers

    def user_login(self, request, *args, **kwargs):
        username = request.params.get('username')
        pwd = request.params.get('pwd')
        print(username, pwd)
        user = User.objects.filter(username=username, password=pwd)
        if user:
            return APIResponse(data_message='登陆成功')

        else:
            return APIResponse(data_message="登陆失败")

    def post(self, request, *args, **kwargs):

        return APIResponse(data_message="注册成功")
