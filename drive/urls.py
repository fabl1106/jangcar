from django.urls import path

from .views import *

app_name = 'drive'

urlpatterns = [
    path('mylist/', drive_mylist, name='mylist'),
    path('list/',drive_list, name='list'),
    path('detail/<int:pk>', DriveDetail.as_view(), name='detail'),
    path('update/<int:pk>', drive_update, name='update'),
    path('delete/<int:pk>', drive_delete, name='delete'),
    path('create/', drive_create, name='create'),
    path('', Main.as_view(), name='main'),
]