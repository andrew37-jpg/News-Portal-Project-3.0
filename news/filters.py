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