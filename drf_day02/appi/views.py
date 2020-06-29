from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView
from appi.models import User


class UserAPIView(APIView):

    def get(self,request,*args,**kwargs):
        user_id = kwargs.get("pk")
        user_cal = User.objects.get(id=user_id)

        return Response("DRF GET SUCCESS")

    def post(self,request,*args,**kwargs):
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        user = User.objects.create(username=username,password=pwd)
        if user:
            return Response("POST GET SUCCESS")