from django.urls import path
from .views import expensive_products, inexpensive_products, incomplete_orders, completed_orders, favorite_sellers

urlpatterns = [
    path('reports/expensive', expensive_products),
    path('reports/inexpensive', inexpensive_products),
    path('reports/incomplete', incomplete_orders),
    path('reports/complete', completed_orders),
    path('reports/favorites', favorite_sellers)
]
