import os
from dotenv import load_dotenv
import mysql.connector

# ------------------------ CREDENTIALS ------------------------------
load_dotenv()
host = os.getenv("host")
port = os.getenv("port")
user = os.getenv("user")
password = os.getenv("password")
database = os.getenv("database")



# ------------------------ CONNECTION ------------------------------
try:
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    mycursor = conn.cursor()
    print("Connection Established")
except mysql.connector.Error as e:
    print(f"Error: {e}")


#------------------------ DATABASE CREATION ------------------------------
try:
    mycursor.execute("CREATE DATABASE indigo")
    print("Database created successfully")
except:
    print("Database already exists")


"""
------------------------ TABLE CREATION ------------------------------
|airport_id| airport_name | city | code |
"""
try:
    mycursor.execute(
        """
        CREATE TABLE airports(
            airport_id INT PRIMARY KEY,
            airport_name VARCHAR(255) NOT NULL,
            city VARCHAR(255) NOT NULL,
            code VARCHAR(10) NOT NULL
        )
        """
    )
    print("Table created successfully")

except:
    print("Table already exists")

#------------------------ INSERTION ------------------------------
try:
    mycursor.execute("SELECT COUNT(*) FROM airports")
    count = mycursor.fetchone()[0]

    if count == 0:
        mycursor.execute(
            """
                INSERT INTO airports VALUES
                (1, 'Indira Gandhi International Airport', 'Delhi', 'DEL'),
                (2, 'Chhatrapati Shivaji Maharaj International Airport', 'Mumbai', 'BOM'),
                (3, 'Kempegowda International Airport', 'Bengaluru', 'BLR'),
                (4, 'Rajiv Gandhi International Airport', 'Hyderabad', 'HYD'),
                (5, 'Chennai International Airport', 'Chennai', 'MAA'),
                (6, 'Netaji Subhas Chandra Bose International Airport', 'Kolkata', 'CCU'),
                (7, 'Cochin International Airport', 'Kochi', 'COK'),
                (8, 'Sardar Vallabhbhai Patel International Airport', 'Ahmedabad', 'AMD'),
                (9, 'Dabolim Airport', 'Goa', 'GOI'),
                (10, 'Pune Airport', 'Pune', 'PNQ')
            """
        )
        conn.commit()
        print(f"{mycursor.rowcount} row(s) inserted")
    else:
        print("Data already exists, skipping insert")
except mysql.connector.Error as e:
    print(f"Error: {e}")


#------------------------ FETCHING DATA ------------------------------
try:
    mycursor.execute("SELECT * FROM airports WHERE airport_id >= 1")
    result = mycursor.fetchall()
    print(result)

except mysql.connector.Error as e:
    print(f"Error: {e}")

# ------------------------ UPDATE DATA ------------------------------
try:
    mycursor.execute("UPDATE airports SET city = 'New Delhi' WHERE airport_id = 1")
    conn.commit()
    mycursor.execute("SELECT * FROM airports")
    result = mycursor.fetchall()
    print(result)
except mysql.connector.Error as e:
    print(f"Error: {e}")

#------------------------ DELETE DATA ------------------------------
try:
    mycursor.execute("DELETE FROM airports WHERE airport_id = 10")
    conn.commit()
    mycursor.execute("SELECT * FROM airports")
    result = mycursor.fetchall()
    print(result)
except mysql.connector.Error as e:
    print(f"Error: {e}")

