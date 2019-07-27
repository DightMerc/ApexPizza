from rest_framework import serializers
from .models import TempOrder, Topping, TempDrink


class ToppingSerizlizer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=256)

class PizzaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    picture = serializers.CharField(max_length=256)
    title = serializers.CharField(max_length=256)

    toppings = ToppingSerizlizer(many=True, read_only=True)
    size = serializers.CharField(max_length=10)
    doughType = serializers.CharField()
    price = serializers.IntegerField()

class DrinkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    picture = serializers.CharField(max_length=256)
    title = serializers.CharField(max_length=256)
    price = serializers.IntegerField()

    class Meta:
        model = TempDrink
        fields = ('id', 'picture', 'title', 'price', 'volume')

class SnackSerializer(serializers.Serializer):
    picture = serializers.CharField(max_length=256)
    title = serializers.CharField(max_length=256)
    price = serializers.IntegerField()

class SauceSerializer(serializers.Serializer):
    picture = serializers.CharField(max_length=256)
    title = serializers.CharField(max_length=256)
    price = serializers.IntegerField()

class SetSerializer(serializers.Serializer):
    picture = serializers.CharField(max_length=256)
    title = serializers.CharField(max_length=256)
    price = serializers.IntegerField()

class AnonymousUserSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256)


class TempOrderSerializer(serializers.ModelSerializer):
    title = serializers.IntegerField()

    user = AnonymousUserSerializer()
    
    pizzas = PizzaSerializer(many=True, read_only=True)
    drinks = DrinkSerializer(many=True, read_only=True)
    snacks = SnackSerializer(many=True, read_only=True)
    sauces = SauceSerializer(many=True, read_only=True)
    sets = SetSerializer(many=True, read_only=True)

    class Meta:
        model = TempOrder
        fields = ('title', 'user', 'pizzas', 'drinks','snacks', 'sauces', 'sets')
        


