import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def incomplete_orders(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                  o.id as 'order',
                  u.first_name || ' ' || u.last_name as 'full name',
                  SUM(price) as 'total price'

                FROM bangazonapi_order o
                JOIN bangazonapi_customer c ON o.customer_id = c.id
                JOIN auth_user u ON u.id = c.user_id
                JOIN bangazonapi_orderproduct op ON op.order_id = o.id
                JOIN bangazonapi_product p ON p.id = op.product_id
                WHERE payment_type_id IS NULL
                GROUP BY o.id
                """)

            dataset = db_cursor.fetchall()

            incomplete_orders = []

            for row in dataset:
                order = {
                  'order_id': row['order'],
                  'full_name': row['full name'],
                  'total_price': row['total price']
                }
                incomplete_orders.append(order)

        template = 'orders/incomplete_orders.html'
        context = {'incomplete_orders': incomplete_orders}

        return render(request, template, context)
