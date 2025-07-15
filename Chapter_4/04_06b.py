#Build with AI: AI-Powered Dashboards with Streamlit 
#Refine and Maintain Your AI-Powered Dashboard

#Import packages
import streamlit as st
import pandas as pd
import os, pickle
from openai import OpenAI
import numpy as np
import altair as alt


#Enable Altair VegaFusion data transformer for efficient chart rendering
alt.data_transformers.enable("vegafusion")

#Configure page
st.set_page_config(page_title="Hotel Dashboard", layout="wide")

#Write title
st.title("")

#Setup log file for dashboard events, feedback, and errors


#Check for cleaned dataset, stop if missing
if not os.path.exists("cleaned_data_final.pkl"):
    st.error("No cleaned dataset found. Please complete previous lessons first.")
    st.stop()

#Load cleaned dataset from pickle file
with open("cleaned_data_final.pkl", "rb") as f:
    df_full = pickle.load(f)

#Copy full dataset for filtering
df = df_full.copy()

#Create sidebar for dynamic filters
st.sidebar.header("Choose Filters to Display")

#Identify numeric and categorical columns
numeric_cols = df_full.select_dtypes(include="number").columns.tolist()
cat_cols = df_full.select_dtypes(exclude="number").columns.tolist()

#User multiselects to choose which numeric and categorical columns to show as filters
selected_numeric = st.sidebar.multiselect("Numeric Filters", options=numeric_cols, default=[])
selected_categorical = st.sidebar.multiselect("Categorical Filters", options=cat_cols, default=[])

#Create sliders for selected numeric columns
for col in selected_numeric:
    #Determine minimum and maximum values for the current numeric column
    min_val, max_val = float(df_full[col].min()), float(df_full[col].max())
    #Add a slider to the sidebar for selecting a numeric value range
    sel_range = st.sidebar.slider(
        #Label for the slider
        f"{col} Range",    
        #Minimum possible value          
        min_value=min_val,   
        #Maximum possible value        
        max_value=max_val,   
        #Default slider range (full span)        
        value=(min_val, max_val),  
        #Unique key for this filter to track state  
        key=f"filter_{col}"          
    )
    #Filter the dataset based on the selected slider range values
    df = df[(df[col] >= sel_range[0]) & (df[col] <= sel_range[1])]

#Create multiselects for selected categorical columns
for col in selected_categorical:
    #Retrieve sorted list of unique non-null options for the current categorical column
    options = sorted(df_full[col].dropna().unique().tolist())
    #Add a multiselect widget to the sidebar for selecting categories
    sel_opts = st.sidebar.multiselect(
        #Label for the multiselect
        f"{col} Options", 
        #Available selection options     
        options=options, 
        #Default selection (select all by default)      
        default=options,       
        #Unique key for this filter to track state
        key=f"filter_{col}"    
    )
    #Filter the dataset based on the selected categories
    df = df[df[col].isin(sel_opts)]

#Log applied filters


#Check for existing saved dashboard layout
if not os.path.exists("dashboard_layout.py"):
    st.error("No dashboard layout found from previous lesson. Please complete the previous lesson first.")
    st.stop()

#Read in AI-generated layout code from file
with open("dashboard_layout.py", "r", encoding="utf-8") as f:
    dashboard_layout_code = f.read()

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
    #Log this warning event to the log file

    #Stop the app execution since there’s nothing to display
    st.stop()

#Display charts in the arrangement specified by saved dashboard layout code
try:
    #Execute the AI-generated dashboard layout code, injecting charts and Streamlit into its local namespace
    exec(dashboard_layout_code, {}, charts | {"st": st})
    #Log a success message if the dashboard layout executes without errors

except Exception as e:
    #Display error message in the Streamlit UI if the layout execution fails
    st.error(f"Error running dashboard layout: {e}")
    #Log the error message to the log file

    #Log the full traceback for debugging purposes


#Add feedback section in the sidebar for user input


#Create thumbs-up feedback button

    #Log positive feedback when user clicks thumbs-up

    #Display thank you message in sidebar


#Create thumbs-down feedback button

    #Log negative feedback when user clicks thumbs-down

    #Display thank you message for constructive feedback


#Add text input for written feedback


#Save written feedback when submitted

    #If text area is empty, prompt the user to enter feedback

        #Log user’s written feedback to log file

        #Confirm feedback submission to user


#Read and display recent log entries for dashboard activity and feedback


#Read last 10 lines of the dashboard maintenance log

    #Open the log file and read its contents

        #Read only the last 10 lines for recent activity

    #Display last 10 log lines in a Streamlit code block

    #If log file doesn't exist yet, notify user
