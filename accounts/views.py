from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import CustomUser, BlacklistedToken
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, format=None):
        if request.user.username == username:
            user = get_object_or_404(CustomUser, username=username)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': '프로필 조회 권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            access_token = request.data.get('access')

            # Refresh 토큰 무효화
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            # Access 토큰 무효화
            if access_token:
                BlacklistedToken.objects.create(token=access_token, user=request.user)

            return Response({"message": "Successfully logged out"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)