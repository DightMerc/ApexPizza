from django.urls import path
from .views import base
from .views import temp_order

urlpatterns = [
    path('', base, name='base_view'),
    path('temp/<int:pk>/', temp_order, name='tmp_view'),
    
]