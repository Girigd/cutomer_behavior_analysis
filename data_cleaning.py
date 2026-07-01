import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

user = "root"
password = quote_plus("mysql@123")
host = "127.0.0.1"
port = "3306"
database = "customer_data"

connection = mysql.connector.connect(
    host=host,
    user=user,
    password="mysql@123",
    database=database
)

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)


df= pd.read_csv("customer_shopping_behavior.csv")
df["Review Rating"] = df.groupby("Category")["Review Rating"].transform(lambda x: x.fillna(x.median()))
df.columns= df.columns.str.lower()
df.columns= df.columns.str.replace(' ','_')

df= df.rename(columns = {"purchase_amount_(usd)" : "purchase_amount"})
labels= ["Young_Adult","Adult","Middle_Aged","Senior"]
df["age_group"]= pd.qcut(df['age'], q=4, labels=labels)

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df["purchase_frequency_days"]= df['frequency_of_purchases'].map(frequency_mapping)

df= df.drop('promo_code_used' ,axis= 1)



"""query = "SELECT * FROM customers"

df = pd.read_sql(query, connection)

print(df.head())
"""

df.to_sql(
    name="customer_behavior",
    con=engine,
    if_exists="replace",   # Creates the table. Replaces it if it already exists.
    index=False
)

print("Data Loaded to Database Table")


connection.close()