from django.urls import path
from .views import base
from .views import temp_order, requestAjax

urlpatterns = [
    path('', base, name='base_view'),
    path('temp/<int:pk>/', temp_order, name='tmp_view'),
    path('my_ajax_request/', requestAjax, name='my_ajax_request'),
    
]