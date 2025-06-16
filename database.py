import psycopg2

conn = psycopg2.connect(user="postgres",password="1112",host="localhost",port="5432",database="mduka") #used to connect

cur = conn.cursor() #object to execute sql quesries.

# cur.execute("select*from products") #method used to 
# products=cur.fetchall()
# print(products)

#READING DATA
#getting products and sales using function
def get_products():
   cur.execute("select*from products") #method used to 
   products=cur.fetchall()
   return products

def get_sales():
   cur.execute("select*from sales")
   sales = cur.fetchall()
   return sales


sales_data = get_sales()


print('sales data is', sales_data)

# Create
# Inserting Data (always use double quotations)

# cur.execute("insert into products(name,buying_price,selling_price)values('milk',80,80)")
# conn.commit() #used to save

# the parameter values is is used since  %s is used as the placeholders
def insert_products(values):
   query="insert into products(name,buying_price,selling_price)values(%s,%s,%s)"
   cur.execute(query,values)
   conn.commit()
#  second method as above 
# def insert_products(values):
#    query=f"insert into products(name,buying_price,selling_price)values{values}""
#    cur.execute(query,values)
#    conn.commit()

#since  data from database is fetched and comes as a list of tuples this means inserting data will be done in terms of tuples
#below are sample values in a tuple to insert
product_values1= ('shoes',1500,2000)
product_values2= ('t-shirt',1500,2000)

insert_products(product_values1)
insert_products(product_values2)



#inserting saLes
def insert_sales(values):
   query= "INSERT INTO sales (pid, quantity, created_at)values(%s,%s,NOW())"
   cur.execute(query,values)
   conn.commit()

sales_values1= (1,2)
sales_values2= (5,20)
insert_sales(sales_values1)
insert_sales(sales_values2)
sales= get_sales()
print(sales)







