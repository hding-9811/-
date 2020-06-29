

from django.urls import path,include
from stu import views

urlpatterns = [
    path("stu/<str:id>/",views.StudentAPIView.as_view()),
    path("stu/",views.StudentAPIView.as_view())

]
