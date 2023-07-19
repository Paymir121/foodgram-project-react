from django.contrib import admin
from .models import User, Follow


class Users(admin.ModelAdmin):
    pass


class Follows(admin.ModelAdmin):
    pass

admin.site.register(User, Users)
admin.site.register(Follow, Follows)