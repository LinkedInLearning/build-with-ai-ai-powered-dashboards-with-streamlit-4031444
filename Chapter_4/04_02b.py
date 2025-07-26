#Build with AI: AI-Powered Dashboards with Streamlit 
#Refine Data Visuals Using AI Suggestions

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
st.title("")

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

#Check for existing saved chart files


#Create selectbox for user to choose a saved chart to refine


#Load selected chart code from file


#Attempt to safely execute the selected chart code
local_vars = {"df": df, "alt": alt}
exec(, {}, local_vars)
chart = local_vars["chart"]


#Display the selected chart
st.altair_chart(chart, use_container_width=True)

#Create text input area for user to describe how to refine the selected chart
user_prompt = st.text_area(
    "", 
    height=80
)

#Check if 'Refine & Save' button is clicked
if st.button(""):
    #Provide warning if user has not entered a refinement instruction
    if not user_prompt.strip():
        st.warning("")
    else:
        #Display spinner while querying AI
        with st.spinner("Generating code…"):
            try:
                #Send prompt and system instructions to OpenAI LLM and receive response
                resp = client.chat.completions.create(
                    #Select model
                    model="gpt-3.5-turbo",
                    messages=[
                        #Provide system instructions
                        {"role": "system", "content": (
                            "You are an Altair expert."

                        )},
                        #Send user's refinement instruction
                        {"role": "user", "content": user_prompt}
                    ]
                )

                #Extract AI's reply text and remove markdown and code block formatting
                raw = resp.choices[0].message.content
                code_lines = "\n".join(
                    line for line in raw.splitlines() 
                    if not line.strip().startswith(("```", "python"))
                )

                #Fix known Altair code issues if present
                ai_code = 

            #Handle errors if code generation request fails
            except Exception as e:
                st.error(f" {e}")

        st.subheader("AI‑Generated Code")
        #Display AI-generated refinement code
        st.code(ai_code, language="python")

        #Combine original chart code and AI-generated refinement code
        

        #Attempt to save combined refined code back to original file
        out_path = os.path.join(CHART_DIR, chart_name)
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write()
            st.success(f"")
        except Exception as e:
            st.error(f" {e}")

        #Attempt to safely execute the combined refined chart code
        local_vars = {"df": df, "alt": alt}
        try:
            exec(, {}, local_vars)
            refined_chart = local_vars["chart"]

            st.subheader("")
            #Display the refined chart
            st.altair_chart(, use_container_width=True)

        #Handle errors if chart execution or display fails
        except Exception as e:
            st.error(f" {e}")