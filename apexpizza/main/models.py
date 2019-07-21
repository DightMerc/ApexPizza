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

    size = models.ManyToManyField(Size)

    doughType = models.ManyToManyField(DoughType)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)


"""

Модель напитков

"""

class Drink(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    
    active = models.BooleanField("Активен", default=False)

    price = models.FloatField("Цена", default=0)

    volume = models.FloatField("Объём", default=0)

    def __str__(self):
        return str(self.title)

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

    pizzas = models.ManyToManyField(Pizza)
    drinks = models.ManyToManyField(Drink)
    snacks = models.ManyToManyField(Snack)
    sauces = models.ManyToManyField(Sauce)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)