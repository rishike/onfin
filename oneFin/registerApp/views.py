from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer
from helper.helper import add_request_counter
from django.core.signals import request_finished


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        request_finished.connect(add_request_counter)
        return Response({
            "access_token": get_tokens_for_user(user)['access']
        })


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_name = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=user_name, password=password)
            if user is not None:
                request_finished.connect(add_request_counter)
                return Response({
                    "message": "Logged in success",
                    "access_token": get_tokens_for_user(user)['access']
                })
        request_finished.connect(add_request_counter)
        return Response({
            "message": "Username and Password does not match"
        })
