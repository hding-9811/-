

from django.urls import path,include
from app2 import views

urlpatterns = [
  path("book/<str:id>/",views.BookAPIView.as_view()),
  path("book/",views.BookAPIView.as_view()),
  path("book2/<str:id>/",views.BookGenericAPIView.as_view()),
  path("user/",views.UserGenericViewSet.as_view({
    "get":"user_login",
  })),
  path("book2/",views.BookGenericAPIView.as_view()),



]
