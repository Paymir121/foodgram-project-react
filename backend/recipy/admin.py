from django.contrib import admin

from .models import Recipy, RecipyIngredient, RecipyTag, Tag, Ingredient, Favorite, ShoppingCart

admin.site.register(RecipyIngredient)
admin.site.register(RecipyTag)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)

@admin.register(Recipy)
class Recipes(admin.ModelAdmin):
    list_display = ("name", "author", "count_favorite")
    list_filter = ("name", "author", 'tags')
    search_fields = ("author__startswith", "name__startswith")

    def count_favorite(self, obj):
        return Recipy.objects.filter(favorites__recipy=obj).count()

@admin.register(Ingredient)
class Ingredient(admin.ModelAdmin):
    list_filter = ("measurement_unit", )
    list_display = ("name", "measurement_unit", )
    search_fields = ("name__startswith", "measurement_unit__startswith")