from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

class UserAdminOption(UserAdmin):
    UserAdmin.fieldsets[1][1]['fields'] += ('name','phone','message')
    UserAdmin.add_fieldsets += (
        (('Additional Info'), {'fields':('name','phone','message')}),
    )
    list_display = ['username', 'name', 'phone', 'email']
    list_filter = ['name', 'phone', 'email']


admin.site.register(get_user_model(), UserAdminOption)
