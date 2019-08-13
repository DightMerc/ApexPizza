from django.shortcuts import render, get_object_or_404
from .models import Pizza, AnonymousUser, TempOrder, TempPizza, Size, DoughType, Topping, Drink, TempDrink, Volume, PriceForSize, PriceForVolume
from .models import Snack, Sauce, Set
from .models import TempSnack, TempSauce, TempSet, Present, TempPresent, Discount, Vacancy, BlogPost, Order, User, Order, HeaderImage, HeaderMobileImage, ArchievedOrder
import json

from django.core.paginator import Paginator

from django.http import JsonResponse, HttpResponse, response, HttpResponsePermanentRedirect

import logging 

from .serializers import TempOrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
import plural_ru


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

   temp_orders = TempOrder.objects.all()
   temp_order = None

   

   try:
      cashback = User.objects.get(link=user_num).cashback
   except Exception as e:
      cashback = "0"

   header_images = HeaderImage.objects.all()
   

   if len(temp_orders)>0:
      for order in temp_orders:
         if order.user.id == user_num:
            temp_order = get_object_or_404(TempOrder, pk=order.id)

            for pizza in order.pizzas.all():
               cart_price += PriceForSize.objects.filter(pizza=pizza.elder_pizza.id).get(size=pizza.size).price * pizza.quantity

            for drink in order.drinks.all():
               cart_price += PriceForVolume.objects.filter(drink=drink.elder_drink.id).get(volume=drink.volume).price * drink.quantity

            for snack in order.snacks.all():
               cart_price += snack.price * snack.quantity

            for sauce in order.sauces.all():
               cart_price += sauce.price * sauce.quantity

            for _set in order.sets.all():
               cart_price += _set.price * _set.quantity
   else:
      temp_order = None




   num_visits=request.session.get('num_visits', 0)
   request.session['num_visits'] = num_visits+1

   total_amount = 0
   if temp_order!=None:
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

   product_counter_text = plural_ru.ru(total_amount, ["товар","товара", "товаров"])

   return render(request, 'main/index.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "total_amount":total_amount, "product_counter_text":product_counter_text, "cashback":cashback, "header_images":header_images, "mobile_image":HeaderMobileImage.objects.get(pk=1)})

def removeProduct(request):
   user_num = request.session.get('user')

   if request.is_ajax:

      if request.POST.get("object") == "pizza":
         pizza_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         pizza = get_object_or_404(TempPizza, pk=pizza_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.pizzas.remove(pizza)

         return HttpResponse("Pizza removed from order " + str(order_num) + " " + str(pizza.quantity) + " " + str(pizza.price) )
      elif request.POST.get("object") == "drink":
         drink_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         drink = get_object_or_404(TempDrink, pk=drink_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.drinks.remove(drink)

         return HttpResponse("Drink removed from order " + str(order_num) + " " + str(drink.quantity) + " " + str(drink.price))
      elif request.POST.get("object") == "snack":
         snack_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         snack = get_object_or_404(TempSnack, pk=snack_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.snacks.remove(snack)

         return HttpResponse("Snack removed from order " + str(order_num) + " " + str(snack.quantity) + " " + str(snack.price))
      elif request.POST.get("object") == "sauce":
         sauce_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         sauce = get_object_or_404(TempSauce, pk=sauce_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.sauces.remove(sauce)

         return HttpResponse("Sauce removed from order " + str(order_num) + " " + str(sauce.quantity) + " " + str(sauce.price))
      elif request.POST.get("object") == "set":
         set_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         _set = get_object_or_404(TempSet, pk=set_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.sets.remove(_set)

         return HttpResponse("Set removed from order " + str(order_num) + " " + str(_set.quantity) + " " + str(_set.price))
      elif request.POST.get("object") == "present":
         present_num = int(request.POST.get("number"))
         order_num = int(request.POST.get("order_number"))

         present = get_object_or_404(TempPresent, pk=present_num)
         order = get_object_or_404(TempOrder, pk=order_num)

         order.presents.remove(present)

         return HttpResponse("Present removed from order " + str(order_num) + " " + str(present.quantity) + " " + str(present.price))
         

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
               return HttpResponse(str(temp_pizza.id) + " " + str(temp_order.id) + " "  + str(temp_pizza.doughType) + " " + str(temp_pizza.size) + " " + str(temp_pizza.price))
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.pizzas.add(get_object_or_404(TempPizza, pk=temp_pizza.id))
         return HttpResponse(str(temp_pizza.id) + " " + str(temp_order.id) + " "  + str(temp_pizza.doughType) + " " + str(temp_pizza.size) + " " + str(temp_pizza.price))

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
               return HttpResponse(str(temp_drink.id) + " " + str(temp_order.id) + " "  + str(temp_drink.volume) +  " " + str(temp_drink.price))
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.drinks.add(get_object_or_404(TempDrink, pk=temp_drink.id))

         return HttpResponse(str(temp_drink.id) + " " + str(temp_order.id) + " "  + str(temp_drink.volume) +  " " + str(temp_drink.price))
         

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
               return HttpResponse(str(temp_snack.id) + " " + str(temp_order.id) +  " " + str(temp_snack.price))
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.snacks.add(get_object_or_404(TempSnack, pk=temp_snack.id))
         return HttpResponse(str(temp_snack.id) + " " + str(temp_order.id) +  " " + str(temp_snack.price))


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
               return HttpResponse(str(temp_sauce.id) + " " + str(temp_order.id) +  " " + str(temp_sauce.price))
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.sauces.add(get_object_or_404(TempSauce, pk=temp_sauce.id))

         return HttpResponse(str(temp_sauce.id) + " " + str(temp_order.id) +  " " + str(temp_sauce.price))
         

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
               return HttpResponse(str(temp_set.id) + " " + str(temp_order.id) +  " " + str(temp_set.price))
               
               break
      
         order_quantity = len(TempOrder.objects.all())
         temp_order = TempOrder()
         temp_order.title = order_quantity + 1
         temp_order.user = get_object_or_404(AnonymousUser, pk=user_num)
         temp_order.save(force_insert=True)
         temp_order.sets.add(get_object_or_404(TempSet, pk=temp_set.id))

         return HttpResponse(str(temp_set.id) + " " + str(temp_order.id) +  " " + str(temp_set.price))
         
      

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

         

         return HttpResponse(str(changing_model.quantity) + " " + str(changing_model.price))

      elif operation == "minus":
         order = get_object_or_404(TempOrder, pk=order_number)

         



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

            return HttpResponse("removed " + str(changing_model.price))

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

            return HttpResponse("removed " + str(changing_model.price))
         else:
            if changing_model.quantity!=0:
               changing_model.quantity = changing_model.quantity - 1
               changing_model.save()

            

            return HttpResponse(str(changing_model.quantity) + " " + str(changing_model.price))


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
   total_amount = 0


   temp_order = None

   try:
      cashback = User.objects.get(link=user_num).cashback
   except Exception as e:
      cashback = "0"

   header_images = HeaderImage.objects.all()

   if len(temp_orders)>0:
      for order in temp_orders:
         if order.user.id == user_num:
            temp_order = get_object_or_404(TempOrder, pk=order.id)

            for pizza in order.pizzas.all():
               cart_price += PriceForSize.objects.filter(pizza=pizza.elder_pizza.id).get(size=pizza.size).price * pizza.quantity

            for drink in order.drinks.all():
               cart_price += PriceForVolume.objects.filter(drink=drink.elder_drink.id).get(volume=drink.volume).price * drink.quantity

            for snack in order.snacks.all():
               cart_price += snack.price * snack.quantity

            for sauce in order.sauces.all():
               cart_price += sauce.price * sauce.quantity

            for _set in order.sets.all():
               cart_price += _set.price * _set.quantity
   else:
      temp_order = None




   num_visits=request.session.get('num_visits', 0)
   request.session['num_visits'] = num_visits+1

   total_amount = 0
   if temp_order!=None:
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

   
   product_counter_text = plural_ru.ru(total_amount, ["товар","товара", "товаров"])


   
   

   return render(request, 'main/cart.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount, "presents": presents, "product_counter_text":product_counter_text,"cashback":cashback, "header_images":header_images, "mobile_image":HeaderMobileImage.objects.get(pk=1)})

   


      
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

   temp_order = None

   try:
      cashback = User.objects.get(link=user_num).cashback
   except Exception as e:
      cashback = "0"

   header_images = HeaderImage.objects.all()
   if len(temp_orders)>0:
      for order in temp_orders:
         if order.user.id == user_num:
            temp_order = get_object_or_404(TempOrder, pk=order.id)

            for pizza in order.pizzas.all():
               cart_price += PriceForSize.objects.filter(pizza=pizza.elder_pizza.id).get(size=pizza.size).price * pizza.quantity

            for drink in order.drinks.all():
               cart_price += PriceForVolume.objects.filter(drink=drink.elder_drink.id).get(volume=drink.volume).price * drink.quantity

            for snack in order.snacks.all():
               cart_price += snack.price * snack.quantity

            for sauce in order.sauces.all():
               cart_price += sauce.price * sauce.quantity

            for _set in order.sets.all():
               cart_price += _set.price * _set.quantity
   else:
      temp_order = None




   num_visits=request.session.get('num_visits', 0)
   request.session['num_visits'] = num_visits+1

   total_amount = 0
   if temp_order!=None:
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

   product_counter_text = plural_ru.ru(total_amount, ["товар","товара", "товаров"])

   return render(request, 'main/discounts.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount, "discounts": discounts, "product_counter_text":product_counter_text, "cashback":cashback, "header_images":header_images, "mobile_image":HeaderMobileImage.objects.get(pk=1)})

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

   temp_order = None

   try:
      cashback = User.objects.get(link=user_num).cashback
   except Exception as e:
      cashback = "0"

   header_images = HeaderImage.objects.all()

   if len(temp_orders)>0:
      for order in temp_orders:
         if order.user.id == user_num:
            temp_order = get_object_or_404(TempOrder, pk=order.id)

            for pizza in order.pizzas.all():
               cart_price += PriceForSize.objects.filter(pizza=pizza.elder_pizza.id).get(size=pizza.size).price * pizza.quantity

            for drink in order.drinks.all():
               cart_price += PriceForVolume.objects.filter(drink=drink.elder_drink.id).get(volume=drink.volume).price * drink.quantity

            for snack in order.snacks.all():
               cart_price += snack.price * snack.quantity

            for sauce in order.sauces.all():
               cart_price += sauce.price * sauce.quantity

            for _set in order.sets.all():
               cart_price += _set.price * _set.quantity
   else:
      temp_order = None




   num_visits=request.session.get('num_visits', 0)
   request.session['num_visits'] = num_visits+1

   total_amount = 0
   if temp_order!=None:
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

   product_counter_text = plural_ru.ru(total_amount, ["товар","товара", "товаров"])
   

   return render(request, 'main/vacancy.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount, "vacancies": pagination.page(pk).object_list,"page_count":page_count, "current_page": current_page, "prev":prev_page, "next":next_page, "product_counter_text":product_counter_text, "cashback":cashback, "header_images":header_images, "mobile_image":HeaderMobileImage.objects.get(pk=1)})



def blog_view(request, pk):

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

   temp_order = None

   try:
      cashback = User.objects.get(link=user_num).cashback
   except Exception as e:
      cashback = "0"

   header_images = HeaderImage.objects.all()

   if len(temp_orders)>0:
      for order in temp_orders:
         if order.user.id == user_num:
            temp_order = get_object_or_404(TempOrder, pk=order.id)

            for pizza in order.pizzas.all():
               cart_price += PriceForSize.objects.filter(pizza=pizza.elder_pizza.id).get(size=pizza.size).price * pizza.quantity

            for drink in order.drinks.all():
               cart_price += PriceForVolume.objects.filter(drink=drink.elder_drink.id).get(volume=drink.volume).price * drink.quantity

            for snack in order.snacks.all():
               cart_price += snack.price * snack.quantity

            for sauce in order.sauces.all():
               cart_price += sauce.price * sauce.quantity

            for _set in order.sets.all():
               cart_price += _set.price * _set.quantity
   else:
      temp_order = None




   num_visits=request.session.get('num_visits', 0)
   request.session['num_visits'] = num_visits+1

   total_amount = 0
   if temp_order!=None:
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

   product_counter_text = plural_ru.ru(total_amount, ["товар","товара", "товаров"])
   

   return render(request, 'main/blog.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount, "posts": posts, "page_count":page_count, "next": next_page, "prev": prev_page, "current_page": current_page, "product_counter_text":product_counter_text, "cashback":cashback, "header_images":header_images, "mobile_image":HeaderMobileImage.objects.get(pk=1)})


def blog_view_detailed(request, pk):
   pizzas = Pizza.objects.all()

   drinks = Drink.objects.all()


   post = BlogPost.objects.get(pk=pk)

   volume = Volume.objects.all()
   pricesFS = PriceForSize.objects.all()
   pricesFV = PriceForVolume.objects.all()

   snacks = Snack.objects.all()
   sauces = Sauce.objects.all()

   sets = Set.objects.all()

   user_num = request.session.get('user')
   cart_price = 0
   cart_num = 0
   temp_order = None

   try:
      cashback = User.objects.get(link=user_num).cashback
   except Exception as e:
      cashback = "0"

   header_images = HeaderImage.objects.all()
   temp_orders = TempOrder.objects.all()
   if len(temp_orders)>0:
      for order in temp_orders:
         if order.user.id == user_num:
            temp_order = get_object_or_404(TempOrder, pk=order.id)

            for pizza in order.pizzas.all():
               cart_price += PriceForSize.objects.filter(pizza=pizza.elder_pizza.id).get(size=pizza.size).price * pizza.quantity

            for drink in order.drinks.all():
               cart_price += PriceForVolume.objects.filter(drink=drink.elder_drink.id).get(volume=drink.volume).price * drink.quantity

            for snack in order.snacks.all():
               cart_price += snack.price * snack.quantity

            for sauce in order.sauces.all():
               cart_price += sauce.price * sauce.quantity

            for _set in order.sets.all():
               cart_price += _set.price * _set.quantity
   else:
      temp_order = None




   num_visits=request.session.get('num_visits', 0)
   request.session['num_visits'] = num_visits+1

   total_amount = 0
   if temp_order!=None:
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

   product_counter_text = plural_ru.ru(total_amount, ["товар","товара", "товаров"])
   

   return render(request, 'main/blog-single.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount, "post": post,"product_counter_text":product_counter_text, "cashback":cashback, "header_images":header_images, "mobile_image":HeaderMobileImage.objects.get(pk=1)})

def contact_view(request):
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
   temp_order = None

   try:
      cashback = User.objects.get(link=user_num).cashback
   except Exception as e:
      cashback = "0"

   header_images = HeaderImage.objects.all()


   if len(temp_orders)>0:
      for order in temp_orders:
         if order.user.id == user_num:
            temp_order = get_object_or_404(TempOrder, pk=order.id)

            for pizza in order.pizzas.all():
               cart_price += PriceForSize.objects.filter(pizza=pizza.elder_pizza.id).get(size=pizza.size).price * pizza.quantity

            for drink in order.drinks.all():
               cart_price += PriceForVolume.objects.filter(drink=drink.elder_drink.id).get(volume=drink.volume).price * drink.quantity

            for snack in order.snacks.all():
               cart_price += snack.price * snack.quantity

            for sauce in order.sauces.all():
               cart_price += sauce.price * sauce.quantity

            for _set in order.sets.all():
               cart_price += _set.price * _set.quantity
   else:
      temp_order = None




   num_visits=request.session.get('num_visits', 0)
   request.session['num_visits'] = num_visits+1

   total_amount = 0
   if temp_order!=None:
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
   product_counter_text = plural_ru.ru(total_amount, ["товар","товара", "товаров"])
   

   return render(request, 'main/contact.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount, "product_counter_text":product_counter_text, "cashback":cashback, "header_images":header_images, "mobile_image":HeaderMobileImage.objects.get(pk=1)})

def about_view(request):
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
   temp_order = None

   try:
      cashback = User.objects.get(link=user_num).cashback
   except Exception as e:
      cashback = "0"

   header_images = HeaderImage.objects.all()

   temp_orders = TempOrder.objects.all()


   if len(temp_orders)>0:
      for order in temp_orders:
         if order.user.id == user_num:
            temp_order = get_object_or_404(TempOrder, pk=order.id)

            for pizza in order.pizzas.all():
               cart_price += PriceForSize.objects.filter(pizza=pizza.elder_pizza.id).get(size=pizza.size).price * pizza.quantity

            for drink in order.drinks.all():
               cart_price += PriceForVolume.objects.filter(drink=drink.elder_drink.id).get(volume=drink.volume).price * drink.quantity

            for snack in order.snacks.all():
               cart_price += snack.price * snack.quantity

            for sauce in order.sauces.all():
               cart_price += sauce.price * sauce.quantity

            for _set in order.sets.all():
               cart_price += _set.price * _set.quantity
   else:
      temp_order = None




   num_visits=request.session.get('num_visits', 0)
   request.session['num_visits'] = num_visits+1

   total_amount = 0
   if temp_order!=None:
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
      
   product_counter_text = plural_ru.ru(total_amount, ["товар","товара", "товаров"])
   

   return render(request, 'main/about.html', {'pizzas' : pizzas, 'drinks' : drinks,'number': num_visits,'m_volume': volume, "pricesFS": pricesFS, "pricesFV": pricesFV, "snacks" : snacks, "sauces" : sauces, "sets" : sets, "cart": temp_order, "cart_price" : cart_price, "cart_num": cart_num, "total_amount":total_amount,"product_counter_text":product_counter_text, "cashback":cashback, "header_images":header_images, "mobile_image":HeaderMobileImage.objects.get(pk=1)})


def newOrderView(request):

   name = request.POST.get("name")
   phone = request.POST.get("phone").replace(" ", "").replace("-", "").replace("+", "")
   place = request.POST.get("place")
   info = request.POST.get("info")

   user_num = request.session.get('user')


   try:
      actual_user = User.objects.get(phone=phone)
   except Exception as e:
      actual_user = User()
      actual_user.cashback = 0


   actual_user.name = name
   actual_user.phone = phone
   
   actual_user.link = AnonymousUser.objects.get(pk=user_num)


   actual_user.save()


   user_num = request.session.get('user')

   temp_orders = TempOrder.objects.all()
   if len(temp_orders)>0:
      for order in temp_orders:
         if order.user.id == user_num:
            temp_order = get_object_or_404(TempOrder, pk=order.id)

   actual_order = Order()
   order_quantity = len(Order.objects.all())

   actual_order.title = order_quantity + 1
   actual_order.address = place
   actual_order.user = actual_user
   actual_order.info = info



   actual_order.save()


   for element in temp_order.pizzas.all():
      actual_order.pizzas.add(element)
   for element in temp_order.drinks.all():
      actual_order.drinks.add(element)
   for element in temp_order.snacks.all():
      actual_order.snacks.add(element)
   for element in temp_order.sauces.all():
      actual_order.sauces.add(element)
   for element in temp_order.sets.all():
      actual_order.sets.add(element)
   for element in temp_order.presents.all():
      actual_order.presents.add(element)

   temp_order.delete()

   return HttpResponse("Order created. Temp order deleted")


def AdminPanelView(request, pk):
   if request.user.is_authenticated:

      orders = Order.objects.all().order_by("pk").reverse()
      visible_order_list = []

      for order in orders:
         if order.visible:
            visible_order_list.append(order)

      pagination = Paginator(visible_order_list, 6)
      count = len(visible_order_list)


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


      return render(request, 'main/admin_panel.html', {'current_page': current_page, 'next': next_page, 'prev':prev_page, 'page_count':page_count, "orders": pagination.page(pk).object_list,"count":count})
   else:
      return HttpResponse("Access denied", status=404)

   
def AdminPanelViewSingle(request, pk):
   if request.user.is_authenticated:
      order = Order.objects.get(pk=pk)

      return render(request, 'main/admin_panel_single.html', {"order": order})
   else:
      return HttpResponse("Access denied", status=404)
   
   
def orderCountView(request):
   if request.user.is_authenticated:
      count = len(list(Order.objects.all()))

      return HttpResponse(count, status=200)
   else:
      return HttpResponse("Access denied", status=404)
               
def getOrderView(request, pk):
   if request.user.is_authenticated:
      order = Order.objects.get(title=pk)

      return HttpResponse("{} {} {} {}".format(order.id, order.title, order.user, order.created_date), status=200)
   else:
      return HttpResponse("Access denied", status=404)


def url_redirect(request):
   url = request.path_info
   if "blog" in url:
      redirect_url = "/blog/1/"
   elif "vacancy" in url:
      redirect_url = "/vacancy/1/"
   else:
      redirect_url = "/admin_panel/1/"


   return HttpResponsePermanentRedirect(redirect_url)

def toggleOrder_view(request, pk):
   if request.user.is_authenticated:
      order = Order.objects.get(title=pk)
      temp_orders = TempOrder.objects.all()
   
      cart_price = 0
      for pizza in order.pizzas.all():
         cart_price += pizza.price * pizza.quantity

      for drink in order.drinks.all():
         cart_price += drink.price * drink.quantity

      for snack in order.snacks.all():
         cart_price += snack.price * snack.quantity

      for sauce in order.sauces.all():
         cart_price += sauce.price * sauce.quantity

      for _set in order.sets.all():
         cart_price += _set.price * _set.quantity

      cashback = cart_price*0.1

      if order.active:
         order.active = False
         order.save()
         
         user = order.user
         user.cashback = user.cashback - cashback
         user.save()

      else:
         order.active = True
         order.save()
         
         user = order.user
         user.cashback = user.cashback + cashback
         user.save()




      return HttpResponse("{} {} {}".format(order.active, user, user.cashback), status=200)
   else:
      return HttpResponse("Access denied", status=404)

def closeOrder_view(request, pk):
   if request.user.is_authenticated:
      try:
         temp_order = Order.objects.get(title=pk)
         actual_order = ArchievedOrder()

         actual_order.user = temp_order.user
         actual_order.title = temp_order.title
         actual_order.address = temp_order.address
         actual_order.info = temp_order.info
         actual_order.active = False

         

         actual_order.created_date = temp_order.created_date
         actual_order.state = temp_order.state
         actual_order.save()

         for element in temp_order.pizzas.all():
            actual_order.pizzas.add(element)
         for element in temp_order.drinks.all():
            actual_order.drinks.add(element)
         for element in temp_order.snacks.all():
            actual_order.snacks.add(element)
         for element in temp_order.sauces.all():
            actual_order.sauces.add(element)
         for element in temp_order.sets.all():
            actual_order.sets.add(element)
         for element in temp_order.presents.all():
            actual_order.presents.add(element)

         temp_order.visible = False;
         temp_order.save()



         return HttpResponse("Order archieved", status=200)
      except Exception as e:
         return HttpResponse(str(e), status=500)


   else:
      return HttpResponse("Access denied", status=404)

def archievedordersView(request, pk):
   if request.user.is_authenticated:

      orders = ArchievedOrder.objects.all().order_by("pk").reverse()
      count = len(list(ArchievedOrder.objects.all()))
      pagination = Paginator(orders, 6)

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


      return render(request, 'main/admin_panel_archieve.html', {'current_page': current_page, 'next': next_page, 'prev':prev_page, 'page_count':page_count, "orders": pagination.page(pk).object_list,"count":count})
   else:
      return HttpResponse("Access denied", status=404)

def AdminPanelViewArchievedSingle(request, pk):
   if request.user.is_authenticated:
      order = ArchievedOrder.objects.get(pk=pk)

      return render(request, 'main/admin_panel_single.html', {"order": order})
   else:
      return HttpResponse("Access denied", status=404)