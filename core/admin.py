from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Service, Part, Order, OrderStatusHistory, OrderPart, Comment
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Роль и контакты', {'fields': ('role', 'phone')}),
    )
    list_display = ('username', 'role', 'phone', 'is_staff')
    list_filter = ('role', 'is_staff')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity_in_stock', 'price')
    search_fields = ('name',)


class OrderPartInline(admin.TabularInline):
    model = OrderPart
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'device_type', 'client', 'master',
        'status', 'total_cost', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('device_type', 'description', 'client__username')
    inlines = [OrderPartInline, CommentInline]


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'changed_at', 'changed_by')
    list_filter = ('status',)


@admin.register(OrderPart)
class OrderPartAdmin(admin.ModelAdmin):
    list_display = ('order', 'part', 'quantity_used')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('order', 'author', 'created_at')