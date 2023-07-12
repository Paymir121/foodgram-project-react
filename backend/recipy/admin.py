from django.contrib import admin
from .models import Recipy, RecipyIngredient, RecipyTag, Tag, Ingredient


admin.site.register(Recipy)
admin.site.register(RecipyIngredient)
admin.site.register(RecipyTag)
admin.site.register(Tag)
admin.site.register(Ingredient)
