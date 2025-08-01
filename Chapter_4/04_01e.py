#Build with AI: AI-Powered Dashboards with Streamlit 
#Generate Data Visualizations Using AI Prompts

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
st.title("Generated Visualizations with AI")

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

#Create text input for user to name their chart
chart_name = st.text_input("Enter a name for this chart", value="chart1")

#Create text input area for user to describe desired chart
user_prompt = st.text_area(
    "Describe the chart you’d like (e.g. 'bar chart of Revenue by City')",
    height=80,
)

#Check if 'Generate & Save Chart' button is clicked
if st.button("Generate & Save Chart"):
    #Provide warning if user has not entered a description
    if not user_prompt.strip():
        st.warning("Please enter a description.")
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
                        {
                            "role": "system",
                            "content": (
                                "You are an Altair expert. Given a DataFrame `df`, "
                                "return only a Python code block that builds an Altair chart "
                                "and assigns it to a variable named `chart`. "
                                "Do not include extra imports or `st.` calls, just the Altair code."
                            ),
                        },
                        #Send user's chart description
                        {"role": "user", "content": user_prompt},
                    ],
                )

                #Extract AI's reply text and remove markdown/code block formatting
                raw = resp.choices[0].message.content
                code_lines = [
                    line
                    for line in raw.splitlines()
                    if not line.strip().startswith(("```", "python"))
                ]
                ai_code = "\n".join(code_lines)

            except Exception as e:
                st.error(f"Failed to generate chart code: {e}")

        #Add subheader for AI-generated code preview
        st.subheader("AI‑Generated Code")
        #Display AI's generated Altair code
        st.code(ai_code, language="python")

        #Attempt to safely execute the AI-generated Altair code
        local_vars = {"df": df, "alt": alt}
        try:
            exec(ai_code, {}, local_vars)
            #Check if chart variable was successfully created
            if "chart" not in local_vars:
                raise ValueError("The generated code did not produce a `chart` variable.")
            chart = local_vars["chart"]

            #Add subheader and display the newly generated chart
            st.subheader("Preview of Generated Chart")
            st.altair_chart(chart, use_container_width=True)

            #Save AI-generated code to a .py file in the charts directory
            out_path = os.path.join(CHART_DIR, f"{chart_name}.py")
            try:
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(ai_code)
                st.success(f"Saved chart code to `{out_path}`")
            except Exception as e:
                st.error(f"Failed to save chart code: {e}")

        #Handle errors if code execution or chart display fails
        except Exception as e:
            st.error(f"Failed to build or display chart: {e}")

#Add subheader for existing saved charts
st.subheader("Existing Saved Charts")

#Loop through previously saved chart files in the charts directory
for fname in sorted(os.listdir(CHART_DIR)):
    #Skip any non-Python files
    if not fname.lower().endswith(".py"):
        continue

    #Display filename as a bullet point
    st.write(f"- **{fname}**")

    try:
        #Open and read chart code from file
        with open(os.path.join(CHART_DIR, fname), encoding="utf-8") as f:
            saved_code = f.read()

        #Execute saved Altair code safely and display the chart
        local_vars = {"df": df, "alt": alt}
        exec(saved_code, {}, local_vars)
        old_chart = local_vars["chart"]
        st.altair_chart(old_chart, use_container_width=True)

    #Handle errors if chart loading or execution fails
    except Exception as e:
        st.error(f"Failed to load chart {fname}: {e}")
