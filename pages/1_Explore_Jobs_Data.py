import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
import regex as re
import numpy as np
import plotly.figure_factory as ff
st.title('Explore Jobs and Salaries')
st.write('This page analyzes data science job listings and extracts jobs and salaries information based \
         on the search parameters you enter. To begin enter a list of languages and or qualifications \
         in the search box. Make sure to have a space separation between entries and hit the \'Enter\'\
         key when done.')
user_input = st.text_input("Languages and/or qualifications:")
loading_message_placeholder = st.empty()
user_selected_langs = []
if user_input:
    # using spinner while loading data
    with st.spinner('Processing dataset, please wait...'):
        user_selected_langs = list(user_input.split())
        # Cleaning Data:
        # functions
        # Read locations and convert to state codes
        def extract_state_codes(locations):
            # Dictionary of state names and their abbreviations
            state_abbreviations = {
                "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
                "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
                "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
                "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
                "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
                "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
                "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
                "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
                "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
                "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
                "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
                "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
                "Wisconsin": "WI", "Wyoming": "WY"
            }
            
            state_codes = []  # Use a list to preserve order
            for s in locations:
                first = False
                second = False
                us = False
                for k in state_abbreviations.keys():
                    if k in s:
                        state_codes.append((state_abbreviations.get(k)))
                        first = True
                        break
                if not first:
                    for v in state_abbreviations.values():
                        if v in s:
                            state_codes.append(v)
                            second = True
                            break
                if not first and not second:
                    state_codes.append('US')

            return state_codes

        # Read salary information from salary column and convert to high and low lists
        def get_salaries(sals):
            low_salaries = []
            high_salaries = []

            for range_str in sals:
                if len(str(range_str))>0:
                    numbers = re.findall(r'[\$]?([\d,]+)', str(range_str))
                    if len(numbers) == 2:
                        try:
                            low_salary = int(numbers[0].replace(',', ''))
                            high_salary = int(numbers[1].replace(',', ''))
                            # Adjusting hourly salary to annual
                            if low_salary < 150:
                                low_salary *= 8 * 5 * 52
                                low_salaries.append(low_salary)
                            elif low_salary < 300000 :
                                low_salaries.append(low_salary)
                            else:
                                low_salaries.append(np.nan)
                            if high_salary < 150:
                                high_salary *= 8 * 5 * 52
                                high_salaries.append(high_salary)
                            elif high_salary < 300000 :
                                high_salaries.append(high_salary)
                            else:
                                high_salaries.append(np.nan)
                        
                            
                        except ValueError as e:
                            print(f"ValueError: {e} for entry: {range_str}")
                            low_salaries.append(np.nan)
                            high_salaries.append(np.nan)

                    elif len(numbers) == 1:
                        try:
                            low_salary = int(numbers[0].replace(',', ''))
                             # Adjusting hourly salary to annual
                            if low_salary < 150:
                                low_salary *= 8 * 5 * 52
                                low_salaries.append(low_salary)
                            elif low_salary < 300000:
                                low_salaries.append(low_salary)
                            else:
                                low_salaries.append(np.nan)
                            high_salaries.append(np.nan)
                        except ValueError as e:
                            print(f"ValueError: {e}")
                            low_salaries.append(np.nan)
                            high_salaries.append(np.nan)
                    else:
                        low_salaries.append(np.nan)
                        high_salaries.append(np.nan)               

                else:
                    low_salaries.append(np.nan)
                    high_salaries.append(np.nan)

            return low_salaries, high_salaries
            
        # Read salaries from description column and convert to high and low arrays
        def get_salaries_description(descriptions):
            low_salaries = []
            high_salaries = []
            
            # Define a regex pattern for matching salary information
            salary_pattern = re.compile(r'\$([\d,]+)(?:\s*-\s*\$?([\d,]+))')
            for description in descriptions:
                #if the job has no description or is not a string, add np.nan
                if pd.isna(description) or not isinstance(description, str):
                    low_salaries.append(np.nan)  
                    high_salaries.append(np.nan)
                    # ignore the rest and move to the next iteration
                    continue 
                # compare the job description with the defined regex
                if salary_pattern.search(description):
                    # before the dash
                    low_salary_str = salary_pattern.search(description).group(1)
                    # after the dash
                    high_salary_str = salary_pattern.search(description).group(2)

                    try:
                        # Convert low salary to int
                        low_salary = int(low_salary_str.replace(',', '').strip())
                        # Convert to annual if needed
                        if low_salary < 150:
                            low_salary *= 8 * 5 * 52
                            low_salaries.append(low_salary)
                        elif low_salary <300000 :
                            low_salaries.append(low_salary)
                        else:
                            low_salaries.append(np.nan)
                        # Check if the high salary information is available, convert it to int
                        if high_salary_str:
                            high_salary = int(high_salary_str.replace(',', '').strip())
                            # Convert to annual if needed
                            if high_salary < 150:
                                high_salary *= 8 * 5 * 52
                                high_salaries.append(high_salary) # change this
                            elif high_salary <300000:
                                high_salaries.append(high_salary) # change this
                            else:
                                high_salaries.append(np.nan)
                        # append np.nan if no high salary information is available
                        else:
                            high_salaries.append(np.nan)
                    # handle exceptions by adding np.nan if everything else failed   
                    except ValueError:
                        low_salaries.append(np.nan)  
                        high_salaries.append(np.nan)
                # if no description found or not a string, add np.nan
                else:
                    low_salaries.append(np.nan)
                    high_salaries.append(np.nan)

            return low_salaries, high_salaries

        # Merge salaries from both sources
        def merge_salaries(from_salaries , from_descriptions):
            result = []
            for i in range(len(from_salaries)):
                if not np.isnan(from_salaries[i]):
                    result.append(from_salaries[i])
                    continue
                result.append(from_descriptions[i])
            return result
        # Parse the description to extract the languages/qualifications and encode them
        def parse_languages(job_descriptions, languages_list):
            row = 0
            result = [[0 for _ in range(len(languages_list))] for _ in range(len(job_descriptions))]
            for i in range(len(job_descriptions)): 
                for j in range(len(languages_list)):
                    if str(languages_list[j]).lower() in str(job_descriptions[i]).lower():
                        result[i][j] = 1
            return result
        # convert a column into a list of strings
        # needed for some functions
        def col_to_str_list(col):
            l = []
            for e in col:
                l.append(str(e))
            return l 
        # Create a cleaned dataset
        # read dataset
        # This is the dataset after knn imputation
        data = pd.read_csv('pages/us_jobs_data_knn_imputed_v2.csv')
        # Extract state codes into location list ------ need to check why it is adding more data
        location = extract_state_codes(col_to_str_list(data['job_location']))

        # Extract salary information from salaries column into hi, low lists
        low , hi = get_salaries(data['job_salary'])

        # Extract salary information from job descriptions into hi2, low2 lists
        low2 , hi2 = get_salaries_description(data['job_summary']) 

        # Merge salary lists
        low_range = merge_salaries(low , low2)
        high_range = merge_salaries(hi , hi2)

        # Define a list of languages/qualifications
        lang_qual = user_selected_langs
        qualifications = parse_languages(data['job_summary'], lang_qual)
        generated = {
            'Job Title': col_to_str_list(data['job_title']),
            'Location': location,
            'Salary From': low_range,
            'Salary To': high_range
            
        }
        cleaned_data = pd.DataFrame(generated)
        # Add the encoded columns
        flipped_matrix = [list(row) for row in zip(*qualifications)]
        cols= ['t1','t2']
        for i in range(len(flipped_matrix)):
            cleaned_data[lang_qual[i]] = flipped_matrix[i]

        
    # ---------------------------------------------  Plotting and Analysis section
        st.header('Plotting Based on Your Selection:')
       # loading_message_placeholder.text('Creating plots....\nPlease wait.')
        
        data = cleaned_data

        data = data[data[lang_qual].ne(0).any(axis=1)]
        st.write("Number of jobs found:",len(data))
        if(len(data)==0):
            st.write("Sorry! The language(s) you entered were not found.\n Please try another list!")
        else:
            st.subheader('Salary vs Location Visualization')
            st.write('The following plot shows the salary ranges and distributions for different jobs accross the states.\
            You can hover over a dot to show job titles and salary information.')
            # Create a scatter plot for salary vs location
            with st.spinner('Creating plots, please wait...'):    
                #with st.spinner('Creating plot, please wait...'):
                fig = px.scatter(
                    data,
                    x='Location',
                    y='Salary From',  # Default to showing 'Salary From'
                    color='Location',  # Color points by location
                    title='Salary vs Location',
                    height=600,
                )

                # Update hover information to format salaries with a dollar sign
                fig.update_traces(
                    hovertemplate=(
                        'Job Title: %{hovertext}<br>' +
                        'Salary From: $%{y:,.0f}<br>' +  # Added dollar sign here
                        'Salary To: $%{customdata[0]:,.0f}<br>' +  # Added dollar sign here
                        '<extra></extra>'
                    ),
                    hovertext=data['Job Title'],
                    customdata=data[['Salary To']].values
                )
                # Update layout for better visibility
                fig.update_layout(
                    xaxis_tickangle=-45,
                    xaxis=dict(showticklabels=False)  # Remove ticks on the x-axis
                )

                st.plotly_chart(fig)
                # Fill NaN values in salary columns with 0 for calculations
                data['Salary From'] = data['Salary From'].fillna(0)
                data['Salary To'] = data['Salary To'].fillna(0)

                # Calculate average salary
                data['Average Salary'] = (data['Salary From'] + data['Salary To']) / 2

                # Plotting count and average salary based on user selection
                st.subheader('Job Counts and Average Salaries per Location')
                st.write('The location seems to affect the number of jobs and the average salary. To check this out, try selecting from the following menu:')

                # Create a container for the checkboxes
                with st.container():
                    qualifications = user_selected_langs
                    
                    # Create horizontal checkboxes
                    cols = st.columns(len(qualifications))
                    selected_qualifications = {}
                    
                    for i, qual in enumerate(qualifications):
                        # Set a unique key for each checkbox
                        selected_qualifications[qual] = cols[i].checkbox(qual, value=True, key=f"{qual}_{i}")

                # Filter data based on selected qualifications
                filtered_data = data.copy()  # Replace 'data' with your actual dataframe
                for qual, selected in selected_qualifications.items():
                    if not selected:
                        filtered_data = filtered_data[filtered_data[qual] == 0]

                # Group by location and calculate the average salary
                average_salary_by_location = filtered_data.groupby('Location')['Average Salary'].mean().reset_index()

                # Group by location and calculate the job count
                job_counts = filtered_data.groupby('Location').size().reset_index(name='Job Count')

                # Create Plotly bar charts inside the container where filtering occurs
                # Create the Job Count plot
                fig1 = px.bar(
                    job_counts,
                    x='Location',
                    y='Job Count',
                    color='Location',  # Color by location
                    title='Count of Jobs by Location Based on Qualifications',
                    labels={'Job Count': 'Job Count', 'Location': 'Location'},
                )

                # Update layout for better visibility for Job Count plot
                fig1.update_layout(
                    xaxis_tickangle=-45,
                    xaxis=dict(showticklabels=False)  # Remove ticks on the x-axis
                )

                # Create the Average Salary plot
                fig2 = px.bar(
                    average_salary_by_location,
                    x='Location',
                    y='Average Salary',
                    color='Location',  # Color by location
                    title='Average Salary per Location',
                    labels={'Average Salary': 'Average Salary ($)', 'Location': 'Location'},
                )

                # Update layout for better visibility for Average Salary plot
                fig2.update_layout(
                    xaxis_tickangle=-45,
                    xaxis=dict(showticklabels=False)  # Remove ticks on the x-axis
                )

                # Streamlit dropdown to select between plots
                option = st.selectbox(
                    'Select a plot to display:',
                    ('Job Count by Location', 'Average Salary by Location')
                )

                # Display the selected plot
                if option == 'Job Count by Location':
                    st.subheader('Job Counts Per Location')
                    st.write('Certain locations may have different industry requirements and therefore may have different qualification requirements. The following plot shows the job count per location based on qualifications. You can check/uncheck qualifications to see the job counts.')
                    st.plotly_chart(fig1, key="job_count_plot")
                else:
                    st.subheader('Average Salary Per Location - Qualification Based')
                    st.write('Having experience in one or more programming languages and being familiar with some technologies is a big factor in getting a job, which can also affect the salary range. Use the following plot to find the average salary per location based on the qualifications listed above the plot. Check/uncheck any of the qualifications to see the salary ranges.')
                    st.plotly_chart(fig2, key="salary_plot")
    def plot_correlation_heatmap(data):
        # Read the data from the uploaded file
        #data = pd.read_csv(file)
        
        # Remove the unnamed column (assuming it's the first column)
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
        data = data.drop(columns=['Average Salary'])
        # Select only numeric columns for correlation
        numeric_data = data.select_dtypes(include=['float64', 'int64'])
        
        # Compute the correlation matrix
        correlation_matrix = numeric_data.corr()
        
        # Flip the order of the columns and rows
        correlation_matrix = correlation_matrix[::-1].reset_index().set_index('index')
        
        # Create an interactive heatmap
        fig = ff.create_annotated_heatmap(
            z=correlation_matrix.values,
            x=list(correlation_matrix.columns),
            y=list(correlation_matrix.index),
            annotation_text=correlation_matrix.round(2).values,
            colorscale='Viridis'
        )
        
        # Update layout for better visualization
        fig.update_layout(
            title='Correlation Matrix',
            height=600,
            width=800
        )
        
        # Display the heatmap in Streamlit
        st.plotly_chart(fig)
    st.subheader('Relationship Between Salary and Qualifications')
    st.write('While experience level plays a role in the salary range, there are other factors that \
    may affect that. Moreover, some jobs may ask for more than one technology/qualification. The question \
    we are trying to answer here is \'is there a correlation between the different features of the data?\' \
    For example, is there a correlation between Python and SQL? which helps you answer the following question \
    I\'m very experienced in Python, do I need to learn SQL? To answer such questions, let\'s look at the following \
    plot that shows the correlation between different features of the data.')
    with st.spinner('Generating correlation heatmap, please wait...'):
        plot_correlation_heatmap(data)
else:
    st.write("")
loading_message_placeholder.text('')
#st.image("Images/ corr_matrix.png", caption="Correlation Matrix")
#st.write("When we look at the plot above we can answer the question we asked earlier. As we can see there is \
#a positive correlation between Python and SQL which tells us that there's a good percentage of jobs that require\
# both.")
