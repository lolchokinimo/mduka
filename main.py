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
from flask import Flask, render_template


app=Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/products') 
def products():
    return render_template("products.html")

@app.route('/dashboard') 
def dashboard():
    return render_template("dashboard.html")


app.run(debug=True)



