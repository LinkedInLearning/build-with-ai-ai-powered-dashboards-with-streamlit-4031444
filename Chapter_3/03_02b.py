#Build with AI: AI-Powered Dashboards with Streamlit 
#Upload and Preview External Data in Streamlit

#Import packages


#Write title

#Write description


#Add file upload widget for revenue and expenses file

#Add file upload widget for location file


#Check if both files have been uploaded

    #Display a spinner while files are being processed

        #Read in revenue and expenses file

        #Read in location file

        #Merge files on 'Hotel ID' stepwise

    #Display success message when files are merged

    #Add subheader for merged data preview

    #Display first few rows of merged data


    #Add subheader for full merged data section

    #Add expander to show entire merged dataset


    ##Cache computations that return data

    #Create DataFrame to CSV conversion function


    #Convert merged dataframe to CSV for download


    #Add download button to allow users to download merged data as CSV file


#If files have not been uploaded, display an informational message
