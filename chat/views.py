from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,generics
from . serializers import *
from . models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django.contrib.auth import authenticate



# Create your views here.

def index(request):
    return render(request, 'index.html')

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    def create(self,request,*args,**kwargs):
        try:
            response = super().create(request, *args,**kwargs)
            return Response({
                "status": "success",
                "response_code": status.HTTP_200_OK,
                "message": "OTP sent successfully to the email"
            }, status=response.status_code)
        except Exception as e:
            return Response({"status":"error","response_code":status.HTTP_400_BAD_REQUEST,"message":str(e)})
        

class VerifyOtpView(generics.GenericAPIView):
    serializer_class = VerifyOtpSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                return Response({"status":"success","response_code":status.HTTP_200_OK,"message":"OTP verified"})
        except Exception as e:
            return Response({"status":"error","response_code":status.HTTP_400_BAD_REQUEST,"message":str(e)})
        
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request,*args,**kwargs):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(email=email,password=password)

            if user is None:
                return Response({"status":"error","response_code":status.HTTP_401_UNAUTHORIZED,"message":"Invalid email or password"})
            if not user.is_verified:
                return Response({"status":"error","response_code":status.HTTP_401_UNAUTHORIZED,"message":"User is not verified, try register again"})
            
            refresh = RefreshToken.for_user(user)
            return Response({"status":"success","response_code":status.HTTP_200_OK,"message":"Login Successfull","tokens":{"refresh_token":str(refresh),"access_token":str(refresh.access_token)}})
        except Exception as e:
            return Response({"status":"error","response_code":status.HTTP_400_BAD_REQUEST,"message":str(e)})


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"status":"error","response_code":status.HTTP_400_BAD_REQUEST,"message":"Refresh token is required"})
            token = RefreshToken(refresh_token)
            if BlacklistedToken.objects.filter(token__jti=token['jti']).exists():
                return Response({"status":"error","response_code":status.HTTP_401_UNAUTHORIZED,"message":"Refresh token is blacklisted. Try another refreshtoken"})
            access_token = super().post(request,*args,**kwargs)
            return Response({"status":"success","response_code":status.HTTP_200_OK,"access_token": access_token.data['access']})
        except Exception as e:
            return Response({"status":"error","response_code":status.HTTP_400_BAD_REQUEST,"message":str(e)})