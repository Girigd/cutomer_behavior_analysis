import mysql.connector
import pandas as pd

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql@123",
    database="customer_data"
)

"""query = "SELECT * FROM customers"

df = pd.read_sql(query, connection)

print(df.head())
"""
print("Hhhh")
connection.close()