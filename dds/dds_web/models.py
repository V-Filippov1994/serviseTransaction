from django.db import models
from django.core.validators import MinValueValidator


class BaseModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Status(BaseModel):
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(BaseModel):
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Category(BaseModel):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories', verbose_name='Тип')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Record(models.Model):
    date = models.DateField(verbose_name='Дата операции')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='records', verbose_name='Статус')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='records', verbose_name='Тип')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='records', verbose_name='Категория')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='records', verbose_name='Подкатегория')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Сумма')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ['-date', '-id']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f'{self.date} — {self.type.name} — {self.amount}'
