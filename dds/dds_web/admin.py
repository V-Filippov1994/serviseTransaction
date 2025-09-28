from django.contrib import admin
from .models import Status, Type, Category, SubCategory, Record


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'is_active', 'created_at', 'updated_at')
    list_filter = ('type', 'is_active')
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'is_active', 'created_at', 'updated_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment')
    list_filter = ('status', 'type', 'category', 'subcategory')
    search_fields = ('comment',)
    date_hierarchy = 'date'
