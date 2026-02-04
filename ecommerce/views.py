from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate

# Create your views here.
class LoginView(APIView):
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get('password')
        if not username or password:
            authenticate(username=username,password=password)
            return Response({"message":"Authenticate successful"})
        return Response({"message":f"error {e} "})

