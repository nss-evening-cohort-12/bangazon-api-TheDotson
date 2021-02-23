import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection


def incomplete_orders(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT 
                  o.id order_id,
                  SUM(pr.price) total_price, a.first_name || ' ' || a.last_name AS full_name

                FROM bangazonapi_order o
                JOIN bangazonapi_orderproduct op
                ON o.id = op.order_id
                JOIN bangazonapi_product pr 
                ON op.product_id = pr.id
                JOIN bangazonapi_customer c 
                ON o.customer_id = c.id 
                JOIN auth_user a
                ON c.user_id = a.id
                WHERE o.payment_type_id IS NULL
                GROUP BY o.id
            """)

            dataset = db_cursor.fetchall()

            order_list = {}

            for row in dataset:
              order = Order()
              order_id = row["order_id"]
              full_name = row["full_name"]
              price = row["total_price"]
              order_list.append(product)

        template = 'orders/incomplete_orders.html'
        context = {'incomplete_orders': order_list}

        return render(request, template, context)
