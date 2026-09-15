import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import streamlit as st

class DB:
    def __init__(self):
        # ------------------------ CONNECTION & CREDENTIALS ------------------------------
        load_dotenv()
        self.host = st.secrets["host"]
        self.port = st.secrets["port"]
        self.user = st.secrets["user"]
        self.password = st.secrets["password"]
        self.database = st.secrets["database"]
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.mycursor = self.conn.cursor()
            print("Connection Established")
        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def flights_regions(self):

        # ------------------------ FINDING LOCATIONS ------------------------------
        self.mycursor.execute(
            """
            select distinct(Source) from flights
            union 
            select distinct(Destination) from flights
            """
        )
        self.locations = self.mycursor.fetchall()
        return self.locations

    def flights_destination(self, source):
        self.mycursor.execute(
            '''
            select distinct Destination from flights
            where Source = %s
            ''', (source,)
        )
        return self.mycursor.fetchall()

    def flights_result(self, source, destination):
        self.mycursor.execute(
            '''
            select Airline, Source, Destination, Route, Dep_Time, Duration, Price from flights
            where Source = '{}' and Destination = '{}' order by Price asc limit 20
            '''.format(source, destination)
        )
        return self.mycursor.fetchall()

    def airline_analysis(self):
        self.mycursor.execute(
            """
            select Airline, count(*) from flights
            group by Airline
            """
        )
        self.flights_result = self.mycursor.fetchall()
        df = pd.DataFrame(self.flights_result, columns=["Airline", "Flight Count"])
        return df

    def flight_bar(self):
        self.mycursor.execute(
            """
            select Source,count(*) from
            (select Source from flights
            union all
            select Destination from flights) f
            group by f.Source
            """
        )
        self.flights_result = self.mycursor.fetchall()
        df = pd.DataFrame(self.flights_result, columns=["Source", "Flight Count"])
        return df

    def airlines_line(self, airline):
        self.mycursor.execute(
            """SELECT Date_of_Journey, count(*) FROM flights.flights
                where Airline = '{}'
                group by Date_of_Journey""".format(airline)
        )
        self.flights_result = self.mycursor.fetchall()
        df = pd.DataFrame(self.flights_result, columns=["Date_of_Journey", "Flight Count"])
        return df

    def flight_between(self):
        self.mycursor.execute(
            """
            select Source, Destination, count(*) from flights
            group by Source, Destination
            """
        )
        self.flights_result = self.mycursor.fetchall()
        df = pd.DataFrame(self.flights_result, columns=["Source", "Destination", "Flight Count"])
        return df