from django.urls import path
from .views import expensive_products, inexpensive_products

urlpatterns = [
    path('reports/expensive', expensive_products),
    path('reports/inexpensive', inexpensive_products)
]
