from django.db import transaction
from rest_framework import serializers
from datetime import datetime
from django_redis import get_redis_connection
from course.models import Course, CourseExpire
from user.models import Order, OrderDetail


class OrderModelSerializer(serializers.ModelSerializer):
    """
    订单模型序列化器
    """

    class Meta:
        model = Order
        fields = ["id", "order_number", "pay_type"]

        extra_kwargs = {
            "id": {"read_only": True},
            "order_number": {"read_only": True},
            "pay_type": {"write_only": True},

        }

    def validate(self, attrs):
        """对数据进行验证"""
        pay_type = attrs.get("pay_type")
        try:
            Order.pay_choices[pay_type]
        except Order.DoesNotExist:
            raise serializers.ValidationError("你当前选择的支付方式不允许")
        return attrs

    def create(self, validated_data):
        """生成 订单 与订单详情"""

        redis_connection = get_redis_connection("cart")
        # 通过context获取到request对象
        user_id = self.context["request"].user.id

        #  生成唯一订单 时间戳 用户id 随机字符串
        incr = redis_connection.incr("order")

        order_number = datetime.now().strftime("%Y%m%d%H%S") + "%06d" % user_id + "%06d" % incr

        with transaction.atomic():

            # 记录事务回滚的点
            rollback_id = transaction.savepoint()

            try:
                order = Order.objects.create(order_title="百知教育视频课订单", total_price=0, real_price=0,
                                             order_number=order_number, pay_type=validated_data.get("pay_type"),
                                             order_status=0, credit=0, coupon=0, order_desc="买它",
                                             user_id=user_id
                                             )
            except Order.DoesNotExist:
                transaction.savepoint_rollback(rollback_id)

            # 生成订单详情
            # 从购物车获取所有已勾选的商品
            cart_list = redis_connection.hgetall("cart_%s" % user_id)
            select_list = redis_connection.smembers("selected_%s" % user_id)

            for course_id_byte, expire_id_byte in cart_list.items():
                course_id = int(course_id_byte)
                expire_id = int(expire_id_byte)

                # 判断商品id是否在已勾选的列表中
                if course_id_byte in select_list:

                    try:
                        # 获取 到所有课程的信息
                        course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                        original_price = course.price
                    except Course.DoesNotExist:

                        transaction.savepoint_rollback(rollback_id)
                        return serializers.ValidationError("对不起，当前商品不存在")

                    try:
                        # 如果有效期的id 大于0 则需要计算商品价格 id不大于0 则代表永久有效
                        if expire_id > 0:
                            course_expire = CourseExpire.objects.get(id=expire_id)
                            # 对应有效期的价格
                            original_price = course_expire.price


                    except CourseExpire.DoesNotExist:
                        pass

                    # 计算总价
                    real_expire_price = course.real_expire_price(expire_id)


                    try:
                        # 生成订单详情
                        OrderDetail.objects.create(
                            order=order,
                            course=course,
                            expire=expire_id,
                            price=original_price,
                            real_price=real_expire_price,
                            discount_name=course.discount_name,
                        )
                    except:
                        transaction.savepoint_rollback(rollback_id)
                        raise serializers.ValidationError("订单生成失败")

                    # 计算订单的总价
                    order.total_price += float(original_price)
                    order.real_price += float(real_expire_price)
                    try:
                        redis_connection.hdel("cart_%s" % user_id, course.id)
                    except:
                        transaction.savepoint_rollback(rollback_id)
            order.save()

        return order
