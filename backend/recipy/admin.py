from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Favorite, Ingredient, Recipy, RecipyIngredient, RecipyTag,
                     ShoppingCart, Tag)

admin.site.register(RecipyIngredient)
admin.site.register(RecipyTag)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)


@admin.register(Ingredient)
class Ingredient(admin.ModelAdmin):
    list_filter = ("measurement_unit",)
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name__startswith", "measurement_unit__startswith")


class IngredientInline(admin.TabularInline):
    model = Recipy.ingredients.through
    min_num = 1


class TagInline(admin.TabularInline):
    model = Recipy.tags.through
    min_num = 1
    extra = 3


@admin.register(Recipy)
class Recipes(admin.ModelAdmin):
    fields = ["name",
              "author",
              'text',
              'cooking_time',
              'image',
              'get_image', ]
    readonly_fields = ["get_image"]
    list_display = ("name", "author", "count_favorite", 'get_image_preview', )
    list_filter = ("name", "author", "tags")
    search_fields = ("author__startswith", "name__startswith")
    inlines = [
        IngredientInline,
        TagInline,
    ]

    def get_image(self, obj):
        return mark_safe(
            f'<img src={obj.image.url} style="max-height: 200px;"')

    def get_image_preview(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    def count_favorite(self, obj):
        return Recipy.objects.filter(favorites__recipy=obj).count()
