from django.core import serializers
from django.http import JsonResponse
from django.urls import reverse_lazy

from .forms import RecordForm
from .models import Category, SubCategory, Record


class FilterCategoryViewMixin:
    model = Record
    form_class = RecordForm
    success_url = reverse_lazy('dds:home')

    def get(self, request, *args, **kwargs):
        if 'X-CAT-AJAX' in request.headers:
            type_id = request.GET.get('type')
            categories = Category.objects.filter(type_id=type_id, is_active=True)
            categories_json = serializers.serialize('json', categories)
            return JsonResponse({'categories': categories_json})

        elif 'X-SUBCAT-AJAX' in request.headers:
            category = request.GET.get('category')
            subcats = SubCategory.objects.filter(category__slug=category, is_active=True)
            subcats_json = serializers.serialize('json', subcats)
            return JsonResponse({'subcategories': subcats_json})
        return super().get(request, *args, **kwargs)