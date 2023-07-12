from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import Follow, User

admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'is_active'
    )
    list_filter = ('first_name', 'email',)
    # Если честно не понял, зачем нам фильтры по имени и почте, почта -
    # unique=True. А фильтр по имени бесполезный)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    list_filter = ('user', 'following',)


admin.site.register(Follow, FollowAdmin)
admin.site.register(User, UserAdmin)
