from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

# Register your models here.
from user.models import User, UserLogo


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'last_login', 'is_admin',)
    search_fields =('email', 'username',)
    readonly_fields = ('id','last_login',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)
admin.site.register(UserLogo)
