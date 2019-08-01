from django.db import models

"""

Модели пиццы и около пиццы

"""

class Topping(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Активен", default=False)

    def __str__(self):
        return str(self.title)

class Size(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Активен", default=False)

    def __str__(self):
        return str(self.title)

class DoughType(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Активен", default=False)

    def __str__(self):
        return str(self.title)



class Pizza(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Активен", default=False)

    toppings = models.ManyToManyField(Topping)

    available = models.ManyToManyField(Size)

    doughType = models.ManyToManyField(DoughType)

    def __str__(self):
        return str(self.title)

class PriceForSize(models.Model):

    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, default = 1)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default = 1)

    price = models.FloatField("Цена", default=0)


    def __str__(self):
        return str(self.pizza.title) + " - " + str(self.size)



"""

Модель напитков

"""
class Volume(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Активен", default=False)

    def __str__(self):
        return str(self.title)

class Drink(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    
    active = models.BooleanField("Активен", default=False)
    available = models.ManyToManyField(Volume)

    def __str__(self):
        return str(self.title)


class PriceForVolume(models.Model):

    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, default = 1)
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, default = 1)

    price = models.FloatField("Цена", default=0)


    def __str__(self):
        return str(self.drink.title) + " - " + str(self.volume)

"""

Модели закусок и соусов

"""

class Snack(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Активен", default=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)


class Sauce(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Активен", default=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

"""

Модель сета

"""

class Set(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Активен", default=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

"""

Модель временного пользователя

"""
class AnonymousUser(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    
    cashback = models.PositiveIntegerField()

    def __str__(self):
        return str(self.title)

"""

Модель временного заказа

"""
class TempPizza(models.Model):
    elder_pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, default=1)

    quantity = models.PositiveIntegerField(default=1)

    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    toppings = models.ManyToManyField(Topping)

    size = models.ForeignKey(Size, on_delete=models.CASCADE, default=3)

    doughType = models.ForeignKey(DoughType, on_delete=models.CASCADE, default=2)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

class TempDrink(models.Model):

    elder_drink = models.ForeignKey(Drink, on_delete=models.CASCADE, default=1)

    quantity = models.PositiveIntegerField(default=1)

    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    
    price = models.FloatField("Цена", default=0)

    volume = models.ForeignKey(Volume, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

class TempSnack(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    quantity = models.PositiveIntegerField(default=1)

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

class TempSauce(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    quantity = models.PositiveIntegerField(default=1)

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

class TempSet(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    quantity = models.PositiveIntegerField(default=1)

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

class Present(models.Model):

    title = models.CharField("ID", max_length=511, default="", unique=False, null=False)
    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

class TempPresent(models.Model):

    title = models.CharField("ID", max_length=511, default="", unique=False, null=False)
    price = models.FloatField("Цена", default=0)

    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.title)

class TempOrder(models.Model):
    title = models.CharField("ID", max_length=511, default="", unique=False, null=False)
    user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)  

    pizzas = models.ManyToManyField(TempPizza) 
    drinks = models.ManyToManyField(TempDrink)
    snacks = models.ManyToManyField(TempSnack)
    sauces = models.ManyToManyField(TempSauce)
    sets = models.ManyToManyField(TempSet, related_name="sets")
    presents = models.ManyToManyField(TempPresent)

    def __str__(self):
        return str(self.title)

class Discount(models.Model):
    title = models.TextField()
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    active = models.BooleanField("Активен", default=False)


    description = models.TextField()

    def __str__(self):
        return str(self.title)

class Vacancy(models.Model):
    title = models.CharField("ID", max_length=511, default="", unique=False, null=False)
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    active = models.BooleanField("Активен", default=False)


    start = models.CharField("Начало рабочего дня", max_length=511, default="", unique=False, null=False)
    end = models.CharField("Конец рабочего дня", max_length=511, default="", unique=False, null=False)

    dinner_start = models.CharField("Начало обеденного времени", max_length=511, default="", unique=False, null=False)
    dinner_end = models.CharField("Конец обеденного времени", max_length=511, default="", unique=False, null=False)

    salary = models.PositiveIntegerField()
    year = models.PositiveIntegerField()




    def __str__(self):
        return str(self.title)


        


