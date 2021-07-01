from django import forms
from .models import product

class productForm(forms.ModelForm):

    class Meta:
        model = product
        fields = ['sku_id','name','mrp','exp_date','qty']

