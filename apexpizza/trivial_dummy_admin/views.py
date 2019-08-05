from django.shortcuts import render
from main.models import Order
# Create your views here.

def pizza_new(request):
    orders = Order.objects.all()

    return render(request, 'trivial_dummy_admin/main.html', {'orders': orders})