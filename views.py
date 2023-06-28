from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Sum
import requests
import json

# from assign1 import purchases

 

from .models import Purchase
from django.db import models
from django.core import serializers
import json


def sample(request):
    
    response = requests.get('https://example.com/api/data')

        
    print(json.loads(str(response)))


# API 1:
@require_GET
def get_total_items(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    department = request.GET.get('department')

 

    
    filtered_purchases = Purchase.objects.filter(
        date__gte=start_date,
        date__lte=end_date,
        department=department
    )

 

    
    total_items = filtered_purchases.aggregate(total_items=Sum('seats'))['total_items']

 

    return JsonResponse({'total_items': total_items})

 


# API 2:
@require_GET
def get_nth_most_total_item(request):
    item_by = request.GET.get('item_by')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    n = int(request.GET.get('n'))

 

   
    filtered_purchases = Purchase.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    )

 
    if item_by == 'quantity':
        item_sales = filtered_purchases.values('software').annotate(total_seats=Sum('seats')).order_by('-total_seats')
        if item_sales:
            nth_item = item_sales[min(n - 1, len(item_sales) - 1)]['software']
        else:
            return JsonResponse({'error': 'No items found in the given date range.'})
    elif item_by == 'price':
        item_sales = filtered_purchases.values('software').annotate(total_amount=Sum('amount')).order_by('-total_amount')
        if item_sales:
            nth_item = item_sales[min(n - 1, len(item_sales) - 1)]['software']
        else:
            return JsonResponse({'error': 'No items found in the given date range.'})
    else:
        return JsonResponse({'error': 'Invalid item_by parameter.'})


 


# API 3: 
@require_GET
def get_percentage_of_department_wise_sold_items(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

 

    
    filtered_purchases = Purchase.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    )

 

    
    department_sales = filtered_purchases.values('department').annotate(total_seats=Sum('seats'))
    total_sales = filtered_purchases.aggregate(total_seats=Sum('seats'))['total_seats']
    percentages = {entry['department']: entry['total_seats'] / total_sales * 100 for entry in department_sales}

 

    return JsonResponse({'percentages': percentages})

 


# API 4: 
@require_GET
def get_monthly_sales(request):
    product = request.GET.get('product')
    year = int(request.GET.get('year'))

 

    
    filtered_purchases = Purchase.objects.filter(
        software=product,
        date__year=year
    )

 

    
    monthly_sales = filtered_purchases.annotate(month=models.functions.ExtractMonth('date')).values('month').annotate(total_sales=Sum('amount')).order_by('month')

 

    
    monthly_sales_list = [entry['total_sales'] for entry in monthly_sales]

 

    return JsonResponse({'monthly_sales': monthly_sales_list})