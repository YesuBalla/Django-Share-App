from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from ShareApp.permissions import IsOpsUser,IsClientUser
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer,RegisterSerializer
from FilesApp.models import User
from .utils import encrypt_url,decrypt_url
from django.conf import settings
from django.core.mail import send_mail


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                update_last_login(None, user)
                return Response({
                    'token': token.key,
                    'message': 'Login successful'
                }, status=HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    permission_classes = [IsAuthenticated,IsClientUser]
    # permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            encrypted_url = encrypt_url(user.email)  
            confirmation_url = f"http://localhost:8000/confirm/{encrypted_url}"

            subject = 'Verify Your Email Address'
            message = f"Hi {user.username},\n\nPlease verify your email by clicking the link below:\n{confirmation_url}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)
            return Response({
                "message": "User registered successfully",
                "confirmation_url": confirmation_url
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ConfirmUserView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated,IsClientUser]
    def get(self, request, encrypted_data):
        try:
            decrypted_email = decrypt_url(encrypted_data)
            user = User.objects.get(email=decrypted_email)
            user.is_active = True
            user.save()

            return Response({"message": f"User {user.username} confirmed!"}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid or expired URL"}, status=HTTP_400_BAD_REQUEST)



