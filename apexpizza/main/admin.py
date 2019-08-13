from django.contrib import admin
from .models import Pizza, Topping, DoughType, Size
from .models import Drink, Sauce, Snack, Set, AnonymousUser, TempPizza, TempOrder, Volume, PriceForSize, TempDrink, PriceForVolume, TempSnack, TempSauce, TempSet, Present, TempPresent
from .models import Discount, Vacancy, BlogPost, User, Order, OrderState, HeaderImage, HeaderMobileImage, ArchievedOrder

# register your models here.
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(DoughType)
admin.site.register(Size)

admin.site.register(Drink)
admin.site.register(Sauce)
admin.site.register(Snack)

admin.site.register(Set)

admin.site.register(AnonymousUser)
admin.site.register(TempPizza)
admin.site.register(TempOrder)
admin.site.register(Volume)

admin.site.register(PriceForSize)
admin.site.register(TempDrink)
admin.site.register(PriceForVolume)
admin.site.register(TempSnack)
admin.site.register(TempSauce)
admin.site.register(TempSet)

admin.site.register(Present)
admin.site.register(TempPresent)

admin.site.register(Discount)
admin.site.register(Vacancy)
admin.site.register(BlogPost)

admin.site.register(User)
admin.site.register(Order)

admin.site.register(OrderState)
admin.site.register(HeaderImage)
admin.site.register(HeaderMobileImage)

admin.site.register(ArchievedOrder)



















