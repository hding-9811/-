from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from edu_api.settings import constants
import logging

from course.models import Course, CourseExpire

log = logging.getLogger('django')


class CartView(ViewSet):
    """ 购物车相关的处理"""

    # //只有登录且认证成功的用户才可以访问此接口
    # permission_classes = [IsAuthenticated]

    def add_cart(self, request, *args, **kwargs):
        """
        将用户提交的信息提交到购物车
        :param request:  用户id  课程id  勾选状态 有效期
        :param args:
        :param kwargs:
        :return:
        """
        course_id = request.data.get("course_id")
        user_id = request.user.id
        print(user_id)
        # 是否勾选
        select = True
        # 有效期
        expire = 0

        # 校验前端提交的参数
        try:
            Course.objects.get(is_show=True, id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，课程保存失败"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # 获取到redis
            redis_connection = get_redis_connection("cart")

            # 将 数据保存到redis
            pipeline = redis_connection.pipeline()
            # 管道开启
            pipeline.multi()

            # 商品信息极对应的有效期
            pipeline.hset('cart_%s' % user_id, course_id, expire)
            # 被勾选的商品
            pipeline.sadd('selected_%s' % user_id, course_id)
            course_len = redis_connection.hlen("cart_%s" % user_id)
            print(course_len)

            # 执行
            pipeline.execute()
        except:
            log.error("购物车数据储存失败")
            return Response({"message": "参数有误，购物车保存失败"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "购物车商品添加成功", "cart_length": course_len})

    def list_cart(self, request, *args, **kwargs):
        """展示购物车"""
        user_id = request.user.id
        # user_id = 2
        redis_connection = get_redis_connection("cart")
        cart_list = redis_connection.hgetall("cart_%s" % user_id)
        select_list = redis_connection.smembers('selected_%s' % user_id)
        print('cart_list', cart_list)
        print(select_list, "sele")

        # 循环从mysql中找出商品的信息
        data = []
        for course_id, expire_id in cart_list.items():
            course_id = int(course_id)
            expire_id = int(expire_id)
            try:
                # 获取到所有的课程信息
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            # 将购物车所需要的信息返回
            data.append({
                'selected': True if course_id in select_list else False,
                "course_img": constants.IMAGE_SRC + course.course_img.url,
                "name": course.name,
                "expire_id": expire_id,
                "price": course.price,
                "id": course.id,
                # 购物车列表需要课程有效期
                "expire_list": course.expire_list,
                # 获取真实价格
                "real_price": course.real_expire_price(expire_id),

            })

        return Response(data)

    def change_select(self, request):
        """切换购物车商品的状态"""
        user_id = request.user.id
        selected = request.data.get("selected")
        # selected = request.data.get("selected")

        course_id = request.data.get("course_id")
        print(course_id)
        try:
            Course.objects.get(is_show=True, is_delete=False, id=course_id)
        except:
            return Response({"message": "参数有误，当前商品不存在"}, status=status.HTTP_402_PAYMENT_REQUIRED)

        redis_connection = get_redis_connection("cart")
        if selected:
            redis_connection.sadd('selected_%s' % user_id, course_id)
        else:
            redis_connection.srem("selected_%s" % user_id, course_id)

        return Response({"message": "状态切换成功"})

    def delete_course(self, request):
        user_id = request.user.id
        # selected = request.data.get("selected")
        course_id = request.data.get('course_id')
        print(course_id, user_id)
        try:
            Course.objects.get(is_show=True, is_delete=False, id=course_id)
        except:
            return Response({"message": "删除失败"}, status=status.HTTP_400_BAD_REQUEST)

        redis_connection = get_redis_connection('cart')

        if course_id:
            redis_connection.hdel("cart_%s" % user_id, course_id)

        # return Response({"message":"删除失败"},status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "删除成功"}, status=status.HTTP_200_OK)

    def change_expire(self, request):

        """改变redis课程的有效期"""

        user_id = request.user.id
        expire_id = request.data.get("expire_id")
        course_id = request.data.get("course_id")
        print(expire_id,course_id)

        try:
            course = Course.objects.get(is_show=True,is_delete=False,id=course_id)
            if expire_id > 0:
                expire_iem = CourseExpire.objects.get(is_show=True, is_delete=False, id=expire_id)
                if not expire_iem:
                    raise Course.DoesNotExist()
        except Course.DoesNotExist:
            return Response({"message": "课程信息不存在"}, status=status.HTTP_400_BAD_REQUEST)
        connection = get_redis_connection("cart")
        connection.hset("cart_%s" % user_id, course_id, expire_id)

        # 重新计算切换后的价钱

        real_price = course.real_expire_price(expire_id)

        return Response({"message":"切换有效期成功","real_price":real_price})
