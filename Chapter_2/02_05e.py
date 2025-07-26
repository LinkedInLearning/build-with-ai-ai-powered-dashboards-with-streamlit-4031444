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
st.title('Error Handling')

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
st.subheader("Paste Python code to run (must define a variable `df`):")
user_code = st.text_area("Python Code", height=200)

#Define function to execute the user-submitted code
def run_code():
    #Remove any extra whitespace from the code
    code = user_code.strip()
    #Provide warning if user has not entered any code
    if not code:
        st.warning("Please paste some Python code before running.")
        return

    #Display a spinner while code is running
    with st.spinner("Executing code…"):
        try:
            #Create a temporary file to write the Python code into
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
                tmp.write(code)
                tmp.flush()
                #Run the temporary Python file and capture the results
                result = runpy.run_path(tmp.name)

            #Check if expected variable is present
            if 'df' not in result:
                #Display message if variable is missing
                st.info("Code ran, but no variable named `df` was found.")
                #Add assistant's reply to chat history
                st.session_state.chat_history.append(("Bot", "No `df` variable found."))
            else:
                #Display success message if code runs and variable is present
                st.success("Code executed successfully!")
                #Display the result when the code is run
                st.write(result['df'])
                #Add assistant's reply to chat history
                st.session_state.chat_history.append(("Bot", "Code ran successfully and returned a DataFrame."))

        #Handle syntax errors and add to chat history
        except SyntaxError as e:
            st.error(f"Syntax error in your code: {e}")
            st.session_state.chat_history.append(("Bot", f"Syntax error: {e}"))
        #Handle other errors and add to chat history
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            st.session_state.chat_history.append(("Bot", f"Unexpected error: {e}"))

#Create button on main page to run code when clicked
st.button("Run Code", on_click=run_code)

#Add chat window to display messages
st.subheader("Feedback History")
#Loop through the chat history stored in session state and display each message
for who, msg in st.session_state.chat_history:
    #Check if message is from assistant and display as info box
    if who == "Bot":
        st.info(f"**{who}:** {msg}")
    #Otherwise display message as regular text
    else:
        st.write(f"**{who}:** {msg}")

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