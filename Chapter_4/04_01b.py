#Build with AI: AI-Powered Dashboards with Streamlit 
#Generate Data Visualizations Using AI Prompts

#Import packages

#Open file with API key


#Initialize OpenAI client with your API key


#Configure page


#Write title


#Create directory to store chart files if it doesn't already exist


#Check if cleaned dataset exists, stop app if not found


#Load cleaned dataset from pickle file


#Add subheader for cleaned data preview

#Display first few rows of cleaned data


#Create text input for user to name their chart


#Create text input area for user to describe desired chart


#Check if 'Generate & Save Chart' button is clicked

    #Provide warning if user has not entered a description

        #Display spinner while querying AI

                #Send prompt and system instructions to OpenAI LLM and receive response

                    #Select model

                        #Provide system instructions

                        #Send user's chart description


                #Extract AI's reply text and remove markdown/code block formatting


        #Add subheader for AI-generated code preview

        #Display AI's generated Altair code


        #Attempt to safely execute the AI-generated Altair code


            #Check if chart variable was successfully created


            #Add subheader and display the newly generated chart


            #Save AI-generated code to a .py file in the charts directory


        #Handle errors if code execution or chart display fails


#Add subheader for existing saved charts


#Loop through previously saved chart files in the charts directory

    #Skip any non-Python files


    #Display filename as a bullet point

        #Open and read chart code from file


        #Execute saved Altair code safely and display the chart


    #Handle errors if chart loading or execution fails

