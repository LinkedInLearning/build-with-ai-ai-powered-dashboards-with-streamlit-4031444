#Build with AI: AI-Powered Dashboards with Streamlit 
#Build a Simple Dashboard in Streamlit with Sample Data

#Import packages
import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
import altair as alt

#Configure page
st.set_page_config(page_title='Iris Dashboard', layout='wide')

#Write title and description
st.title('Create Iris Dataset Dashboard')

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