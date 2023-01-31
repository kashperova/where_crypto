from django.contrib import admin
from django.urls import path
from .views import home, search, get_info, home_page_return, get_ukraine_map


urlpatterns = [
    path('', home, name='home'),
    path('/search', search, name='search'),
    path('/get_info', get_info, name='get_info'),
    path('/map', get_ukraine_map, name='get_map'),
    path(r'^.+$', home_page_return, name='home_page_return'),
]