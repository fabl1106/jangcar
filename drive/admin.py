from django.contrib import admin
from .models import Drive

class DriveOption(admin.ModelAdmin):
    list_display = ['id', 'user', 'departure_area', 'arrive_area', 'departure_date']
    list_filter = ['departure_date']

admin.site.register(Drive, DriveOption)
