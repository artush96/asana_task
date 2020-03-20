from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home_url'),
    path('getusers/', get_users, name='get_users_url'),
]