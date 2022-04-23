from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from .models import Post, Category


class PostFilter(FilterSet):
    Category = ModelChoiceFilter(
        field_name='postCategory',
        label='Категория',
        lookup_expr='exact',
        queryset=Category.objects.all(),
    )

    Title = CharFilter(
        field_name='title',
        label='Заголовок содержит',
        lookup_expr='icontains',
    )

    TimeAdding = DateFilter(
        'timeAdding',
        lookup_expr='gt',
        label='Дата, не позднее',
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
        model = Post
        fields = {
            'author__authorUser': ['exact'],
        }