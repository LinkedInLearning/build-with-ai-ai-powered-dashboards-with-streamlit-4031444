#Build with AI: AI-Powered Dashboards with Streamlit 
#Define Dashboard Filters with AI Assistance

#Import packages
import streamlit as st
import pandas as pd
import os, pickle
from openai import OpenAI


#Open file with API key
with open("openai_key.txt") as f:
    my_api_key = f.read().strip()

#Initialize OpenAI client with your API key
client = OpenAI(api_key=my_api_key)

#Write title
st.title("")

#Check if cleaned dataset exists, stop app if not found


#Load cleaned dataset from pickle file
with open("cleaned_data_final.pkl", "rb") as f:
    df = pickle.load(f)

#Add subheader for cleaned data preview
st.subheader("Cleaned Data Preview")
#Display first few rows of cleaned data
st.dataframe(df.head())

#Build a summary of each column’s data type, values, and stats

#Loop through each column in the dataframe

    #Check if column is numeric and capture min and max values

    #Check if column is date type and capture date range

    #Otherwise treat as categorical or text and capture sample values

    #Add column summary to list


#Convert list of column summaries into markdown-formatted string


#Create text input area for user to enter a filter suggestion request or targeted question
user_prompt = st.text_area(
    "",
    height=
)

#Check if 'Generate Filter Suggestions' button is clicked
if st.button(""):
    #Provide warning if user has not entered a request
    if not user_prompt.strip():
        st.warning("")
    else:
        #Display spinner while querying AI
        with st.spinner(""):
            try:
                #Construct system prompt to explain available columns and instructions for AI


                #Send prompt and system instructions to OpenAI LLM and receive response
                resp = client.chat.completions.create(
                    #Select model
                    model="gpt-3.5-turbo",
                    messages=[
                        #Provide system instructions
                        {"role": "system", "content": },
                        #Send user's request
                        {"role": "user", "content": user_prompt}
                    ]
                )

                #Extract assistant's reply

                #Display assistant's suggestions as markdown


            #Handle API errors and display message if request fails
            except Exception as e:
                st.error(f" {e}")

