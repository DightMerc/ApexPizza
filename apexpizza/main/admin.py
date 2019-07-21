from django.contrib import admin
from .models import Pizza, Topping, DoughType, Size
from .models import Drink, Sauce, Snack, Set

# register your models here.
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(DoughType)
admin.site.register(Size)

admin.site.register(Drink)
admin.site.register(Sauce)
admin.site.register(Snack)

admin.site.register(Set)

