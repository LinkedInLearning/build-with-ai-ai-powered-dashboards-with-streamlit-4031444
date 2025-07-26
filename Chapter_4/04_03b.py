#Build with AI: AI-Powered Dashboards with Streamlit 
#Organize Your Dashboard Layout with AI Help

#Import packages
import streamlit as st
import pandas as pd
import os, pickle
from openai import OpenAI
import numpy as np
import altair as alt

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
st.title("Organize Visualizations with AI")

#Create directory to store chart files if it doesn't already exist
CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)

#Check if cleaned dataset exists, stop app if not found
if not os.path.exists("cleaned_data_final.pkl"):
    st.error("No cleaned dataset found. Please complete previous lessons first.")
    st.stop()

#Load cleaned dataset from pickle file
with open("cleaned_data_final.pkl", "rb") as f:
    df = pickle.load(f)

#Add subheader for cleaned data preview
st.subheader("Cleaned Data Preview")
#Display first few rows of cleaned data
st.dataframe(df.head())

#Initialize dictionary for charts


#Loop through each file in the chart directory, sorted alphabetically

    #Check if the file is a Python file by confirming it ends with ".py"

        #Open the chart Python file and read its code as a string
        with open(os.path.join(CHART_DIR, fname), encoding="utf-8") as f:
            code = f.read()
        
        #Create a local namespace with required objects for chart code execution
        local_vars = {"df": df, "alt": alt}
        
        #Try to safely execute the chart code

            #Execute the code in an isolated local_vars context
            exec(code, {}, local_vars)  
            
            #If a variable named 'chart' was created during code execution, store it in the charts dictionary

                #Use the file name (without extension) as the chart's dictionary key

                #Add the chart object to the charts dictionary

        
        #If any error occurs while loading a chart file, display and log an error message
        except Exception as e:
            st.error(f"{e}")


#Provide warning if no charts found in directory

    #Display list of available chart names


#Create text area for user to describe desired dashboard layout using chart names
user_prompt = st.text_area(
    "", 
    height=80
)

#Check if 'Generate Dashboard Layout' button is clicked
if st.button(""):
    #Provide warning if user has not entered a layout instruction
    if not user_prompt.strip():
        st.warning("")
    else:
        #Display spinner while querying AI
        with st.spinner(""):
            try:
                #Prepare AI system instructions with list of available chart names
                chart_names = ", ".join(charts.keys())
                system_message = (
                    f""
                )

                #Send prompt and system instructions to OpenAI LLM and receive response
                resp = client.chat.completions.create(
                    #select model
                    model="gpt-3.5-turbo",
                    #Define assistant's role and instructions
                    messages=[
                        {"role": "system", "content": },
                        #Send user's query
                        {"role": "user", "content": user_prompt}
                    ]
                )

                #Extract AI's reply text and remove markdown and code block formatting
                raw = resp.choices[0].message.content
                code_lines = [
                    line for line in raw.splitlines()
                    if not line.strip().startswith(("```", "python"))
                ]


                st.subheader("AI‑Generated Code")
                #Display AI-generated Streamlit layout code
                st.code(, language="python")

                #Execute the AI-generated layout code to arrange charts on dashboard
                exec()

                #Save AI-generated layout code for next lesson use
                with open("", "w", encoding="utf-8") as f:
                    f.write()
                st.success("")

            #Handle errors if code generation or execution fails
            except Exception as e:
                st.error(f" {e}")