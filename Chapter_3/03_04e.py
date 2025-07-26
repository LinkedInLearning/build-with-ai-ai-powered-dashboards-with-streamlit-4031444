# Build with AI: AI-Powered Dashboards with Streamlit 
# Clean Your Data with Help from AI

#Import packages
import streamlit as st
import pandas as pd
import runpy, tempfile, os, pickle
from openai import OpenAI

#Open file with API key
with open("openai_key.txt") as f:
    my_api_key = f.read().strip()

#Initialize OpenAI client with your API key
client = OpenAI(api_key=my_api_key)

#Write title
st.title("Clean Data with AI")

#Check if cleaned dataset exists and load it if available
if os.path.exists("cleaned_data_final.pkl"):
    with open("cleaned_data_final.pkl", "rb") as f:
        df = pickle.load(f)
    #Display success message when cleaned data is loaded
    st.success("Existing cleaned dataset loaded.")
else:
    #Load revenue and expenses file
    df_rev_exp = pd.read_excel("Landon_Hotel_Revenue_And_Expenses.xlsx")
    #Load location file
    df_loc = pd.read_excel("Landon_Hotel_Location.xlsx")
    #Merge files on 'Hotel ID'
    df = df_rev_exp.merge(df_loc, on="Hotel ID", how="outer")
    #Display success message when raw data is loaded
    st.success("Raw merged dataset loaded.")

#Add subheader for current data preview
st.subheader("Current Working Data Preview")
#Display first few rows of current dataframe
st.dataframe(df.head())

#Determine if chat history exists in the session state and initialize if it doesn't
if "history" not in st.session_state:
    st.session_state.history = []

#Create text input area for users to describe their cleaning instructions
user_prompt = st.text_area(
    "Describe how you'd like to clean the data (e.g. drop nulls in 'Expenses', rename columns, etc.)",
    height=100
)

#Determine if AI-generated cleaning code exists in the session state and initialize if it doesn't
if "latest_code" not in st.session_state:
    st.session_state.latest_code = ""

#Check if 'Generate Cleaning Code' button is clicked
if st.button("Generate Cleaning Code"):
    #Provide warning if user has not entered a cleaning instruction
    if not user_prompt.strip():
        st.warning("Please describe a cleaning action before sending.")
    else:
        #Add user's message to chat history
        st.session_state.history.append(("You", user_prompt))
        #Display spinner while querying AI
        with st.spinner("Generating cleaning code…"):
            try:
                #Send prompt and instructions to OpenAI LLM and receive response
                resp = client.chat.completions.create(
                    #Select model
                    model="gpt-3.5-turbo",
                    messages=[
                        #Define assistant's role and instructions
                        {"role": "system", "content": (
                            "You are a Python data engineer. "
                            "Given df (a pandas DataFrame), output only a Python code block "
                            "that transforms df according to the user's request and reassigns to df."
                        )},
                        #Send user's prompt
                        {"role": "user", "content": user_prompt}
                    ]
                )

                #Define function to clean AI's code response by removing markdown markers
                def clean_ai_code(raw_code):
                    code = raw_code.strip()
                    #Remove ``` markdown markers if present
                    if code.startswith("```"):
                        parts = code.split("```")
                        code = "".join(parts[1:])
                    #Remove any standalone 'python' lines
                    code_lines = code.splitlines()
                    code_lines = [line for line in code_lines if line.strip().lower() != "python"]
                    clean_code = "\n".join(code_lines).strip()
                    return clean_code

                #Gather assistant's raw reply
                raw_code = resp.choices[0].message.content
                #Clean AI response to extract Python code only
                clean_answer = clean_ai_code(raw_code)

                #Add subheader for AI-generated cleaning code
                st.subheader("AI‑Generated Cleaning Code")
                #Display extracted AI-generated code with syntax highlighting
                st.code(clean_answer, language="python")

                #Save AI-generated code in session state for possible application later
                st.session_state.latest_code = clean_answer

                #Add assistant's reply to chat history
                st.session_state.history.append(("Bot", "Cleaning code generated successfully. Use the button below to apply and save it if you wish."))

            #Handle API and code extraction errors and add to chat history
            except Exception as e:
                st.error(f"AI error: {e}")
                st.session_state.history.append(("Bot", f"Error: {e}"))

#Check if AI-generated cleaning code is available and if 'Apply & Save Cleaning Change' button is clicked
if st.session_state.latest_code:
    if st.button("Apply & Save Cleaning Change"):
        try:
            #Save current dataframe to a pickle file for use by temp script
            with open("cleaned_data_final.pkl", "wb") as f:
                pickle.dump(df, f)

            #Also save cleaned dataset to the Chapter_4 folder one level up
            chapter_4_path = os.path.join(os.path.dirname(os.getcwd()), "Chapter_4", "cleaned_data_final.pkl")
            #Ensure Chapter_4 exists
            os.makedirs(os.path.dirname(chapter_4_path), exist_ok=True)  
            #Save current dataframe to a pickle file for use by temp script
            with open(chapter_4_path, "wb") as f:
                pickle.dump(df, f)

            #Create temporary Python script containing AI-generated cleaning code
            temp_code = f"""
import pickle
import os

#Load existing dataframe
with open("cleaned_data_final.pkl", "rb") as f:
    df = pickle.load(f)

#AI-generated cleaning code
{st.session_state.latest_code}

#Save updated dataframe back to current folder
with open("cleaned_data_final.pkl", "wb") as f:
    pickle.dump(df, f)

#Save updated dataframe to Chapter_4 folder one level up
chapter_4_path = os.path.join(os.path.dirname(os.getcwd()), "Chapter_4", "cleaned_data_final.pkl")
os.makedirs(os.path.dirname(chapter_4_path), exist_ok=True)
with open(chapter_4_path, "wb") as f:
    pickle.dump(df, f)
"""

            #Create a temporary file to write the AI Python code into
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
                tmp.write(temp_code)
                tmp.flush()
                #Run the temporary Python file
                runpy.run_path(tmp.name)
                #Delete the temporary file after running
                os.remove(tmp.name)

            #Load updated cleaned dataframe from pickle file
            with open("cleaned_data_final.pkl", "rb") as f:
                df = pickle.load(f)

            #Display success message when cleaning code is applied
            st.success("Cleaning applied and saved successfully!")
            #Display updated dataframe preview
            st.dataframe(df.head())

            #Reset latest code so user knows it's been applied
            st.session_state.latest_code = ""
            st.session_state.history.append(("Bot", "Cleaning code applied and changes saved."))

        #Handle errors during cleaning code application and add to chat history
        except Exception as e:
            st.error(f"Error applying cleaning code: {e}")
            st.session_state.history.append(("Bot", f"Error: {e}"))

#Convert cleaned dataframe to CSV for download
csv = df.to_csv(index=False)
#Add download button to allow users to download cleaned data as CSV file
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="cleaned_data_final.csv",
    mime="text/csv"
)

#Add chat window to display messages
st.markdown("Cleaning History")
#Loop through the chat history stored in session state and display each message
for who, msg in st.session_state.history:
    #Check if message is from user and display it
    if who == "You":
        st.write(f"**You:** {msg}")
    #Otherwise display assistant's response as info box
    else:
        st.info(f"**Bot:** {msg}")
