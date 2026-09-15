import os
import pandas as pd
from dotenv import load_dotenv
import mysql.connector
from sqlalchemy import create_engine

# ------------------------ CREDENTIALS ------------------------------
load_dotenv(override=True)
host = os.getenv("host")
port = os.getenv("port")
user = os.getenv("user")
password = os.getenv("password")
database = os.getenv("database")

# ------------------------ STEP 1: CREATE DATABASE IF NOT EXISTS ------------------------
conn = mysql.connector.connect(host=host, port=port, user=user, password=password)
mycursor = conn.cursor()
mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
conn.commit()
conn.close()
print(f"Database '{database}' ready")

# ------------------------ STEP 2: CONNECT TO THE DATABASE ------------------------
conn = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)
mycursor = conn.cursor()
print("Connected to database:", database)

# ------------------------ STEP 3: CREATE TABLE WITH PRIMARY KEY ------------------------
mycursor.execute("DROP TABLE IF EXISTS flights")
conn.commit()

mycursor.execute("""
    CREATE TABLE flights (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Airline TEXT,
        Date_of_Journey TEXT,
        Source TEXT,
        Destination TEXT,
        Route TEXT,
        Dep_Time TEXT,
        Duration TEXT,
        Total_Stops TEXT,
        Price BIGINT
    )
""")
conn.commit()
print("Table 'flights' created")

# ------------------------ STEP 4: LOAD CSV DATA ------------------------
csv_path = "flights.csv"  
df = pd.read_csv(csv_path)

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

df.to_sql(
    name="flights",
    con=engine,
    if_exists="append",   # table already created with primary key, so only insert
    index=False
)
print(f"{len(df)} rows loaded into 'flights' table")

# ------------------------ STEP 5: VERIFY ------------------------
mycursor.execute("SELECT COUNT(*) FROM flights")
count = mycursor.fetchone()[0]
print(f"Total rows in 'flights' table: {count}")

# ------------------------ CLEANUP ------------------------
mycursor.close()
conn.close()
engine.dispose()