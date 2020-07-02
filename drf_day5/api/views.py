from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from api.models import User
from api.thorttle import SendMessageRate
from utils.response import APIResponse
from django.contrib.auth.models import Group, Permission

from api.authentication import MyAuth
from api.permissions import MyPermission


# Create your views here.


class TestAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        # 查询用户
        user = User.objects.first()
        # 根据用户获取对应的角色
        print(user.groups.first())

        # 通过角色获取对应的权限
        print(user.user_permissions.first().name)
        """
        """
        group = Group.objects.first()
        # 通过角色获取对应的权限
        print(group.permissions.first().name)

        # 通过角色获取对应的用户
        print(group.user_set.first().username)
        """

        # 获取权限
        permission = Permission.objects.filter(pk=9).first()
        # 根据权限获取用户
        print(permission.user_set.first().username)
        # 根据权限获取角色
        per = Permission.objects.filter(pk=13).first()
        print(per.group_set.first().name)

        return APIResponse('ok')


class TestPermissionAPIView(APIView):
    """
    只有认证后才可以访问
    """
    authentication_classes = [MyAuth]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return APIResponse("登陆访问成功")


class UserLoginOrReadOnly(APIView):
    """
    登录可写 游客只读
    """

    permission_classes = [MyPermission]

    def get(self, request, *args, **kwargs):
        return APIResponse("读操作访问成功")

    def post(self, request, *args, **kwargs):
        return APIResponse("写操作")


class SendMessageAPIView(APIView):
    throttle_classes = [SendMessageRate]

    def get(self, request, *args, **kwargs):
        return APIResponse("读操作访问成功")

    def post(self, request, *args, **kwargs):
        return APIResponse("写操作")
