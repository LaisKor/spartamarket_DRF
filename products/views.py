from rest_framework import generics, permissions, pagination
from .models import Product
from .serializers import ProductSerializer

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5 
    page_size_query_param = 'page_size' 
    max_page_size = 100

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if self.request.method in ['PUT', 'DELETE'] and not request.user == obj.owner:
            self.permission_denied(request, message='작성자만 수정이 가능합니다')