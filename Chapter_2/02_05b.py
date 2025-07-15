#Build with AI: AI-Powered Dashboards with Streamlit 
#Handle Errors and Provide User Feedback in Your App

#Import packages
import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
import altair as alt
from openai import OpenAI

import runpy
import tempfile

#Open file with API key
with open("openai_key.txt") as f:
    my_api_key = f.read().strip()

#Initialize OpenAI client with your API key
client = OpenAI(api_key=my_api_key)

#Configure page
st.set_page_config(page_title='Iris Dashboard', layout='wide')

#Write title and description
st.title('')

#Load Iris dataset
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

#Add sidebar filters
st.sidebar.header('Filter Options')
#Add species filter
species_options = st.sidebar.multiselect('Select species:', options=iris.target_names, default=list(iris.target_names))
#Allow users to change x-axis
x_axis = st.sidebar.selectbox('X-axis feature:', options=iris.feature_names, index=0)
#Allow users to change y-axis
y_axis = st.sidebar.selectbox('Y-axis feature:', options=iris.feature_names, index=1)

#Add chat widget on main page
st.subheader("Chat Widget")
#Determine if chat history exists in the session state and initialize if it doesn't
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

#Create code input area on main page for user to paste Python code


#Define function to execute the user-submitted code

    #Remove any extra whitespace from the code

    #Provide warning if user has not entered any code


    #Display a spinner while code is running

            #Create a temporary file to write the Python code into

                #Run the temporary Python file and capture the results as a dictionary

            #Check if expected variable is present

                #Display message if variable is missing

                #Add assistant's reply to chat history


                #Display success message if code runs and variable is present

                #Display the result when the code is run

                #Add assistant's reply to chat history


        #Handle syntax errors and add to chat history

        #Handle other errors and add to chat history


#Create button on main page to run code when clicked


#Add chat window to display messages

#Loop through the chat history stored in session state and display each message

    #Check if message is from assistant and display as info box

    #Otherwise display message as regular text


#Filter DataFrame
filtered_df = df[df['species'].isin(species_options)]

#Display filtered data
st.subheader('Filtered Data')
st.dataframe(filtered_df)

#Create scatter plot visualization
st.subheader('Scatter Plot')
scatter = (
    alt.Chart(filtered_df)
    .mark_circle(size=60)
    .encode(
        x=x_axis,
        y=y_axis,
        color='species',
        tooltip=iris.feature_names + ['species']
    )
    .interactive()
)
st.altair_chart(scatter, use_container_width=True)

#Display summary statistics
st.subheader('Summary Statistics')
st.write(filtered_df.describe())

#Add dashboard footer
st.write('---')
st.write('Dashboard built with Streamlit and Altair')