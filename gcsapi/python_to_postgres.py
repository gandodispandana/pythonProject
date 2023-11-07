import ast

import psycopg2

conn = psycopg2.connect(database="GCS",
                        host="localhost",
                        user="postgres",
                        password="spandu@194",
                        port="5432")


def joinUserAndRestaurants(cur, city, order='asc'):
    cursor = cur.cursor()
    sql_context = """select usser.username, restaurant.restaurant_name from usser inner join restaurant on usser.city =
                  restaurant.city where usser.city =%s order by usser.username, restaurant.restaurant_name """ + order
    data = [city]
    print(data)
    cursor.execute(sql_context, data)
    print(sql_context)
    result = cursor.fetchall()
    print(result)


joinUserAndRestaurants(conn, 'tokyo')
