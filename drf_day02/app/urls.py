

from django.urls import path
from app import views

urlpatterns = [
    path("user/<str:pk>/",views.EmployeeAPIView.as_view()),
    path("user/",views.EmployeeAPIView.as_view())
]
