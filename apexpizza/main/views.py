from django.shortcuts import render, get_object_or_404
from .models import Pizza
import json

from django.http import JsonResponse

# Create your views here.


def base(request):
    pizzas = Pizza.objects.all()

    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(request, 'main/index.html', {'pizzas' : pizzas, 'number': num_visits})

def temp_order(request, pk):

    sub_data = request.POST.copy
    pizza = get_object_or_404(Pizza, pk=pk)

    data = []

    title = pizza.title
    data.append(title)
    data.append(sub_data)

    return render(request, "main/temp.html", {"value": data})

def requestAjax(request):
   data = {
        'is_valid': False,}

   if request.is_ajax():
      message = request.POST.get('message')
      if message == 'I want an AJAX response':
         data.update(is_valid=True)
         data.update(response='This is the response you wanted')

   return JsonResponse(data)