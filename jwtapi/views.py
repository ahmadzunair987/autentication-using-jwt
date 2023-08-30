from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializers, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer
from django.contrib.auth import authenticate, login
from jwtapi.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegisteration(APIView):
    def post(self, request):
        serializer = UserSerializers(data= request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response ({'token' : token, 'msg' : 'Registeration Successful'})
        return Response ({'msg' : 'Registeration is not Successful'})

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data= request.data)
        if serializer.is_valid(raise_exception = True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(request, email=email, password = password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'token' : token, 'msg' : 'login Success'}, status=status.HTTP_200_OK)
                # login(request, user)
            else:
                return Response ({'error' : {'non_field_errors' : ['Invalid Email OR Password']}},
                 status=status.HTTP_404_NOT_FOUND)
        return Response ({'msg' : serializer.errors})


class UserProfileView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
