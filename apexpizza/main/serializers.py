from rest_framework import serializers
from .models import TempOrder




class TempOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempOrder
        fields = ('user', 'pizzas', 'drinks', 'snacks', 'sauces', 'sets')