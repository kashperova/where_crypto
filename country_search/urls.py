from django.contrib import admin
from django.urls import path
from .views import home, search, get_info, home_page_return


urlpatterns = [
    path('', home, name='home'),
    path('/search', search, name='search'),
    path('/get_info', get_info, name='get_info'),
    path(r'^.+$', home_page_return, name='home_page_return'),
]