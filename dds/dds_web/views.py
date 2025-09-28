from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django_filters.views import FilterView

from .filters import RecordFilter
from .forms import CategoryForm, SubCategoryForm, TypeForm, StatusForm
from .models import Record, Status, Type, Category, SubCategory
from .mxins import FilterCategoryViewMixin


class BaseCreateView(CreateView):
    template_name = 'dds_web/form.html'
    success_url = reverse_lazy('dds:manage_refs')


class BaseUpdateView(UpdateView):
    template_name = 'dds_web/form.html'
    success_url = reverse_lazy('dds:manage_refs')


class BaseDeleteView(DeleteView):
    template_name = 'dds_web/confirm_delete.html'
    success_url = reverse_lazy('dds:manage_refs')


class StatusCreateView(BaseCreateView):
    model = Status
    form_class = StatusForm
    extra_context = {'title': 'Добавить статус'}


class StatusUpdateView(BaseUpdateView):
    model = Status
    form_class = StatusForm
    extra_context = {'title': 'Редактировать статус'}


class StatusDeleteView(BaseDeleteView):
    model = Status
    extra_context = {'title': 'Удалить статус?'}


class TypeCreateView(BaseCreateView):
    model = Type
    form_class = TypeForm
    extra_context = {'title': 'Добавить тип'}


class TypeUpdateView(BaseUpdateView):
    model = Type
    form_class = TypeForm
    extra_context = {'title': 'Редактировать тип'}


class TypeDeleteView(BaseDeleteView):
    model = Type
    extra_context = {'title': 'Удалить тип?'}


class CategoryCreateView(BaseCreateView):
    model = Category
    form_class = CategoryForm
    extra_context = {'title': 'Добавить категорию'}


class CategoryUpdateView(BaseUpdateView):
    model = Category
    form_class = CategoryForm
    extra_context = {'title': 'Редактировать категорию'}


class CategoryDeleteView(BaseDeleteView):
    model = Category
    extra_context = {'title': 'Удалить категорию?'}


class SubCategoryCreateView(BaseCreateView):
    model = SubCategory
    form_class = SubCategoryForm
    extra_context = {'title': 'Добавить подкатегорию'}


class SubCategoryUpdateView(BaseUpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    extra_context = {'title': 'Редактировать подкатегорию'}


class SubCategoryDeleteView(BaseDeleteView):
    model = SubCategory
    extra_context = {'title': 'Удалить подкатегорию?'}


class ManageRefsView(TemplateView):
    template_name = 'dds_web/manage_refs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        return context


class RecordListView(FilterView):
    model = Record
    template_name = 'dds_web/records_list.html'
    context_object_name = 'records'
    filterset_class = RecordFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('status', 'type', 'category', 'subcategory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.filter(is_active=True)
        context['types'] = Type.objects.filter(is_active=True)
        context['categories'] = Category.objects.filter(is_active=True)
        context['subcategories'] = SubCategory.objects.filter(is_active=True)
        context['filters'] = self.request.GET
        return context


class RecordCreateView(FilterCategoryViewMixin, CreateView):
    template_name = 'dds_web/record_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create'] = True
        context['success_url'] = self.success_url
        return context


class RecordUpdateView(FilterCategoryViewMixin, UpdateView):
    template_name = 'dds_web/record_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create'] = False
        context['success_url'] = self.success_url
        return context


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy('dds:home')