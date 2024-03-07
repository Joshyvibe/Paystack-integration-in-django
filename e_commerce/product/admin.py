from django.contrib import admin
from .models import Product, OrderItem, Order

class orderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'paid', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'address']
    inlines = [orderItemInline]
    readonly_fields = ['created_at']
    list_display_links = ['user', 'created_at']

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
