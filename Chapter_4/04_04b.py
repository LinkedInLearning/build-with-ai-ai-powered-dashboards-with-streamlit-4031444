#Build with AI: AI-Powered Dashboards with Streamlit 
#Build Interactive Dashboards That Respond to Filters

#Import packages
import streamlit as st
import pandas as pd
import os, pickle
import altair as alt
from openai import OpenAI

#Enable Altair VegaFusion data transformer for efficient chart rendering
alt.data_transformers.enable("vegafusion")

#Open file with API key
with open("openai_key.txt") as f:
    my_api_key = f.read().strip()

#Initialize OpenAI client with your API key
client = OpenAI(api_key=my_api_key)

#Configure page
st.set_page_config(page_title="Hotel Dashboard", layout="wide")

#Write title
st.title("")

#Check for cleaned dataset, stop if missing
if not os.path.exists("cleaned_data_final.pkl"):
    st.error("No cleaned dataset found. Please complete previous lessons first.")
    st.stop()

#Load cleaned dataset from pickle file
with open("cleaned_data_final.pkl", "rb") as f:
    df_full = pickle.load(f)

#Copy full dataset for filtering


#Create sidebar for dynamic filters


#Identify numeric and categorical columns


#User multiselects to choose which numeric and categorical columns to show as filters


#Create sliders for selected numeric columns

    #Determine minimum and maximum values for the current numeric column

    #Add a slider to the sidebar for selecting a numeric value range

        #Label for the slider
 
        #Minimum possible value          

        #Maximum possible value        
  
        #Default slider range (full span)        
 
        #Unique key for this filter to track state  

    #Filter the dataset based on the selected slider range values


#Create multiselects for selected categorical columns

    #Retrieve sorted list of unique non-null options for the current categorical column

    #Add a multiselect widget to the sidebar for selecting categories

        #Label for the multiselect

        #Available selection options     

        #Default selection (select all by default)      
   
        #Unique key for this filter to track state 

    #Filter the dataset based on the selected categories


#Check for existing saved dashboard layout
if not os.path.exists(""):
    st.error("Please complete the previous lesson first.")
    st.stop()

#Read in AI-generated layout code from file
with open("dashboard_layout.py", "", encoding="utf-8") as f:


#Load charts using the current filtered dataset
CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)

#Initialize dictionary for charts
charts = {}

#Loop through each file in the chart directory, sorted alphabetically
for fname in sorted(os.listdir(CHART_DIR)):
    #Check if the file is a Python file by confirming it ends with ".py"
    if fname.lower().endswith(".py"):
        #Open the chart Python file and read its code as a string
        with open(os.path.join(CHART_DIR, fname), encoding="utf-8") as f:
            code = f.read()
        
        #Create a local namespace with required objects for chart code execution
        local_vars = {"df": df, "alt": alt}
        
        #Try to safely execute the chart code
        try:
            #Execute the code in an isolated local_vars context
            exec(code, {}, local_vars)  
            
            #If a variable named 'chart' was created during code execution, store it in the charts dictionary
            if "chart" in local_vars:
                #Use the file name (without extension) as the chart's dictionary key
                chart_key = os.path.splitext(fname)[0]
                #Add the chart object to the charts dictionary
                charts[chart_key] = local_vars["chart"]
        
        #If any error occurs while loading a chart file, display and log an error message
        except Exception as e:
            st.error(f"Failed to load {fname}: {e}")

#Warn if no charts found
if not charts:
    #Display Streamlit warning message if no charts are loaded into the dashboard
    st.warning("No saved charts found. Please generate charts first.")
    #Stop the app execution since there’s nothing to display
    st.stop()

#Display charts in the arrangement specified by saved dashboard layout code

    #Execute the AI-generated dashboard layout code, injecting charts and Streamlit into its local namespace

    #Display error message in the Streamlit UI if the layout execution fails

#Add AI Chabot section in sidebar

#Determine if chat history exists in the session state and initialize if it doesn't

#Create text input field in sidebar to allow users to type in message


#Check if send button is clicked

        #Provide warning if user has not entered any input

        #Add user's message to chat history


        #Build system prompt and add current chat history



            #Send chat history to OpenAI LLM and receive response

                #Select model

            #Gather assistant's response

            #Add AI assistant's reply to chat history


            #Handle API errors and add to chat history


#Loop through the chat history stored in session state and display each message
