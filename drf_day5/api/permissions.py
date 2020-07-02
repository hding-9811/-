from rest_framework.permissions import BasePermission

from api.models import User


class MyPermission(BasePermission):
    """
    有权访问返回True
    无权访问返回False
    登录可写 ， 游客只读
    """

    def has_permission(self, request, view):
        # 如果是只读接口则所有人都可以访问
        if request.method in ["GET", 'HEAD', 'OPTIONS']:
            return True

        username = request.data.get("username")
        user = User.objects.filter(username=username).first()
        print(user)

        if user:
            return True
        return False
