#Build with AI: AI-Powered Dashboards with Streamlit 
#Test Your App and Gather User Feedback

#Import packages
import pandas as pd
import os, pickle
import altair as alt

#Test the cleaned dataset exists and loads correctly

    #Confirm the pickle file exists


    #Load the dataset from the pickle file
    with open("cleaned_data_final.pkl", "rb") as f:
        df = pickle.load(f)

    #Verify the dataset is not empty


    #Confirm essential expected column exists



#Test that chart files exist in the 'charts' directory


    #Confirm charts directory exists

    #Collect all Python files within the directory


    #Confirm at least one chart file exists



#Test each chart file executes and produces a valid Altair chart

    #Read chart code from file
    with open(os.path.join(), encoding="utf-8") as f:
        code = f.read()

    #Load the cleaned dataset for use during chart execution
    with open("cleaned_data_final.pkl", "rb") as f:
        df = pickle.load(f)

    #Initialize local variables for exec environment
    local_vars = {"df": df, "alt": alt}

    #Execute the chart code and validate result
    try:
        exec(code, {}, local_vars)
        #Check that 'chart' variable was created
        "chart" in local_vars
        chart = local_vars["chart"]
        #Ensure 'chart' is an instance of an Altair Chart


        #Fail test if any exception occurs



#Test that the AI-generated dashboard layout file exists

    #Confirm the file exists in the project directory
    os.path.exists("dashboard_layout.py")


#Test the dashboard layout code runs successfully using dummy streamlit components

    #Read layout code from file
    with open("dashboard_layout.py", "r", encoding="utf-8") as f:
        layout_code = f.read()

    #Load chart files into a dictionary of charts
    charts = {}

    #Loop through each file in the 'charts' directory
    for fname in os.listdir("charts"):
        #Check if the file is a Python file (ends with '.py')
        if fname.endswith(".py"):
            #Open the chart Python file and read its code content as a string
            with open(os.path.join("charts", fname), encoding="utf-8") as fchart:
                code = fchart.read()
            
            #Create a local namespace with a dummy DataFrame and Altair module for chart code execution
            local_vars = {"df": pd.DataFrame(), "alt": alt}

            #Execute the chart code safely in an isolated local_vars context
            exec(code, {}, local_vars)

            #If a variable named 'chart' was created in the executed code, store it in the charts dictionary
            if "chart" in local_vars:
                #Use the file name (without extension) as the chart's dictionary key
                chart_key = os.path.splitext(fname)[0]
                #Add the chart object to the charts dictionary
                charts[chart_key] = local_vars["chart"]

    #Create a dummy container class to simulate context manager behavior (for testing dashboard layout)

        #Define __enter__ method to allow use of 'with' statements


        #Define __exit__ method to properly handle context manager exit calls


        #Handle attribute calls for the dummy container

            #If 'columns' is called, simulate Streamlit's st.columns by returning a list of dummy containers

            #For any other Streamlit method call, return a no-op lambda function


    #Create a dummy Streamlit class to mock Streamlit API calls within layout code

            #If attribute is a container (container, sidebar, expander), return a dummy container

            #If attribute is 'columns', return list of dummy containers

            #For all other Streamlit calls (st.title, st.altair_chart, etc.), return a no-op lambda


    #Attempt to run the layout code using dummy Streamlit environment and chart dictionary

        #Fail test if execution raises an error
