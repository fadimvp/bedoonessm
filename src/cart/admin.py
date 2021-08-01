from django.contrib import admin
from .models import Cart ,CartItems
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added',)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity')
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItems,CartItemsAdmin)