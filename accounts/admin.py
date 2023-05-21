from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account, Profile


class AccountAdmin(UserAdmin):
    list_display = ('id', 'username', 'is_active', 'email', 'first_name', 'last_name', 'is_staff')
    list_editable = ('email', 'username')
    search_fields = ('email', 'username', 'status')
    readonly_fields = ("id", "date_joined", "last_login")

    filter_horizontal = ()
    fieldsets = ()
    ordering = ('-date_joined',)

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)