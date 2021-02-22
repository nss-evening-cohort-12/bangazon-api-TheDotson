import sqlite3
from django.shortcuts import render
from bangazonapi.models import Product
from bangazonreports.views import Connection

def expensive_products(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT 
                  p.name,
                  p.price

                FROM bangazonapi_product p
                WHERE p.price >= 1000
                ORDER BY p.price DESC
            """)

            dataset = db_cursor.fetchall()

            list_of_products = []

            for row in dataset:
                product = Product()
                product.name = row['name']
                product.price = row['price']
                list_of_products.append(product)

        template = 'products/expensive_products.html'
        context = {'expensive_products': list_of_products}

        return render(request, template, context)
