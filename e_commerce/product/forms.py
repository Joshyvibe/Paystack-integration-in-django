from django import forms
from .models import Order


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'state', 'phone']
        exclude = ['total_cost']