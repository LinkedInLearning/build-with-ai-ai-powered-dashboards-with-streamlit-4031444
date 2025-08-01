#Build with AI: AI-Powered Dashboards with Streamlit 
#Handle Errors and Provide User Feedback in Your App

#Import packages
import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
import altair as alt
from openai import OpenAI

#Open file with API key
with open("openai_key.txt") as f:
    my_api_key = f.read().strip()

#Initialize OpenAI client with your API key
client = OpenAI(api_key=my_api_key)

#Configure page
st.set_page_config(page_title="Iris Dashboard", layout="wide")

#Write title
st.title("Error Handling")

#Load Iris dataset
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["species"] = pd.Categorical.from_codes(iris.target, iris.target_names)

#Add sidebar filters
st.sidebar.header("Filter Options")
#Add species filter
species_options = st.sidebar.multiselect("Select species:", options=iris.target_names, default=list(iris.target_names))
#Allow users to change x-axis
x_axis = st.sidebar.selectbox("X-axis feature:", options=iris.feature_names, index=0)
#Allow users to change y-axis
y_axis = st.sidebar.selectbox("Y-axis feature:", options=iris.feature_names, index=1)

#Add chat widget on main page
st.subheader("Ask a question about the Iris dataset")
#Determine if chat history exists in the session state and initialize if it doesn't
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#Create text input field to allow users to type in message
user_input = st.text_input("Type your question here...", key="ui_input")
#Check if send button is clicked
if st.button("Send", key="ui_send"):
    #Provide warning if user has not entered any input
    if not user_input.strip():
        st.warning("Please enter a message before sending.")
    #Add chat history in session state is the user has entered input
    else:
        #Add user's message to chat history
        st.session_state.chat_history.append({"role":"user","content":user_input})
        #Build system prompt
        msgs = [
            {"role":"system","content":
             "You are an expert on the Iris dataset and Python. "
             "If code is needed, reply only with a complete ```python``` block. "
             "The DataFrame is available as `df`. "
             "Columns are: 'sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)', and 'species'"
             "End code with an expression that evaluates to the result, no print or return statements."}
        ] + st.session_state.chat_history
        try:
            #Send chat history to OpenAI LLM and receive response
            response = client.chat.completions.create(
                #Select model
                model="gpt-3.5-turbo",
                messages=msgs
            )
            #Gather assistant's response
            reply = response.choices[0].message.content
            #Add AI assistant's reply to chat history
            st.session_state.chat_history.append({"role":"assistant","content":reply})

        except Exception as api_err:
            #Display API error
            st.error(f"OpenAI API error: {api_err}")
            #Add API error to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": f"API error: {api_err}"})
            reply = None

        
        if reply:
            #Check if the assistant's reply starts with Python code block marker (```python)
            if reply.strip().startswith("```python"):
                #Extract the code content between the ```python and ``` markers
                code = reply.strip().split("```python")[-1].split('```')[0]
                st.subheader("Generated Python Code")
                #Display the extracted code in a code block with Python syntax highlighting
                st.code(code, language="python")

                #Prepare namespace
                ns = {"pd": pd, "df": df, "iris": iris, "st": st}

                try:
                    #Split the generated code into individual lines and remove any empty lines
                    lines = [l for l in code.splitlines() if l.strip()]
                    #Separate all lines except the last into 'body', and last line into 'last'
                    *body, last = lines
                    #Run the 'body' portion of the generated code in the namespace
                    exec("\n".join(body), ns)
                    #Evaluate the last line in the same namespace to capture any returned value
                    result = eval(last, ns)

                    st.subheader("Execution Result")
                    #Display code result
                    st.write(result)

                    #Add success message to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": "Code executed successfully!"})

                except Exception as exec_err:
                    #Display error message if an error occurs during code execution
                    st.error(f"Error executing code: {exec_err}")
                    #Add code execution error to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": f"Execution error: {exec_err}"})
            else:
                #Display result
                st.subheader("Answer")
                st.write(reply)
                #Add success message to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": "Answer delivered without code"})

st.subheader("Feedback History")
#Loop through the chat history stored in session state and display each message
for message in st.session_state.chat_history:
    role = message.get("role", "")
    content = message.get("content", "")

    #Check if message is from assistant and display as info box
    if role == "assistant":
        st.info(f"**Bot:** {content}")
    #Check if message is from user and display as info box
    elif role == "user":
        st.write(f"**You:** {content}")
    #Otherwise display message as regular text
    else:
        st.write(content)

#Filter DataFrame
filtered_df = df[df["species"].isin(species_options)]

#Display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

#Create scatter plot visualization
st.subheader("Scatter Plot")
scatter = (
    alt.Chart(filtered_df)
    .mark_circle(size=60)
    .encode(
        x=x_axis,
        y=y_axis,
        color="species",
        tooltip=iris.feature_names + ["species"]
    )
    .interactive()
)
st.altair_chart(scatter, use_container_width=True)

#Display summary statistics
st.subheader("Summary Statistics")
st.write(filtered_df.describe())

#Add dashboard footer
st.write("---")
st.write("Dashboard built with Streamlit and Altair")