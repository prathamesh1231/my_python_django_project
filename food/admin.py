from django.contrib import admin
from .models import MenuItem, ContactMessage, Cart, CartItem, Order, OrderItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available')
    list_filter  = ('category', 'is_available')
    list_editable = ('price', 'is_available')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    readonly_fields = ('created_at',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('menu_item', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'status', 'total', 'created_at')
    list_filter   = ('status',)
    list_editable = ('status',)
    inlines       = [OrderItemInline]
    readonly_fields = ('created_at',)

admin.site.register(Cart)
admin.site.register(CartItem)
