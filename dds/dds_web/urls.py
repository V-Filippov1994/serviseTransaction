from django.urls import path
from . import views
from .views import (
    StatusCreateView, StatusUpdateView, StatusDeleteView, TypeCreateView, TypeUpdateView, TypeDeleteView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView, SubCategoryCreateView, SubCategoryUpdateView,
    SubCategoryDeleteView
)

app_name = 'dds'

urlpatterns = [
    path('', views.RecordListView.as_view(), name='home'),

    path('create/', views.RecordCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', views.RecordUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.RecordDeleteView.as_view(), name='delete'),

    path('manage-refs/', views.ManageRefsView.as_view(), name='manage_refs'),

    path('status/add/', StatusCreateView.as_view(), name='add_status'),
    path('status/edit/<int:pk>/', StatusUpdateView.as_view(), name='edit_status'),
    path('status/delete/<int:pk>/', StatusDeleteView.as_view(), name='delete_status'),

    path('type/add/', TypeCreateView.as_view(), name='add_type'),
    path('type/edit/<int:pk>/', TypeUpdateView.as_view(), name='edit_type'),
    path('type/delete/<int:pk>/', TypeDeleteView.as_view(), name='delete_type'),

    path('category/add/', CategoryCreateView.as_view(), name='add_category'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view(), name='edit_category'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),

    path('subcategory/add/', SubCategoryCreateView.as_view(), name='add_subcategory'),
    path('subcategory/edit/<int:pk>/', SubCategoryUpdateView.as_view(), name='edit_subcategory'),
    path('subcategory/delete/<int:pk>/', SubCategoryDeleteView.as_view(), name='delete_subcategory'),
]
