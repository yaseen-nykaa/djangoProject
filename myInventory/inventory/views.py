from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.http import HttpResponse

from .models import product
from rest_framework import viewsets
from .serializers import productSerializer

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

import requests

BASE_URL = "http://localhost:8000/products/"

def isValid(prod):
    print("validity check for: ")
    print(prod)
    sku_id = prod['sku_id']
    name = prod['name']
    mrp = prod['mrp']
    qty = prod['qty']
    exp_date = prod['exp_date']

    # print("sku_id type = " + str(type(sku_id)))
    # print("name type = " + str(type(name)))
    # print("mrp type = " + str(type(mrp)))
    # print("qty type = " + str(type(qty)))

    if ((sku_id is not None) and (name is not None) and (mrp is not None)
            and (qty is not None) and (exp_date is not None)):
        if (int(sku_id) >= 0) and (float(mrp) >= 0.00) and (int(qty) >= 0):
            return True
    return False

# Create your views here.
def product_view(request):
    response = requests.get(BASE_URL)
    product_list = response.json()
    print("Product list" + str(product_list))
    context = {'product_list': product_list,}
    return render(request, 'inventory/products.html', context)

@api_view(['GET'])
def get_products(request):
    prods = product.objects.all()
    product_serializer = productSerializer(prods, many=True)
    return JsonResponse(product_serializer.data, safe=False)

@api_view(['GET'])
def prod_detail_view(request):
    sku_id = request.GET['skuId']
    prod = []
    prod.append(product.objects.get(sku_id=sku_id))
    print(type(prod))
    product_serializer = productSerializer(prod, many=True)
    return JsonResponse(product_serializer.data, safe=False)

@api_view(['POST'])
def prod_add_view(request):
    prod = JSONParser().parse(request)
    sku_id = prod['sku_id']
    try:
        original_prod = product.objects.get(sku_id=sku_id)
        return JsonResponse({'ERROR': 'Product with sku_id:' + str(sku_id) + ' already present in table'})
    except:
        if(isValid(prod)):
            product_serializer = productSerializer(data=prod)
            if product_serializer.is_valid():
                product_serializer.save()
                return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"ERROR": "Product data invalid or incomplete"}, status=status.HTTP_400_BAD_REQUEST)

# TODO: prepopulate the form fields
@api_view(['PUT','POST'])
def prod_update(request, sku_id):
    if request.method == 'PUT':
        try:
            prod = product.objects.get(sku_id=sku_id)
            prod_data = JSONParser().parse(request)

            try:
                name = prod_data['name']
                if(name != ""):
                    prod.name = name
                else:
                    return JsonResponse({"Error":"name sent is an empty string"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                pass

            try:
                mrp = prod_data['mrp']
                if(float(mrp) >= 0.00):
                    prod.mrp = float(mrp)
                else:
                    return JsonResponse({"Error": "incorrect mrp value"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                pass

            try:
                qty = prod_data['qty']
                if(int(qty) >= 0):
                    prod.qty = int(qty)
                else:
                    return JsonResponse({"Error": "incorrect qty value"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                pass

            try:
                exp_date = prod_data['exp_date']
                prod.exp_date = exp_date
            except:
                pass

            print(prod.__dict__)
            prod.save()
            return JsonResponse({"message":"product with sku_id " + str(sku_id) + " was updated"}, status=status.HTTP_200_OK)

            # if(isValid(prod_data)):
            #     prod_serializer = productSerializer(prod, data=prod_data)
            #     if prod_serializer.is_valid():
            #         prod_serializer.save()
            #         return JsonResponse(prod_serializer.data)
            # return JsonResponse(prod_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'ERROR': "product with sku_id " + str(sku_id) + " not found"},
                                status=status.HTTP_400_BAD_REQUEST)

    #
    elif request.method == 'POST':
        sku_id = request.POST['sku_id']
        try:
            prod = product.objects.get(sku_id=sku_id)
            name = request.POST['name']
            mrp = request.POST['mrp']
            qty = request.POST['qty']
            exp_date = request.POST['exp_date']
            if(name != ''):
                prod.name = name
            if(mrp != '-1'):
                prod.mrp = mrp
            if(qty != '-1'):
                prod.qty = qty
            if(exp_date != ""):
                prod.exp_date = exp_date
            # print("updated product:" + str(prod.__dict__))
            prod.save()
            return redirect(BASE_URL + "all/")
        except:
            return JsonResponse({'ERROR': "product with sku_id " + str(sku_id) + " not found"},
                                status=status.HTTP_400_BAD_REQUEST)

def prod_update_view(request, sku_id):
    prod = product.objects.get(sku_id=sku_id)
    return render(request, 'inventory/updateProduct.html', {'prod':prod})

@api_view(['DELETE'])
def prod_delete(request, sku_id):
    try:
        prod = product.objects.get(sku_id=sku_id)
        prod.delete()
        return JsonResponse({'message': "product with sku_id " + str(sku_id) + " was deleted"}, status=status.HTTP_204_NO_CONTENT)
    except:
        return JsonResponse({'ERROR': "product with sku_id " + str(sku_id) + " not found"}, status=status.HTTP_400_BAD_REQUEST)