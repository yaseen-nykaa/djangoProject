from rest_framework import serializers
from .models import product

class productSerializer(serializers.ModelSerializer):

    class Meta:
        model = product
        fields = ['sku_id','name','mrp','exp_date','qty']