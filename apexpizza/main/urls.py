from django.urls import path
from .views import base
from .views import temp_order, getTempOrder, removeProduct, changeAmount, CartShow
from .views import discounts_view, vacancy_view, blog_view, blog_view_detailed, contact_view, about_view

urlpatterns = [
    path('', base, name='base_view'),
    path('temp/<int:pk>/', temp_order, name='tmp_view'),
    path('getmytemp/', getTempOrder, name='tmp_get'),
    path('remove/', removeProduct, name='rm_prod'),
    path('change_amount/', changeAmount, name='rm_prod'),
    path('cart/', CartShow, name='show_cart'),
    path('cart/getmytemp/', getTempOrder, name='tmp_get'),
    path('cart/remove/', removeProduct, name='rm_prod'),
    path('cart/change_amount/', changeAmount, name='rm_prod'),
    path('cart/temp/<int:pk>/', temp_order, name='tmp_view'),

    path('discounts/', discounts_view, name='dsc_view'),
    path('vacancy/<int:pk>/', vacancy_view, name='vcn_view'),
    
    path('blog/<int:pk>/', blog_view, name='blg_view'),
    path('blog/<int:pk>/detail/', blog_view_detailed, name='blg_view'),

    path('contact/', base, name='dsc_view'),
    path('about/', about_view, name='dsc_view'),



    
]