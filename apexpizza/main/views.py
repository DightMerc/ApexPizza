from django.shortcuts import render, get_object_or_404
from .models import Pizza, AnonymousUser, TempOrder, TempPizza, Size, DoughType, Topping, Drink
import json

from django.http import JsonResponse, HttpResponse

import logging


# Create your views here.
logger = logging.getLogger(__name__)

def base(request):
    pizzas = Pizza.objects.all()
    drinks = Drink.objects.all()

    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(request, 'main/index.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits})

def temp_order(request, pk):

   if request.is_ajax:

      if request.POST.get("object") == "pizza":
         pizza = get_object_or_404(Pizza, pk=pk)

         user_num = request.session.get('user')
         user_quantity = len(AnonymousUser.objects.all())

         if str(user_num)!="None":
            pass
         else:
            user = AnonymousUser.objects.create(title=user_quantity + 1, cashback=0)
            user_num = user.id

            request.session['user'] = user_num
         

         """

         Создание экземпляра временной пиццы

         """
         temp_pizza = TempPizza()
         temp_pizza.picture = pizza.picture
         logger.error(temp_pizza)

         temp_pizza.title = pizza.title

         size = request.POST.get("size")
         # temp_pizza.size = get_object_or_404(Size, pk=size)

         dough = request.POST.get("type")
         temp_pizza.doughType = get_object_or_404(DoughType, pk=dough)

         temp_pizza.price = pizza.price
         temp_pizza.save(force_insert=True)

         toppings = request.POST.get("toppings")
         for topping in toppings.split():
            temp_pizza.toppings.add(get_object_or_404(Topping, pk=int(topping)))


         """

         Создание экземпляра временного заказа
         
         """
         temp_orders = TempOrder.objects.all()
         for order in temp_orders:
            if order.user.id == user_num:
               temp_order = get_object_or_404(TempOrder, pk=order.id)
               temp_order.pizzas.add(get_object_or_404(TempPizza, pk=temp_pizza.id))
               return HttpResponse("Added successfully to exist order "  + str(user_num) + " " + str(order.id) + " " + str(order.user.id))
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.pizzas.add(get_object_or_404(TempPizza, pk=temp_pizza.id))

         return HttpResponse("Added successfully " + str(user_num))
      elif request.POST.get("object") == "drink":
         return HttpResponse("Гениально")
         

   else:
      return HttpResponse("Not AJAX")

