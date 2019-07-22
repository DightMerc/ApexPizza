from django.shortcuts import render
from .models import Pizza

# Create your views here.


def base(request):
    pizzas = Pizza.objects.all()
    return render(request, 'main/index.html', {'pizzas' : pizzas})