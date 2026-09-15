import streamlit as st
import pandas as pd
from dbhelper import DB
import plotly.express as px
import plotly.graph_objects as go



# ------------------------ SIDEBAR ------------------------------
st.set_page_config(layout="wide")
st.sidebar.title("SQL Flight App")
option = st.sidebar.selectbox("Select an OPTION", ["Check Flights", "Analyze Flights"], index=None, placeholder="Options")


# ------------------------ DB CONNECTION ------------------------------
db = DB()


# ------------------------ MAIN PAGE ------------------------------
if option == "Check Flights":
    st.html("<h1 align='center'>Find Flights</h1>")


    # ------------------------ FINDING LOCATIONS ------------------------------
    regions = []
    for i in db.flights_regions():
        regions.append(i[0])
    # -------------------------------------------------------------------------


    col1, col2 = st.columns(2)
    with col1: 
        source = st.selectbox("Source", regions, index=None, placeholder="Select Source")

    with col2:

        # ------------------------ FINDING DESTINATIONS ------------------------------
        if source:
            destinations = []
            for i in db.flights_destination(source):
                destinations.append(i[0])
            # ----------------------------------------------------------------------------
            if destinations:
                destination = st.selectbox("Destination", destinations, index=None, placeholder="Select Destination")
            else:
                st.selectbox("Destination", [""], index=None, placeholder="There are no flights from this source", disabled=True)

    col1, col2, col3 = st.columns(3)
    if source and destination:
        with col2:
            search = st.button("Search", use_container_width=True, type="primary")

        if search:
            flights = db.flights_result(source, destination)
            df = pd.DataFrame(flights, columns= ["Airline", "Source", "Destination", "Route", "Dep_Time", "Duration", "Price"])
            st.dataframe(df.head(10))
            # st.table(df)

elif option == "Analyze Flights":
    st.html("<h1 align='center'>Analyze Flights</h1>")
    

    col1, col2 = st.columns(2)
    with col1:
        airlines = db.airline_analysis()
        fig = go.Figure(data=[go.Pie(labels=airlines["Airline"], values=airlines["Flight Count"])])
        fig.update_layout(title="Airline Analysis Pie Chart", title_x=0.1)
        st.plotly_chart(fig)
    with col2:
        airports = db.flight_bar()
        fig = px.bar(airports, x="Source", y="Flight Count", 
                     title="Busiest Airports Bar Chart", color="Source")
        fig.update_layout(title="Busiest Airports Bar Chart", title_x=0.4)
        st.plotly_chart(fig)

    st.html("<h2 align='center'>Airline Flight Count Over Time</h2>")
    airline = st.selectbox("Select an Airline", airlines["Airline"].tolist())
    if airline:
        airline_data = db.airlines_line(airline)
        fig = px.line(airline_data, x="Date_of_Journey", y="Flight Count", title=f"Flight Count for {airline}")
        st.plotly_chart(fig)

    st.html("<h2 align='center'>Flight Between Source and Destination</h2>")
    flight_data = db.flight_between()
    st.dataframe(flight_data)

else:
    st.html("<h1 style='text-align: center;'>Welcome to the SQL Flight App</h1>")

