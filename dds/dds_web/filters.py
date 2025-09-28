from django import forms
import django_filters
from .models import  Category, Record, Status, Type, SubCategory


class RecordFilter(django_filters.FilterSet):
    date__gte = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Дата с',
        widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'})
    )
    date__lte = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        label='Дата по',
        widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'})
    )
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        empty_label='Все',
        widget=forms.Select(attrs={'class':'form-select'})
    )
    type = django_filters.ModelChoiceFilter(
        queryset=Type.objects.all(),
        empty_label='Все',
        widget=forms.Select(attrs={'class':'form-select'})
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        empty_label='Все',
        widget=forms.Select(attrs={'class':'form-select'})
    )
    subcategory = django_filters.ModelChoiceFilter(
        queryset=SubCategory.objects.all(),
        empty_label='Все',
        widget=forms.Select(attrs={'class':'form-select'})
    )

    class Meta:
        model = Record
        fields = ['status', 'type', 'category', 'subcategory']