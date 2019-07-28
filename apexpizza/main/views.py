from django.shortcuts import render, get_object_or_404
from .models import Pizza, AnonymousUser, TempOrder, TempPizza, Size, DoughType, Topping, Drink, TempDrink, Volume, PriceForSize, PriceForVolume
from .models import Snack, Sauce, Set
from .models import TempSnack, TempSauce, TempSet
import json

from django.http import JsonResponse, HttpResponse, response

import logging 

from .serializers import TempOrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


# Create your views here.
logger = logging.getLogger(__name__)

def base(request):
   pizzas = Pizza.objects.all()

   drinks = Drink.objects.all()

   volume = Volume.objects.all()
   pricesFS = PriceForSize.objects.all()
   pricesFV = PriceForVolume.objects.all()

   snacks = Snack.objects.all()
   sauces = Sauce.objects.all()

   sets = Set.objects.all()

   user_num = request.session.get('user')
   cart_price = 0
   cart_num = 0

   temp_orders = TempOrder.objects.all()
   if len(temp_orders)>0:
      for order in temp_orders:
         if order.user.id == user_num:
            temp_order = get_object_or_404(TempOrder, pk=order.id)

      for pizza in order.pizzas.all():
         cart_num += 1
         cart_price += PriceForSize.objects.filter(pizza=pizza.elder_pizza.id).get(size=pizza.size).price

      for drink in order.drinks.all():
         cart_num += 1
         cart_price += PriceForVolume.objects.filter(drink=drink.elder_drink.id).get(volume=drink.volume).price

      for snack in order.snacks.all():
         cart_num += 1

         cart_price += snack.price

      for sauce in order.sauces.all():
         cart_num += 1

         cart_price += sauce.price

      for _set in order.sets.all():
         cart_num += 1

         cart_price += _set.price
   else:
      temp_order = ""

            
      




   num_visits=request.session.get('num_visits', 0)
   request.session['num_visits'] = num_visits+1

   return render(request, 'main/index.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num})

def removeProduct(request):
   user_num = request.session.get('user')

   if request.is_ajax:

      if request.POST.get("object") == "pizza":
         pizza_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         pizza = get_object_or_404(TempPizza, pk=pizza_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.pizzas.remove(pizza)

         return HttpResponse("Pizza removed from order " + str(order_num))
      elif request.POST.get("object") == "drink":
         drink_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         drink = get_object_or_404(TempDrink, pk=drink_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.drinks.remove(drink)

         return HttpResponse("Drink removed from order " + str(order_num))
      elif request.POST.get("object") == "snack":
         snack_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         snack = get_object_or_404(TempSnack, pk=snack_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.snacks.remove(snack)

         return HttpResponse("Snack removed from order " + str(order_num))
      elif request.POST.get("object") == "sauce":
         sauce_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         sauce = get_object_or_404(TempSauce, pk=sauce_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.sauces.remove(sauce)

         return HttpResponse("Sauce removed from order " + str(order_num))
      elif request.POST.get("object") == "set":
         set_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         _set = get_object_or_404(TempSet, pk=set_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.sets.remove(_set)

         return HttpResponse("Set removed from order " + str(order_num))
         

def temp_order(request, pk):

   """

   Обработка сессии пользователя
   
   """

   user_num = request.session.get('user')
   user_quantity = len(AnonymousUser.objects.all())

   if str(user_num)!="None":
      pass
   else:
      user = AnonymousUser.objects.create(title=user_quantity + 1, cashback=0)
      user_num = user.id

      request.session['user'] = user_num

   """

   Обработка AJAX
   
   """

   if request.is_ajax:

      if request.POST.get("object") == "pizza":
         pizza = get_object_or_404(Pizza, pk=pk)


         """

         Создание экземпляра временной пиццы

         """
         temp_pizza = TempPizza()
         temp_pizza.elder_pizza = pizza
         temp_pizza.picture = pizza.picture

         temp_pizza.title = pizza.title

         size = request.POST.get("size")
         temp_pizza.size = get_object_or_404(Size, pk=size)

         dough = request.POST.get("type")
         temp_pizza.doughType = get_object_or_404(DoughType, pk=dough)

         temp_pizza.price = PriceForSize.objects.filter(pizza=pizza).filter(size=size).get().price
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
         drink = get_object_or_404(Drink, pk=pk)

         temp_drink = TempDrink()
         temp_drink.picture = drink.picture

         temp_drink.title = drink.title

         temp_drink.price = PriceForVolume.objects.filter(drink=drink).filter(volume=request.POST.get("volume")).get().price

         temp_drink.volume = get_object_or_404(Volume, pk=request.POST.get("volume"))

         temp_drink.save(force_insert=True)

         """

         Создание экземпляра временного заказа

         """

         temp_orders = TempOrder.objects.all()
         for order in temp_orders:
            if order.user.id == user_num:
               temp_order = get_object_or_404(TempOrder, pk=order.id)
               temp_order.drinks.add(get_object_or_404(TempDrink, pk=temp_drink.id))
               return HttpResponse("Added successfully to exist order")
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.drinks.add(get_object_or_404(TempDrink, pk=temp_drink.id))

         return HttpResponse("Added successfully " + str(user_num))

      elif request.POST.get("object") == "snack":
         snack = get_object_or_404(Snack, pk=pk)

         temp_snack = TempSnack()

         temp_snack.picture = snack.picture
         temp_snack.title = snack.title
         temp_snack.price = snack.price
         temp_snack.save(force_insert=True)


         """

         Создание экземпляра временного заказа

         """

         temp_orders = TempOrder.objects.all()
         for order in temp_orders:
            if order.user.id == user_num:
               temp_order = get_object_or_404(TempOrder, pk=order.id)
               temp_order.snacks.add(get_object_or_404(TempSnack, pk=temp_snack.id))
               return HttpResponse("Added successfully to exist order")
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.snacks.add(get_object_or_404(TempSnack, pk=temp_snack.id))

         return HttpResponse("Added successfully " + str(user_num))

      elif request.POST.get("object") == "sauce":
         sauce = get_object_or_404(Sauce, pk=pk)

         temp_sauce = TempSauce()

         temp_sauce.picture = sauce.picture
         temp_sauce.title = sauce.title
         temp_sauce.price = sauce.price
         temp_sauce.save(force_insert=True)

         """

         Создание экземпляра временного заказа

         """

         temp_orders = TempOrder.objects.all()
         for order in temp_orders:
            if order.user.id == user_num:
               temp_order = get_object_or_404(TempOrder, pk=order.id)
               temp_order.sauces.add(get_object_or_404(TempSauce, pk=temp_sauce.id))
               return HttpResponse("Added successfully to exist order")
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.sauces.add(get_object_or_404(TempSauce, pk=temp_sauce.id))

         return HttpResponse("Added successfully " + str(user_num))

      elif request.POST.get("object") == "set":
         _set = get_object_or_404(Set, pk=pk)

         temp_set = TempSet()

         temp_set.picture = _set.picture
         temp_set.title = _set.title
         temp_set.price = _set.price
         temp_set.save(force_insert=True)

         """

         Создание экземпляра временного заказа

         """

         temp_orders = TempOrder.objects.all()
         for order in temp_orders:
            if order.user.id == user_num:
               temp_order = get_object_or_404(TempOrder, pk=order.id)
               temp_order.sets.add(get_object_or_404(TempSet, pk=temp_set.id))
               return HttpResponse("Added successfully to exist order")
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.sets.add(get_object_or_404(TempSet, pk=temp_set.id))

         return HttpResponse("Added successfully " + str(user_num))
      

   else:
      return HttpResponse("Not AJAX")


def getTempOrder(request):
   
   user_num = request.session.get('user')
   user_quantity = len(AnonymousUser.objects.all())

   if str(user_num)!="None":
      pass
   else:
      user = AnonymousUser.objects.create(title=user_quantity + 1, cashback=0)
      user_num = user.id

      request.session['user'] = user_num

   """

   Обработка AJAX
   
   """

   if request.is_ajax:

      temp_orders = TempOrder.objects.all()
      for order in temp_orders:
         if order.user.id == user_num:
            temp_order = get_object_or_404(TempOrder, pk=order.id)
            
            serializer = TempOrderSerializer(temp_order)
            return JsonResponse(serializer.data, content_type='application/json; charset=utf-8', safe=False)
      return HttpResponse("Order is not exsists. User: " + str(user_num))
      
               
