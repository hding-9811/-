from django.db import transaction
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from order import serialiser

from user.models import Order


class OrderAPIView(CreateAPIView):
    """生成订单的视图"""
    queryset = Order.objects.filter(is_show=True, is_delete=False)
    serializer_class = serialiser.OrderModelSerializer


