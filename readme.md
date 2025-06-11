FLASK

LIBRARy && framework
-once you install packages/modules/dependencies
- then you import it
Go to mysql shell,
•	Create database duka;
•	Connect to mduka- \c myduka
•	Create the tables
•	CREATE TABLE products ( id SERIAL PRIMARY KEY, name VARCHAR(100), buying_price NUMERIC(20, 2), selling_price NUMERIC(20, 2) ); 
•	CREATE TABLE sales ( id SERIAL PRIMARY KEY, pid INTEGER REFERENCES products(id), quantity INTEGER, created_at TIMESTAMP );
•	CREATE TABLE stock ( id SERIAL PRIMARY KEY, pid INTEGER REFERENCES products(id), stock_quantity INTEGER, created_at TIMESTAMP );


in database.py
conn = psycopg2.connect(user="postgres",password="1112",host="localhost",port="5432",database="mduka")

Psycopg2.connect() – is a function used to create a new database connection. It takes some arguments/parameters.
The conn -> establishes the connection
1.	User= “postgres” -> default PostgreSQL user
2.	Password=”ur psql password”
3.	Host = “localhost” -> where is my postgresql database located. Localhost means your device
4.	Port = “5432”-> where psgrsql service is running
5.	Database =”mduka” -> database to connect to

cur = conn.cursor()

Cur -> object used to execute
N/B 
1.	USE 	 cursor to fetch data from our database
-	Take note DATA FORMAT- list of tuples
 TASK 
1 insert 2 sales using psql and view the sales using psycopg2. (use functions)

CRUD -> Create, Read , Update ,Delete

Create
Inserting Data
1.	Insert Products with psycopg2
Insert into table_name(columns)values(actual_values);
  -execute query with cursor
   -commit your data to the database
cur.execute("insert into products(name,buying_price,selling_price)values('milk',80,80)")
conn.commit() #used to save

the code above is not dynamic but hard coded.
TASK 
Insert 2 products & 2 sales using pscopg2
