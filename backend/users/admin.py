from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class Users(admin.ModelAdmin):
    list_display = ("email", "username", "count_follower",)
    search_fields = ("email__startswith", "username__startswith")

    def count_follower(self, obj):
        return User.objects.filter(follower__author=obj).count()


@admin.register(Follow)
class Follows(admin.ModelAdmin):
    list_display = ("user", "author",)
