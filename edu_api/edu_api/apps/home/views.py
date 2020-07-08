from rest_framework.generics import ListAPIView

from home.models import Banner, Nav
from home.serializers import BannerModelSerializer,NavModelSerializer


# Create your views here.

class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_delete=False)
    serializer_class = BannerModelSerializer


class NavListerAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True,is_delete=False)
    serializer_class = NavModelSerializer
