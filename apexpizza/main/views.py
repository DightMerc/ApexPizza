from django.shortcuts import render, get_object_or_404
from .models import Pizza, AnonymousUser, TempOrder, TempPizza, Size, DoughType, Topping, Drink, TempDrink, Volume, PriceForSize, PriceForVolume
from .models import Snack, Sauce, Set
from .models import TempSnack, TempSauce, TempSet, Present, TempPresent, Discount, Vacancy, BlogPost
import json

from django.core.paginator import Paginator

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

   total_amount = 0
   if temp_order!="":
      for element in temp_order.pizzas.all():
         total_amount += element.quantity
      for element in temp_order.drinks.all():
         total_amount += element.quantity
      for element in temp_order.snacks.all():
         total_amount += element.quantity
      for element in temp_order.sauces.all():
         total_amount += element.quantity
      for element in temp_order.sets.all():
         total_amount += element.quantity

   return render(request, 'main/index.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount})

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
      elif request.POST.get("object") == "present":
         present_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         present = get_object_or_404(TempPresent, pk=present_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.presents.remove(present)

         return HttpResponse("Present removed from order " + str(order_num))
         

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
         temp_pizza.quantity = 1

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
               return HttpResponse(str(temp_pizza.id) + " " + str(temp_order.id) + " "  + str(temp_pizza.doughType) + " " + str(temp_pizza.size))
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.pizzas.add(get_object_or_404(TempPizza, pk=temp_pizza.id))
         return HttpResponse(str(temp_pizza.id) + " " + str(temp_order.id) + " "  + str(temp_pizza.doughType) + " " + str(temp_pizza.size))

      elif request.POST.get("object") == "drink":
         drink = get_object_or_404(Drink, pk=pk)

         temp_drink = TempDrink()
         temp_drink.elder_drink = drink
         temp_drink.quantity = 1

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
               return HttpResponse(str(temp_drink.id) + " " + str(temp_order.id) + " "  + str(temp_drink.volume))
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.drinks.add(get_object_or_404(TempDrink, pk=temp_drink.id))

         return HttpResponse(str(temp_drink.id) + " " + str(temp_order.id) + " "  + str(temp_drink.volume))
         

      elif request.POST.get("object") == "snack":
         snack = get_object_or_404(Snack, pk=pk)

         temp_snack = TempSnack()

         temp_snack.picture = snack.picture
         temp_snack.quantity = 1

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
               return HttpResponse(str(temp_snack.id) + " " + str(temp_order.id))
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.snacks.add(get_object_or_404(TempSnack, pk=temp_snack.id))
         return HttpResponse(str(temp_snack.id) + " " + str(temp_order.id))


      elif request.POST.get("object") == "sauce":
         sauce = get_object_or_404(Sauce, pk=pk)

         temp_sauce = TempSauce()

         temp_sauce.picture = sauce.picture
         temp_sauce.quantity = 1

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
               return HttpResponse(str(temp_sauce.id) + " " + str(temp_order.id))
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.sauces.add(get_object_or_404(TempSauce, pk=temp_sauce.id))

         return HttpResponse(str(temp_sauce.id) + " " + str(temp_order.id))
         

      elif request.POST.get("object") == "set":
         _set = get_object_or_404(Set, pk=pk)

         temp_set = TempSet()

         temp_set.picture = _set.picture
         temp_set.quantity = 1

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
               return HttpResponse(str(temp_set.id) + " " + str(temp_order.id))
               
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.sets.add(get_object_or_404(TempSet, pk=temp_set.id))

         return HttpResponse(str(temp_set.id) + " " + str(temp_order.id))
         
      

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


def changeAmount(request):
   user_num = request.session.get('user')

   change_object = request.POST.get("object")
   operation = request.POST.get("operation")
   number = request.POST.get("number")
   order_number = request.POST.get("order_number")

   if request.is_ajax:
      

      if change_object == "pizza":
         changing_model = get_object_or_404(TempPizza, pk=number)

      elif change_object == "drink":
         changing_model = get_object_or_404(TempDrink, pk=number)

      elif change_object == "snack":
         changing_model = get_object_or_404(TempSnack, pk=number)
      
      elif change_object == "sauce":
         changing_model = get_object_or_404(TempSauce, pk=number)
      
      elif change_object == "set":
         changing_model = get_object_or_404(TempSet, pk=number)
      elif change_object == "present":
         try:
            order = get_object_or_404(TempOrder, pk=order_number)
            changing_model = order.presents.all().get(pk=number)
         except Exception as e:
            changing_model = TempPresent()
            changing_model.title = get_object_or_404(Present, pk=number).title
            changing_model.price = get_object_or_404(Present, pk=number).price
            changing_model.quantity = 0
            changing_model.save()
            order = get_object_or_404(TempOrder, pk=order_number)
            order.presents.add(changing_model)
            

            
         

      if operation == "plus":
         changing_model.quantity = changing_model.quantity + 1
         changing_model.save()

         order = get_object_or_404(TempOrder, pk=order_number)

         all_price = 0
         for pizza in order.pizzas.all():
            all_price += int(pizza.price) * int(pizza.quantity)
         for drink in order.drinks.all():
            all_price += int(drink.price) * int(drink.quantity)
         for snack in order.snacks.all():
            all_price += int(snack.price) * int(snack.quantity)
         for sauce in order.sauces.all():
            all_price += int(sauce.price) * int(sauce.quantity)
         for _set in order.sets.all():
            all_price += int(_set.price) * int(_set.quantity)

         return HttpResponse(str(changing_model.quantity) + " " + str(all_price))

      elif operation == "minus":
         order = get_object_or_404(TempOrder, pk=order_number)

         all_price = 0
         for pizza in order.pizzas.all():
            all_price += int(pizza.price) * int(pizza.quantity)
         for drink in order.drinks.all():
            all_price += int(drink.price) * int(drink.quantity)
         for snack in order.snacks.all():
            all_price += int(snack.price) * int(snack.quantity)
         for sauce in order.sauces.all():
            all_price += int(sauce.price) * int(sauce.quantity)
         for _set in order.sets.all():
            all_price += int(_set.price) * int(_set.quantity)



         if changing_model.quantity - 1 == 0:
            order = get_object_or_404(TempOrder, pk=order_number)

            if change_object == "pizza":
               order.pizzas.remove(changing_model)

            elif change_object == "drink":
               order.drinks.remove(changing_model)

            elif change_object == "snack":
               order.snacks.remove(changing_model)
            
            elif change_object == "sauce":
               order.sauces.remove(changing_model)
            
            elif change_object == "set":
               order.sets.remove(changing_model)
            elif change_object == "present":
               order.presents.remove(changing_model)

            return HttpResponse("removed " + str(all_price))

         elif changing_model.quantity == 0:
            order = get_object_or_404(TempOrder, pk=order_number)

            if change_object == "pizza":
               order.pizzas.remove(changing_model)

            elif change_object == "drink":
               order.drinks.remove(changing_model)

            elif change_object == "snack":
               order.snacks.remove(changing_model)
            
            elif change_object == "sauce":
               order.sauces.remove(changing_model)
            
            elif change_object == "set":
               order.sets.remove(changing_model)
            elif change_object == "present":
               order.presents.remove(changing_model)

            return HttpResponse("removed " + str(all_price))
         else:
            if changing_model.quantity!=0:
               changing_model.quantity = changing_model.quantity - 1
               changing_model.save()

            

            return HttpResponse(str(changing_model.quantity) + " " + str(all_price))


def CartShow(request):

   pizzas = Pizza.objects.all()

   drinks = Drink.objects.all()

   volume = Volume.objects.all()
   pricesFS = PriceForSize.objects.all()
   pricesFV = PriceForVolume.objects.all()

   snacks = Snack.objects.all()
   sauces = Sauce.objects.all()

   sets = Set.objects.all()

   presents = Present.objects.all()

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

   total_amount = 0
   for element in temp_order.pizzas.all():
      total_amount += element.quantity
   for element in temp_order.drinks.all():
      total_amount += element.quantity
   for element in temp_order.snacks.all():
      total_amount += element.quantity
   for element in temp_order.sauces.all():
      total_amount += element.quantity
   for element in temp_order.sets.all():
      total_amount += element.quantity
   

   return render(request, 'main/cart.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount, "presents": presents})

   


      
def discounts_view(request):

   discounts = Discount.objects.all()

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

   total_amount = 0
   if temp_order!="":
      for element in temp_order.pizzas.all():
         total_amount += element.quantity
      for element in temp_order.drinks.all():
         total_amount += element.quantity
      for element in temp_order.snacks.all():
         total_amount += element.quantity
      for element in temp_order.sauces.all():
         total_amount += element.quantity
      for element in temp_order.sets.all():
         total_amount += element.quantity

   return render(request, 'main/discounts.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount, "discounts": discounts})

def vacancy_view(request, pk):
   pizzas = Pizza.objects.all()
   vacancies = Vacancy.objects.all()


   pagination = Paginator(vacancies, 4)

   

   page_count = []
   a = 0
   while a<pagination.num_pages:
      a += 1
      page_count.append(int(a))


   if not pk in page_count:
      return HttpResponse("Page not found", status=404)
      
   next_page = "#"
   prev_page = "#"

   if pk>1:
      prev_page = str(pk - 1)
   else:
      prev_page = "#"

   if pk + 1 > pagination.num_pages:
      next_page = "#"
   else:
      next_page = str(pk + 1)


   current_page = pk


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

   total_amount = 0
   if temp_order!="":
      for element in temp_order.pizzas.all():
         total_amount += element.quantity
      for element in temp_order.drinks.all():
         total_amount += element.quantity
      for element in temp_order.snacks.all():
         total_amount += element.quantity
      for element in temp_order.sauces.all():
         total_amount += element.quantity
      for element in temp_order.sets.all():
         total_amount += element.quantity

   return render(request, 'main/vacancy.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount, "vacancies": pagination.page(pk).object_list,"page_count":page_count, "current_page": current_page, "prev":prev_page, "next":next_page})



def blog_view(request):

   pizzas = Pizza.objects.all()

   drinks = Drink.objects.all()


   posts = BlogPost.objects.all()

   pagination = Paginator(posts, 6)

   

   page_count = []
   a = 0
   while a<pagination.num_pages:
      a += 1
      page_count.append(int(a))


   if not pk in page_count:
      return HttpResponse("Page not found", status=404)
      
   next_page = "#"
   prev_page = "#"

   if pk>1:
      prev_page = str(pk - 1)
   else:
      prev_page = "#"

   if pk + 1 > pagination.num_pages:
      next_page = "#"
   else:
      next_page = str(pk + 1)


   current_page = pk


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

   total_amount = 0
   if temp_order!="":
      for element in temp_order.pizzas.all():
         total_amount += element.quantity
      for element in temp_order.drinks.all():
         total_amount += element.quantity
      for element in temp_order.snacks.all():
         total_amount += element.quantity
      for element in temp_order.sauces.all():
         total_amount += element.quantity
      for element in temp_order.sets.all():
         total_amount += element.quantity

   return render(request, 'main/blog.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount, "posts": posts, "next": next_page, "prev": prev_page, "current_page": current_page})









      
               
