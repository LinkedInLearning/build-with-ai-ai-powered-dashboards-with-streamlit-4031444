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
st.title("")

#Check if cleaned dataset exists and load it if available

    #Display success message when cleaned data is loaded

    #Load revenue and expenses file
    df_rev_exp = pd.read_excel("Landon_Hotel_Revenue_And_Expenses.xlsx")
    #Load location file
    df_loc = pd.read_excel("Landon_Hotel_Location.xlsx")
    #Merge files on 'Hotel ID'
    df = df_rev_exp.merge(df_loc, on="Hotel ID", how="outer")
    #Display success message when raw data is loaded


#Add subheader for current data preview
st.subheader("")
#Display first few rows of current dataframe
st.dataframe(df.head())

#Determine if chat history exists in the session state and initialize if it doesn't


#Create text input area for users to describe their cleaning instructions


#Determine if AI-generated cleaning code exists in the session state and initialize if it doesn't


#Check if 'Generate Cleaning Code' button is clicked
if st.button(""):
    #Provide warning if user has not entered a cleaning instruction
    if not user_prompt.strip():
        st.warning("")
    else:
        #Add user's message to chat history
        st.session_state.history.append(("You", ))
        #Display spinner while querying AI
        with st.spinner(""):
            try:
                #Send prompt and instructions to OpenAI LLM and receive response
                resp = client.chat.completions.create(
                    #Select model
                    model="gpt-3.5-turbo",
                    messages=[
                        #Define assistant's role and instructions
                        {"role": "system", "content": (
 
                        )},
                        #Send user's prompt
                        {"role": "user", "content": }
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
                st.subheader("")
                #Display extracted AI-generated code with syntax highlighting
                st.code(clean_answer, language="python")

                #Save AI-generated code in session state for possible application later
                st.session_state.latest_code = clean_answer

                #Add assistant's reply to chat history
                st.session_state.history.append(("Bot", ))

            #Handle API and code extraction errors and add to chat history
            except Exception as e:
                st.error(f"AI error: {e}")
                st.session_state.history.append(("Bot", f"Error: {e}"))

#Check if AI-generated cleaning code is available and if 'Apply & Save Cleaning Change' button is clicked

            #Save current dataframe to a pickle file for use by temp script
            with open(".pkl", "wb") as f:
                pickle.dump(df, f)

            #Create temporary Python script containing AI-generated cleaning code
            temp_code = f"""
import pickle


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
            with open(".pkl", "rb") as f:


            #Display success message when cleaning code is applied

            #Display updated dataframe preview


            #Reset latest code so user knows it's been applied

            st.session_state.history.append(("Bot", ))

        #Handle errors during cleaning code application and add to chat history
        except Exception as e:
            st.error(f" {e}")
            st.session_state.history.append(("Bot", f"Error: {e}"))

#Convert cleaned dataframe to CSV for download

#Add download button to allow users to download cleaned data as CSV file


#Add conversation history window
st.markdown("### Conversation")
#Loop through the chat history stored in session state and display each message
for who, msg in st.session_state.history:
    #Check if message is from user and display it
    if who == "You":
        st.write(f"**You:** {msg}")
    #Otherwise display assistant's response as info box
    else:
        st.info(f"**Bot:** {msg}")
