from django.contrib import admin
from .models import Recipy, RecipyIngredients, RecipyTag, Tag, Ingredients


admin.site.register(Recipy)
admin.site.register(RecipyIngredients)
admin.site.register(RecipyTag)
admin.site.register(Tag)
admin.site.register(Ingredients)
