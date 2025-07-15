#Build with AI: AI-Powered Dashboards with Streamlit 
#Quick Review: Streamlit Basics for Web Apps

#Import packages
import streamlit as st
from datetime import date, datetime

#Configure page
st.set_page_config(page_title="Streamlit Basics Review",layout="wide")

#Write title and text
st.title("Streamlit Basics Review")
st.write("Hello world!")

#Gather current date and time
st.write("Current date and time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

#Create button
if st.button("Press me!"):
    st.success("Button was pressed!")

#Create slider widget
age = st.slider("Your age", 0, 120, 30)
st.write(f"You are {age} years old.")

#Create text input widget
name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello, {name}!")

#Create checkbox widget
toggle = st.checkbox("Check for a surprise")
if toggle:
    st.info("Surprise!")

#Create radio buttons widget
gender = st.radio("Select Gender", ["Male", "Female", "Other"])
st.write("You selected:", gender)

#Create multiselect widget
options = st.multiselect("Choose pizza toppings", ["Cheese", "Pepperoni", "Onions"])
st.write("Toppings:", options)

#Create date input widget
today = st.date_input("Pick a date:", date.today())
st.write("You picked:", today)

#Create sidebar container
st.sidebar.title("Sidebar Panel")
#Add selection widget for sidebar
sidebar_option = st.sidebar.selectbox("Select an option:", ["Home", "Settings", "About"])
st.sidebar.write("You chose", sidebar_option)

#Create three column containers
col1, col2, col3 = st.columns(3)
#Create temperature container
with col1:
    st.metric("Temperature", "72°F", "-1.2°F")
#Create wind speed container
with col2:
    st.metric("Wind Speed", "10 mph", "+1.5 mph")
#Create humidity container
with col3:
    st.metric("Humidity", "50%", "-5%")

#Create expander container
with st.expander("See more details"):
    st.write("Here are more details... you can put any Streamlit commands inside expanders.")