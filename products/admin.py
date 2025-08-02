from django.contrib import admin

from products.models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount', 'in_stock',]

class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['product', 'colour']

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']

class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'value']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user','title', 'rank', 'email', 'created_at']

class ProductWishlistAdmin(admin.ModelAdmin):
    list_display = ['product', 'user']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColour, ProductColorAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, ProductWishlistAdmin)