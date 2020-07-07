
from django.urls import path
from api import views

urlpatterns = [
    path("list/",views.ComputerListAPIView.as_view()),

]
