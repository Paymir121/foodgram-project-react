from django_filters import rest_framework as filter

from recipy.models import Recipy, Tag


class RecipyFilter(filter.FilterSet):
    tags = filter.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )

    class Meta:
        model = Recipy
        fields = ['tags', ]
