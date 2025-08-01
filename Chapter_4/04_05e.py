#Build with AI: AI-Powered Dashboards with Streamlit 
#Test Your App and Gather User Feedback

#Import packages
import pandas as pd
import os, pickle
import altair as alt
import pytest

#Test the cleaned dataset exists and loads correctly
def test_cleaned_data_load():
    """Check that cleaned dataset exists, loads successfully, and contains expected columns."""
    #Confirm the pickle file exists
    assert os.path.exists("cleaned_data_final.pkl"), "Missing cleaned dataset."

    #Load the dataset from the pickle file
    with open("cleaned_data_final.pkl", "rb") as f:
        df = pickle.load(f)

    #Verify the dataset is not empty
    assert not df.empty, "Loaded DataFrame is empty."

    #Confirm essential expected column exists
    assert "Hotel ID" in df.columns, "Expected column 'Hotel ID' missing."


#Test that chart files exist in the 'charts' directory
def test_chart_files_exist():
    """Verify that at least one chart file exists in the charts directory."""
    CHART_DIR = "charts"

    #Confirm charts directory exists
    assert os.path.exists(CHART_DIR), "Charts directory missing."

    #Collect all Python files within the directory
    py_files = [f for f in os.listdir(CHART_DIR) if f.endswith(".py")]

    #Confirm at least one chart file exists
    assert py_files, "No chart files found."


#Test each chart file executes and produces a valid Altair chart
@pytest.mark.parametrize("chart_file", [f for f in os.listdir("charts") if f.endswith(".py")])
def test_chart_execution(chart_file):
    """Ensure each chart file runs successfully and produces a valid Altair chart object."""
    #Read chart code from file
    with open(os.path.join("charts", chart_file), encoding="utf-8") as f:
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
        assert "chart" in local_vars, f"'chart' not defined in {chart_file}"
        chart = local_vars["chart"]
        #Ensure 'chart' is an instance of an Altair Chart
        assert isinstance(chart, alt.TopLevelMixin), f"{chart_file} did not produce an Altair chart."
    except Exception as e:
        #Fail test if any exception occurs
        pytest.fail(f"{chart_file} failed to execute: {e}")


#Test that the AI-generated dashboard layout file exists
def test_layout_file_exists():
    """Check that the dashboard layout file created by AI exists."""
    #Confirm the file exists in the project directory
    assert os.path.exists("dashboard_layout.py"), "Missing dashboard_layout.py file."


#Test the dashboard layout code runs successfully using dummy streamlit components
def test_layout_execution():
    """Confirm that AI-generated dashboard layout code runs without errors using dummy Streamlit objects."""
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
    class DummyContainer:
        #Define __enter__ method to allow use of 'with' statements
        def __enter__(self):
            return self

        #Define __exit__ method to properly handle context manager exit calls
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        #Handle attribute calls for the dummy container
        def __getattr__(self, name):
            #If 'columns' is called, simulate Streamlit's st.columns by returning a list of dummy containers
            if name == "columns":
                return lambda n: [self for _ in (range(n) if isinstance(n, int) else n)]
            #For any other Streamlit method call, return a no-op lambda function
            return lambda *args, **kwargs: None

    #Create a dummy Streamlit class to mock Streamlit API calls within layout code
    class DummyStreamlit:
        def __getattr__(self, name):
            #If attribute is a container (container, sidebar, expander), return a dummy container
            if name in ["container", "sidebar", "expander"]:
                return lambda *args, **kwargs: DummyContainer()
            #If attribute is 'columns', return list of dummy containers
            if name == "columns":
                return lambda n: [DummyContainer() for _ in (range(n) if isinstance(n, int) else n)]
            #For all other Streamlit calls (st.title, st.altair_chart, etc.), return a no-op lambda
            return lambda *args, **kwargs: None

    #Attempt to run the layout code using dummy Streamlit environment and chart dictionary
    try:
        exec(layout_code, {}, charts | {"st": DummyStreamlit()})
    except Exception as e:
        #Fail test if execution raises an error
        pytest.fail(f"Dashboard layout failed to execute: {e}")