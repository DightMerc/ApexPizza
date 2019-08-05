from django.urls import path, re_path, include
from .views import main_view

urlpatterns = [
    path('', main_view, name='main_view'),

]