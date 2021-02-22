from django.urls import path
from .views import expensive_products

urlpatterns = [
    path('reports/expensive', expensive_products)
]
