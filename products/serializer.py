from rest_framework import serializers
from common.serializers import MediaSerializer
from products.models import Category, Product

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['image', 'lft', 'rght', 'tree_id', 'level']

class ProductListSerializer(serializers.ModelSerializer):
    thumbnail = MediaSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "price", "category", "in_stock", "brand", "discount", "thumbnail")
