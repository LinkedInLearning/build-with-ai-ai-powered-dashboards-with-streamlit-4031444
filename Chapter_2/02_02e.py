#Build with AI: AI-Powered Dashboards with Streamlit 
#Add a Chat Widget to Your App UI

#Import packages
import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
import altair as alt

#Configure page
st.set_page_config(page_title='Iris Dashboard', layout='wide')

#Write title and description
st.title('Add Chat Widget')

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

#Add chat widget in sidebar
st.sidebar.header('Chat Widget')
#Determine if chat history exists in the session state and initialize if it doesn't
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

#Create text input field in sidebar to allow users to type in message
user_input = st.sidebar.text_input('Type a message...', key='ui_input')
#Check if send button is clicked
if st.sidebar.button('Send', key='ui_send'):
    #Add chat history in session state is the user has entered input
    if user_input:
        st.session_state.chat_history.append(f'You: {user_input}')

st.subheader('Chat Window')
#Loop through the chat history stored in session state and display each message
for message in st.session_state.chat_history:
    st.write(message)
    
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
