from django.contrib import admin
from .models import Menu, Order, Cart


class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "small", "large")

    fieldsets = [
        ("Dish", {"fields": ["name", "type"]}),
        ("Prices", {"fields": ["small", "large"]})
    ]


class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "size")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "item", "price", "time", "status")
    list_filter = ("user", "status")

    fieldsets = [
        ("User", {"fields": ["user"]}),
        ("Ordered item", {"fields": ["item", "price"]}),
        ("Order status", {"fields": ["time", "status"]})
    ]


# Register your models here.
admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)


admin.site.site_header = "Admin Panel"
