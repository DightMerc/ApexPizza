from django.shortcuts import render
from main.models import TempOrder
# Create your views here.

def main_view(request):
    orders = TempOrder.objects.all()

    return render(request, 'trivial_dummy_admin/main.html', {'orders': orders})