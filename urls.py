from django.urls import path

from . import views

urlpatterns = [
    path('sample', views.sample, name='total'),
    path('api/total_items', views.get_total_items, name='total_items'),
    path('api/nth_most_total_item', views.get_nth_most_total_item, name='nth_most_total_item'),
    path('api/percentage_of_department_wise_sold_items', views.get_percentage_of_department_wise_sold_items, name='percentage_of_department_wise_sold_items'),
    path('api/monthly_sales', views.get_monthly_sales, name='monthly_sales'),
]
