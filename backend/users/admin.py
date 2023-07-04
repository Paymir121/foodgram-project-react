from django.contrib import admin
from .models import User


class Users(admin.ModelAdmin):
    pass


admin.site.register(User, Users)