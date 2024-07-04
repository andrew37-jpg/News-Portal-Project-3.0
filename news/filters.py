from django.forms import DateInput
from django_filters import FilterSet, CharFilter, \
    ModelMultipleChoiceFilter, DateFilter, \
    ModelChoiceFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Author


# создаём фильтр
class PostFilter(FilterSet):
    title = CharFilter('title',
                       label='Заголовок содержит:',
                       lookup_expr='icontains',
                       )

    author = ModelChoiceFilter(field_name='author',
                                       label='Автор:',
                                       lookup_expr='exact',
                                       queryset=Author.objects.all()
                                       )
    datetime = DateFilter(
        field_name='dateCreation',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Даты позже'
    )

    class Meta:
        model = Post
        fields = []


from django import template

register = template.Library()

# Список нежелательных слов
BAD_WORDS = ['редиска', 'дурак', 'идиот']


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр 'censor' может быть применен только к строкам.")

    for word in BAD_WORDS:
        value = value.replace(word, '*' * len(word))
        value = value.replace(word.capitalize(), '*' * len(word))

    return value

from django_filters import FilterSet
from .models import Product

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ProductFilter(FilterSet):
   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Product
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'name': ['icontains'],
           # количество товаров должно быть больше или равно
           'quantity': ['gt'],
           'price': [
               'lt',  # цена должна быть меньше или равна указанной
               'gt',  # цена должна быть больше или равна указанной
           ],
       }

import django_filters
from .models import NewsArticle

class NewsArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    pub_date = django_filters.DateFilter(field_name='pub_date', lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = NewsArticle
        fields = ['title', 'author', 'pub_date']