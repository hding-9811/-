from django.urls import path
from payments import views

urlpatterns = [
    path("all_pay/",views.AliPayAPIView.as_view()),
    path("result/",views.AliPayResultAPIView.as_view())

]