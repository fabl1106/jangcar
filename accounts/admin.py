from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from drive.models import Drive

class DriveInline(admin.TabularInline):
    model = Drive


class UserAdminOption(UserAdmin):
    UserAdmin.fieldsets[1][1]['fields'] += ('name','phone','message')
    UserAdmin.add_fieldsets += (
        (('Additional Info'), {'fields':('name','phone','message')}),
    )
    list_display = ['username', 'name', 'phone', 'email']
    list_filter = ['name', 'phone', 'email']
    inlines = [DriveInline]

admin.site.register(get_user_model(), UserAdminOption)
