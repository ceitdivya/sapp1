import streamlit as st
import time
import pandas as pd
import numpy as np
import warnings
import plotly.express as px
warnings.filterwarnings('ignore')
import datetime as dt
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Adidas United States Dashboard!!!",page_icon=":bar_chart:",layout="wide")
st.logo('adidas-logo.jpg')
st.title(":bar_chart: Adidas United States Dashboard!!!")

df=pd.read_excel('Adidas.xlsx',sheet_name='Sales')
df['Year']=df['InvoiceDate'].dt.year
df['Month']=df['InvoiceDate'].dt.month

st.sidebar.header("Choose your filter: ")
# Create for Years
years = st.sidebar.multiselect("Years", df["Year"].unique())
# Create for Regions
region = st.sidebar.multiselect("Regions", df["Region"].unique())
# Create for Sales method
sales = st.sidebar.multiselect("Sales Method", df["SalesMethod"].unique())

if not region and not years and not sales:
    filtered_df = df
    st.dataframe(filtered_df.head())
elif not years and not sales:
    filtered_df = df[df["Region"].isin(region)]
    st.dataframe(filtered_df.head())
elif not region and not sales:
    filtered_df = df[df["Year"].isin(years)]
    st.dataframe(filtered_df.head())
elif region and years:
    filtered_df = df[df["Region"].isin(region) & df["Year"].isin(years)]
    st.dataframe(filtered_df.head())
elif region and sales:
    filtered_df = df[df["Region"].isin(region) & df["Sales"].isin(sales)]
    st.dataframe(filtered_df.head())
elif years and sales:
    filtered_df = df[df["Year"].isin(years) & df["Sales"].isin(sales)]
    st.dataframe(filtered_df.head())
elif years:
    filtered_df = df[df["Year"].isin(years)]
    st.dataframe(filtered_df.head())
else:
    filtered_df = df[df["Year"].isin(years) & df["Region"].isin(region) & df["Sales"].isin(sales)]
    st.dataframe(filtered_df.head())

col1,col2,col3=st.columns(3)
col1.header(":blue[Total Sales]")
col1.subheader(filtered_df['TotalSales'].sum())

col2.header(":blue[Total Units sold]")
col2.subheader(filtered_df['UnitsSold'].sum())

col3.header(":blue[Total Profit]")
col3.subheader(round(filtered_df['OperatingProfit'].sum(),2))

st.header(":blue[Total Sales Trend]")
linechart1 = pd.DataFrame(filtered_df.groupby(filtered_df["Month"])["TotalSales"].sum()).reset_index()
fig1 = px.line(linechart1, x = "Month", y="TotalSales",height=500, width = 1000,template="gridon")
st.plotly_chart(fig1,use_container_width=True)

st.header(":blue[Total Profit Trend]")
linechart2 = pd.DataFrame(filtered_df.groupby(filtered_df["Month"])["OperatingProfit"].sum()).reset_index()
fig2 = px.line(linechart2, x = "Month", y="OperatingProfit",height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

cl1,cl2=st.columns(2)

cl1.header(":blue[Sales By Product]")
chart3 = pd.DataFrame(filtered_df.groupby(filtered_df["Product"])["TotalSales"].sum()).reset_index()
chart3.sort_values(by=['TotalSales'],ascending=True,inplace=True)
fig3=px.funnel(chart3,y='Product',x='TotalSales',color='Product')
cl1.plotly_chart(fig3,use_container_width=True)

cl2.header(":blue[Sales By Retailer]")
chart4 = pd.DataFrame(filtered_df.groupby(filtered_df["Retailer"])["TotalSales"].sum()).reset_index()
fig4=px.pie(chart4, values = "TotalSales", names = "Retailer", hole = 0.1)
cl2.plotly_chart(fig4,use_container_width=True)
 
st.header(":blue[Top 10 Sales By State]")

chart5 = pd.DataFrame(filtered_df.groupby(filtered_df["State"])["TotalSales"].sum()).reset_index()

chart5.sort_values(by=['TotalSales'],ascending=True,inplace=True)

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to get latitude and longitude
def get_lat_long(state):
    try:
        location = geolocator.geocode(state)
        return location.latitude, location.longitude
    except:
        return None, None

# Apply function to DataFrame
chart5['latitude'], chart5['longitude'] = zip(*chart5['State'].apply(get_lat_long))
#st.dataframe(chart5)
chart5.dropna(inplace=True,axis=0)
#st.dataframe(chart5)
#fig5 = px.scatter_mapbox(chart5, lat="latitude", lon="longitude",color="TotalSales", 
                  #color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
st.map(chart5,
    latitude='latitude',
    longitude='longitude',
    
    )
#st.plotly_chart(fig5,use_container_width=True)
