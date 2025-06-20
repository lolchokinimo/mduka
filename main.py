# from flask import Flask

# #creating a flask instance
# app = Flask(__name__)

# @app.route('/') #decorator function responsible for routing. it allows us to see content on page
# def home():
#     return "my flask application"

# @app.route('/name') 
# def name():
#     return "my name is Evans"



# app.run() #you can add app.run(debug=True) for autoupdate


# rendering html pages 
from flask import Flask, render_template, request, redirect,url_for
from database import get_products, insert_products, get_stock, insert_stock, insert_sales, get_sales


app=Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/products') 
def products():
    products= get_products()
    return render_template("products.html",products=products)

@app.route('/dashboard') 
def dashboard():
    return render_template("dashboard.html")

@app.route('/login') 
def login():
    return render_template("login.html")

@app.route('/sales') 
def sales():
    products = get_products()
    sales= get_sales()
    return render_template("sales.html",products=products, sales=sales)
 
#  make a new sale 
@app.route('/add_sale', methods=['GET','POST'])
def add_sale():
    pid= request.form['pid']
    quantity= request.form['quantity']
    new_sale=(pid,quantity)
    insert_sales(new_sale)
    return redirect(url_for('sales'))


# this route will enable us to add stock 
@app.route('/stock')
def stock():
    products = get_products()
    stock=get_stock()
    return render_template("stock.html", products = products, stock=stock)

@app.route('/add_stock', methods=['GET','POST'])
def add_stock():
    pid = request.form['pid']
    stock_quantity = request.form['stock']
    new_stock = (pid,stock_quantity)
    insert_stock(new_stock)
    return redirect(url_for('stock'))



# adding products in new products 
@app.route('/add_products',methods=['GET','POST'])
def add_products():
    product_name = request.form["product"]
    buying_price = request.form["buying"]
    selling_price = request.form["selling"]
    new_product = (product_name,buying_price,selling_price)
    insert_products(new_product)
    # user is redirected 
    return redirect(url_for('products'))



app.run(debug=True)



