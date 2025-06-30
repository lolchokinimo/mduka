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


# sales_data = get_sales()


# print('sales data is', sales_data)

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
# product_values1= ('shoes',1500,2000)
# product_values2= ('t-shirt',1500,2000)

# insert_products(product_values1)
# insert_products(product_values2)



#inserting saLes
def insert_sales(values):
   query= "INSERT INTO sales (pid, quantity, created_at)values(%s,%s,NOW())"
   cur.execute(query,values)
   conn.commit()

# sales_values1= (1,2)
# sales_values2= (5,20)
# insert_sales(sales_values1)
# insert_sales(sales_values2)
# sales= get_sales()
# print(sales)

# inserting stock 
def insert_stock(values):
   query= "insert into stock(pid,stock_quantity,created_at)values(%s,%s,now())"
   cur.execute(query,values)
   conn.commit()

# displaying stock 
def get_stock():
   cur.execute("select* from stock")
   stock =cur.fetchall()
   return stock


# making a sale and updating the stock 
def make_sale_update_stock(values):
    # Unpack values if it's a tuple like (pid, quantity)
    pid, qty = values

    # Insert into sales and return the inserted values
    insert_query = """
        INSERT INTO sales (pid, quantity, created_at)
        VALUES (%s, %s, NOW())
        RETURNING pid, quantity
    """
    cur.execute(insert_query, (pid, qty))
    returned_pid, sold_qty = cur.fetchone()

    # Update stock: subtract sold quantity
    update_query = """
        UPDATE stock
        SET quantity = quantity - %s
        WHERE pid = %s
    """
    cur.execute(update_query, (sold_qty, returned_pid))

    conn.commit()


def sales_per_product():
    cur.execute("""
        select products.name, sum(sales.quantity * products.selling_price) 
                as revenue from products join sales on products.id = sales.pid group by(products.name);
    """)
    profit = cur.fetchall()
    return profit

def profit_per_product():
    cur.execute("""
        select products.name ,sum(sales.quantity * (selling_price - buying_price)) as profit from products join 
        sales on sales.pid = products.id group by products.name;
    """)
    profit_product = cur.fetchall()
    return profit_product

def sales_per_day():
    cur.execute("""
        select date(sales.created_at) as date, sum(sales.quantity * products.selling_price) 
        as sales from sales join products on products.id = sales.pid group by date order by
        date asc;
    """)
    sales_day = cur.fetchall()
    return sales_day

def profit_per_day():
    cur.execute("""
        select date(sales.created_at) as date ,sum(sales.quantity *(selling_price - buying_price))
        as profit from sales join products on products.id = sales.pid group by date order by date
        desc;
    """)
    profit_day = cur.fetchall()
    return profit_day


# 1.	attempt to update stock after making sale 
def available_stock(pid):
    cur.execute("select sum(stock.stock_quantity) from stock where pid = %s",(pid,))
    total_stock = cur.fetchone()[0] or 0

    cur.execute("select sum(sales.quantity) from sales where pid = %s" ,(pid,))
    total_sold = cur.fetchone()[0] or 0
    return total_stock - total_sold


# check_user 
def check_user(email):
    cur.execute("select * from users where users.email = %s",(email,))
    user = cur.fetchone()
    return user

# insert into user 
def insert_user(user_details):
    cur.execute("insert into users(full_name,email,phone_number,password)values(%s,%s,%s,%s)",(user_details))
    conn.commit()


