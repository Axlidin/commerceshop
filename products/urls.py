from django.urls import path
from products.views import *

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('products/', ProductListView.as_view(), name='products'),
    ]