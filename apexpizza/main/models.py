from django.db import models
from django.utils import timezone

"""

Модели пиццы и около пиццы

"""

class Topping(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Актуально", default=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Топпинг"
        verbose_name_plural = "Топпинги"

class Size(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Актуально", default=False)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Размер пиццы"
        verbose_name_plural = "Размеры пиццы"

class DoughType(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Актуально", default=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Тип теста для пицц"
        verbose_name_plural = "Типы теста для пицц"



class Pizza(models.Model):

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    picture = models.ImageField("Фото", blank=True, null=True, upload_to="pictures/")

    active = models.BooleanField("Актуально", default=False)

    toppings = models.ManyToManyField(Topping, verbose_name="Топпинги")

    available = models.ManyToManyField(Size, verbose_name="Доступные размеры")

    doughType = models.ManyToManyField(DoughType, verbose_name="Тип теста")

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Пицца"
        verbose_name_plural = "Пиццы"

class PriceForSize(models.Model):

    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, default = 1, verbose_name="Пицца")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default = 1, verbose_name="Размер")

    price = models.FloatField("Цена", default=0)


    def __str__(self):
        return str(self.pizza.title) + " - " + str(self.size)

    class Meta:
        verbose_name = "Цена для размера пицц"
        verbose_name_plural = "Цены для размеров пицц"



"""

Модель напитков

"""
class Volume(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    active = models.BooleanField("Актуально", default=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Объём"
        verbose_name_plural = "Объёмы"

class Drink(models.Model):

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    picture = models.ImageField("Фото", blank=True, null=True, upload_to="pictures/")
    
    active = models.BooleanField("Актуально", default=False)

    available = models.ManyToManyField(Volume, verbose_name="Доступные объёмы")

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Напиток"
        verbose_name_plural = "Напитки"


class PriceForVolume(models.Model):

    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, default = 1, verbose_name="Напиток")

    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, default = 1, verbose_name="Объём")

    price = models.FloatField("Цена", default=0)


    def __str__(self):
        return str(self.drink.title) + " - " + str(self.volume)

    class Meta:
        verbose_name = "Цена для объёма напитка"
        verbose_name_plural = "Цены для объёмов напитков"

"""

Модели закусок и соусов

"""

class Snack(models.Model):

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    picture = models.ImageField("Фото", blank=True, null=True, upload_to="pictures/")

    active = models.BooleanField("Актуально", default=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Закуска"
        verbose_name_plural = "Закуски"


class Sauce(models.Model):

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    picture = models.ImageField("Фото", blank=True, null=True, upload_to="pictures/")

    active = models.BooleanField("Актуально", default=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Соус"
        verbose_name_plural = "Соусы"

"""

Модель сета

"""

class Set(models.Model):

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    picture = models.ImageField("Фото", blank=True, null=True, upload_to="pictures/")

    active = models.BooleanField("Актуально", default=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Сет"
        verbose_name_plural = "Сеты"

"""

Модель временного пользователя

"""
class AnonymousUser(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    
    cashback = models.PositiveIntegerField()

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Анонимный пользователь"
        verbose_name_plural = "Анонимные пользователи"

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

    class Meta:
        verbose_name = "Временная пицца"
        verbose_name_plural = "Временные пицца"

class TempDrink(models.Model):

    elder_drink = models.ForeignKey(Drink, on_delete=models.CASCADE, default=1)

    quantity = models.PositiveIntegerField(default=1)

    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    
    price = models.FloatField("Цена", default=0)

    volume = models.ForeignKey(Volume, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Временный напиток"
        verbose_name_plural = "Временные напитки"

class TempSnack(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    quantity = models.PositiveIntegerField(default=1)

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Временная закуска"
        verbose_name_plural = "Временные закуски"

class TempSauce(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    quantity = models.PositiveIntegerField(default=1)

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Временный соус"
        verbose_name_plural = "Временные соусы"

class TempSet(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to="pictures/")

    quantity = models.PositiveIntegerField(default=1)

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Временный сет"
        verbose_name_plural = "Временные сеты"

class Present(models.Model):

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    price = models.FloatField("Цена", default=0)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Подарок"
        verbose_name_plural = "Подарки"

class TempPresent(models.Model):

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    price = models.FloatField("Цена", default=0)

    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Временный подарок"
        verbose_name_plural = "Временные подарки"

class TempOrder(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)  

    pizzas = models.ManyToManyField(TempPizza) 
    drinks = models.ManyToManyField(TempDrink)
    snacks = models.ManyToManyField(TempSnack)
    sauces = models.ManyToManyField(TempSauce)
    sets = models.ManyToManyField(TempSet, related_name="sets")
    presents = models.ManyToManyField(TempPresent)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Временный заказ"
        verbose_name_plural = "Временные заказы"

class Discount(models.Model):
    title = models.TextField("Название")
    picture = models.ImageField("Фото", blank=True, null=True, upload_to="pictures/")

    active = models.BooleanField("Актуально", default=False)


    description = models.TextField("Описание")

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

class Vacancy(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    picture = models.ImageField("Фото", blank=True, null=True, upload_to="pictures/")

    active = models.BooleanField("Актуально", default=False)


    start = models.CharField("Начало рабочего дня", max_length=511, default="", unique=False, null=False)
    end = models.CharField("Конец рабочего дня", max_length=511, default="", unique=False, null=False)

    dinner_start = models.CharField("Начало обеденного времени", max_length=511, default="", unique=False, null=False)
    dinner_end = models.CharField("Конец обеденного времени", max_length=511, default="", unique=False, null=False)

    salary = models.PositiveIntegerField("Заработная плата")
    year = models.PositiveIntegerField("Стаж работы")

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


class BlogPost(models.Model):
    title = models.TextField("Название")
    picture = models.ImageField("Фото",blank=True, null=True, upload_to="pictures/")

    active = models.BooleanField("Актуально", default=False)

    show_body = models.TextField("Описание",default="")
    body = models.TextField("Текст поста",default="")

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Пост блога"
        verbose_name_plural = "Посты блога"

class User(models.Model):

    name = models.TextField("Имя")

    phone = models.CharField("Номер телефона", max_length=20, default="", unique=False, null=False)


    cashback = models.PositiveIntegerField()

    link = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

class OrderState(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Состояние заказа"
        verbose_name_plural = "Состояния заказа"
    
class Order(models.Model):
    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    visible = models.BooleanField("Показывать", default=True)

    address = models.TextField("Адрес")

    info = models.TextField("Инфо")

    active = models.BooleanField("Актуально", default=False)

    pizzas = models.ManyToManyField(TempPizza) 
    drinks = models.ManyToManyField(TempDrink)
    snacks = models.ManyToManyField(TempSnack)
    sauces = models.ManyToManyField(TempSauce)
    sets = models.ManyToManyField(TempSet)
    presents = models.ManyToManyField(TempPresent)

    created_date = models.DateTimeField(default=timezone.now)

    state = models.ForeignKey(OrderState, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class HeaderImage(models.Model):
    title = models.TextField("Название")
    picture = models.ImageField("Фото", blank=True, null=True, upload_to="pictures/")

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Фото для слайдера"
        verbose_name_plural = "Фото для слайдера"

class HeaderMobileImage(models.Model):
    picture = models.ImageField("Фото", blank=True, null=True, upload_to="pictures/")

    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name = "Фото для мобильного Header"
        verbose_name_plural = "Фото для мобильного Header"


class ArchievedOrder(models.Model):

    title = models.CharField("Название", max_length=511, default="", unique=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")


    address = models.TextField("Адрес", default="")

    info = models.TextField("Инфо", default="")

    active = models.BooleanField("Актуально", default=False)

    pizzas = models.ManyToManyField(TempPizza) 
    drinks = models.ManyToManyField(TempDrink)
    snacks = models.ManyToManyField(TempSnack)
    sauces = models.ManyToManyField(TempSauce)
    sets = models.ManyToManyField(TempSet)
    presents = models.ManyToManyField(TempPresent)

    created_date = models.DateTimeField(default=timezone.now)

    state = models.ForeignKey(OrderState, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Архивированный заказ"
        verbose_name_plural = "Архивированные заказы"

        


