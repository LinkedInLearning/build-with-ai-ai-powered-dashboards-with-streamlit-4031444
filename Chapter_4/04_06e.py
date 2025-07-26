#Build with AI: AI-Powered Dashboards with Streamlit 
#Refine and Maintain Your AI-Powered Dashboard

#Import packages
import streamlit as st
import pandas as pd
import os, pickle
from openai import OpenAI
import numpy as np
import altair as alt
import logging
import traceback

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
st.title("Interactive Hotel Dashboard")

#Setup log file for dashboard events, feedback, and errors
logging.basicConfig(
    filename="dashboard_maintenance.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

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
logging.info(f"Filters applied - Numeric: {selected_numeric}, Categorical: {selected_categorical}")

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
    logging.warning("No saved charts found when dashboard ran.")
    #Stop the app execution since there’s nothing to display
    st.stop()

#Display charts in the arrangement specified by saved dashboard layout code
try:
    #Execute the AI-generated dashboard layout code, injecting charts and Streamlit into its local namespace
    exec(dashboard_layout_code, {}, charts | {"st": st})
    #Log a success message if the dashboard layout executes without errors
    logging.info("Dashboard layout successfully executed.")
except Exception as e:
    #Display error message in the Streamlit UI if the layout execution fails
    st.error(f"Error running dashboard layout: {e}")
    #Log the error message to the log file
    logging.error(f"Error executing dashboard layout: {e}")
    #Log the full traceback for debugging purposes
    logging.error(traceback.format_exc())

#Add AI Chabot section in sidebar
st.sidebar.header("AI Assistant")
#Determine if chat history exists in the session state and initialize if it doesn't
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#Create text input field in sidebar to allow users to type in message
user_input = st.sidebar.text_input(
    "Ask a question about this hotel dashboard:",
    key="ui_input"
)

#Check if send button is clicked
if st.sidebar.button("Send", key="ui_send"):
    if not user_input.strip():
        #Provide warning if user has not entered any input
        st.sidebar.warning("Please enter a question before sending.")
    else:
        #Add user's message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        #Build system prompt and add current chat history
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an assistant helping analyze a hotel performance dashboard. "
                    "You have access to filtered dataframe `df`, which contains metrics like "
                    "revenue, profit, city, etc. "
                    "Answer in clear, concise language, and if code would help, provide an Altair snippet."
                )
            }
        ] + st.session_state.chat_history

        try:
            #Send chat history to OpenAI LLM and receive response
            resp = client.chat.completions.create(
                #Select model
                model="gpt-3.5-turbo",
                messages=messages
            )
            #Gather assistant's response
            reply = resp.choices[0].message.content
            #Add AI assistant's reply to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

        except Exception as e:
            #Handle API errors and add to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"Error: {e}"
            })

#Loop through the chat history stored in session state and display each message
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.sidebar.markdown(f"**You:** {msg['content']}")
    else:
        st.sidebar.markdown(f"**Bot:** {msg['content']}")
        
#Add feedback section in the sidebar for user input
st.sidebar.header("📣 Feedback")

#Create thumbs-up feedback button
if st.sidebar.button("👍 Dashboard looks great"):
    #Log positive feedback when user clicks thumbs-up
    logging.info("User feedback: 👍 Dashboard looks great")
    #Display thank you message in sidebar
    st.sidebar.success("Thank you for the positive feedback!")

#Create thumbs-down feedback button
if st.sidebar.button("👎 Needs improvement"):
    #Log negative feedback when user clicks thumbs-down
    logging.info("User feedback: 👎 Needs improvement")
    #Display thank you message for constructive feedback
    st.sidebar.info("Thanks — we’ll review your feedback.")

#Add text input for written feedback
feedback = st.sidebar.text_area("Additional Comments")

#Save written feedback when submitted
if st.sidebar.button("Submit Feedback"):
    #If text area is empty, prompt the user to enter feedback
    if not feedback.strip():
        st.sidebar.warning("Please enter your feedback before submitting.")
    else:
        #Log user’s written feedback to log file
        logging.info(f"User written feedback: {feedback}")
        #Confirm feedback submission to user
        st.sidebar.success("Thank you — your feedback has been logged.")

#Read and display recent log entries for dashboard activity and feedback
with st.expander("Recent Log Entries"):

    #Read last 10 lines of the dashboard maintenance log
    if os.path.exists("dashboard_maintenance.log"):
        #Open the log file and read its contents
        with open("dashboard_maintenance.log") as f:
            #Read only the last 10 lines for recent activity
            lines = f.readlines()[-10:]
        #Display last 10 log lines in a Streamlit code block
        st.code("".join(lines))
    else:
        #If log file doesn't exist yet, notify user
        st.write("No log entries found yet.")