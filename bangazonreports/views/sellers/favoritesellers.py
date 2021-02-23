import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def favorite_sellers(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                  buyer.first_name || ' ' || buyer.last_name as Customer_Name,
                  seller.first_name || ' ' || seller.last_name as Favorite_Seller_Name

                FROM bangazonapi_favorite favorite
                JOIN bangazonapi_customer buyer_customer
                ON favorite.customer_id = buyer_customer.id
                JOIN auth_user buyer
                ON buyer.id =  buyer_customer.user_id
                JOIN bangazonapi_customer seller_customer
                ON favorite.seller_id = seller_customer.id
                JOIN auth_user seller
                ON seller.id = seller_customer.user_id
            """)

            dataset = db_cursor.fetchall()

            favorite_list = {}

            for row in dataset:
                buyer = row["Customer_Name"]
                seller = row["Favorite_Seller_Name"]

                if buyer in favorite_list:
                    favorite_list[buyer]['Favorites'].append(seller)
                else:
                    favorite_list[buyer] = {}
                    favorite_list[buyer]["Name"] = row["Customer_Name"]
                    favorite_list[buyer]['Favorites'] = [seller]


        favorites = favorite_list.values()
        template = 'sellers/favorite_sellers.html'
        context = {
            'favorite_sellers': favorites
        }

        return render(request, template, context)
