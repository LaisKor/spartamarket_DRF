from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# 로그인 및 프로필 조회는 여기에 추가 구현
