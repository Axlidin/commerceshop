from rest_framework.generics import ListAPIView
from products.serializer import CategoryListSerializer, ProductListSerializer
from products.models import Category, Product


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = None

class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return Product.objects.cached_all()