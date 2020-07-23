import xadmin
from user.models import Order

from user.models import OrderDetail, UserCourse


class OrderModelAdmin(object):
    """订单模型管理"""
    pass


xadmin.site.register(Order, OrderModelAdmin)


class OrderDetailModelAdmin(object):
    """订单详情模型管理类"""
    pass


xadmin.site.register(OrderDetail, OrderDetailModelAdmin)


class UserCourseModelAdmin(object):
    """用户的课程购买记录"""
    pass


xadmin.site.register(UserCourse, UserCourseModelAdmin)
