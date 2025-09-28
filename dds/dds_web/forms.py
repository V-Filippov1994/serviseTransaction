from django import forms
from django.utils import timezone

from .models import Status, Type, Category, SubCategory, Record


class RecordForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата'
    )

    class Meta:
        model = Record
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%d')
        elif not self.instance.pk:
            self.initial['date'] = timezone.now().date()

        self.fields['category'] = forms.ChoiceField(
            choices=[(c.slug, c.name) for c in Category.objects.all()],
            widget=forms.Select(attrs={'class': 'form-select'}),
            label='Категория'
        )

        self.fields['subcategory'] = forms.ChoiceField(
            choices=[(sc.slug, sc.name) for sc in SubCategory.objects.all()],
            widget=forms.Select(attrs={'class': 'form-select'}),
            label='Подкатегория'
        )

    def clean_category(self):
        slug = self.cleaned_data.get('category')
        if slug:
            try:
                return Category.objects.get(slug=slug)
            except Category.DoesNotExist:
                raise forms.ValidationError('Выбранная категория не существует.')
        return None

    def clean_subcategory(self):
        slug = self.cleaned_data.get('subcategory')
        if slug:
            try:
                return SubCategory.objects.get(slug=slug)
            except SubCategory.DoesNotExist:
                raise forms.ValidationError('Выбранная подкатегория не существует.')
        return None

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        if not type or not category or not subcategory:
            raise forms.ValidationError('Поля "тип", "категория" и "подкатегория" обязательны.')

        if category.type_id != type.id:
            raise forms.ValidationError('Выбранная категория не соответствует выбранному типу.')

        if subcategory.category_id != category.id:
            raise forms.ValidationError('Выбранная подкатегория не соответствует выбранной категории.')
        return cleaned_data


class BaseRefForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'is_active']


class StatusForm(BaseRefForm):
    class Meta(BaseRefForm.Meta):
        model = Status


class TypeForm(BaseRefForm):
    class Meta(BaseRefForm.Meta):
        model = Type


class CategoryForm(BaseRefForm):
    class Meta(BaseRefForm.Meta):
        model = Category
        fields = ['name', 'type', 'slug', 'is_active']


class SubCategoryForm(BaseRefForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True)

    class Meta(BaseRefForm.Meta):
        model = SubCategory
        fields = ['name', 'category', 'slug', 'is_active']
