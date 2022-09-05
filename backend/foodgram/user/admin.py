from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User, Follow


class UserAdmin(UserAdmin):
    """Кастомная админка модели User."""
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    ordering = ('pk',)


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author'
    )
    search_fields = ('user__username', 'author__username')

admin.site.register(User)
admin.site.register(Follow)