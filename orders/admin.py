from django.contrib import admin

from orders.models import *

class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'regions', 'zip_code', 'street', 'address', 'longitude', 'latitude']

class CardsAdmin(admin.ModelAdmin):
    list_display = ['user', 'name_on_card', 'card_number', 'cvv', 'expiration_date']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'subtotal']

class DeleveryTariffAdmin(admin.ModelAdmin):
    list_display = ['branch', 'high', 'width', 'weight', 'price', 'regions', 'delivery_time']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status','total_price']

admin.site.register(Branch, BranchAdmin)
admin.site.register(Card, CardsAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(DeleveryTarif, DeleveryTariffAdmin)
admin.site.register(Order, OrderAdmin)
