from django.contrib import admin
from django.conf import settings

from users.models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email'
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email'
    )
    list_filter = (
        'username',
        'email'
    )
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'following'
    )
    empty_value_display = settings.EMPTY_VALUE
