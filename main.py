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
from flask import Flask, render_template, request, redirect,url_for,flash, session
from database import get_products, insert_products, get_stock, insert_stock, insert_sales, get_sales, available_stock, sales_per_product, profit_per_product, sales_per_day, profit_per_day, check_user, insert_user
from flask_bcrypt import Bcrypt
from functools import wraps

app=Flask(__name__)

bcrypt= Bcrypt(app)

app.secret_key= 'kjjkhdjdnjkndn76'


@app.route('/')
def home():
    return render_template("index.html")

# page protection 
def login_required(f):
    @wraps(f)
    def protected(*args,**kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return protected

@app.route('/homepage')
def homepage():
    flash("Homepage accessed succesfully",'success')
    return render_template("homepage.html")

@app.route('/products')
@login_required 
def products():
    products= get_products()
    return render_template("products.html",products=products)

@app.route('/dashboard')
@login_required  
def dashboard():
    # sales_per_day & profit_per_day 
    sales_product= sales_per_product()
    profit_product = profit_per_product()
    # sales_per_day & profit_per_day 
    sales_day = sales_per_day()
    profit_day = profit_per_day()

    # product related dash data (unpacking the tuple and placing the values into a list)
    product_name = [i[0] for i in sales_product]
    sale_prod =[float(i[1]) for i in sales_product]
    prof_prod = [float(i[1]) for i in profit_product]

    # date related dash data 
    date = [str(i[0]) for i in sales_day]
    sales_of_day = [float(i[1]) for i in sales_day]
    profit_0f_day =[float(i[1]) for i in profit_day]

    return render_template("dashboard.html",product_name=product_name,sale_prod=sale_prod,prof_prod=prof_prod, date=date,sales_of_day=sales_of_day,profit_0f_day=profit_0f_day  )



@app.route('/sales') 
@login_required 
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
    stock_available=available_stock(pid)
    if stock_available < float(quantity):
        flash("Insufficient stock,cant complete sale",'info')
    else:
        insert_sales(new_sale)
        flash("Sale  succesfully")
    return redirect(url_for('sales'))


# this route will enable us to add stock 
@app.route('/stock')
@login_required 
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
    flash("Product added  succesfully")
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

# log in 
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = check_user(email)
        if not user:
            flash("user not found")
        else:
            if bcrypt.check_password_hash(user[-1],password):
                flash("logged in ","success")
                session['email'] = email
                return redirect(url_for('dashboard'))
            else:
                flash("password incorrect",'danger')
    return render_template("login.html")

# registering users
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['fullname']
        email = request.form['email']
        phone_number = request.form['phone']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = check_user(email)
        if not user:
            new_user = (full_name,email,phone_number,hashed_password)
            insert_user(new_user)
            flash("User registered successfully",'success')
            return redirect(url_for('login'))
        else:
            flash("user already exists,please log in",'danger')
    return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop('email', None)
    flash("logged out",'info')
    return redirect(url_for('login'))

app.run(debug=True)



