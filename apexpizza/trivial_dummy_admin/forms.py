from django import forms

from main.models import Pizza

class CreateNewPizza(forms.ModelForm):

    class Meta:
        model = Pizza
        fields = ('picture', 'title', 'active', 'toppings', 'available', 'doughType')