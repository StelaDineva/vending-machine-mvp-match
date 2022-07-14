from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'amount_available', 'seller_id')
    list_filter = ('amount_available', )
    search_fields = ('name', )
