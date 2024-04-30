from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'content', 'image', 'owner']
    
    def get_owner(self, obj):
        return obj.owner.username 