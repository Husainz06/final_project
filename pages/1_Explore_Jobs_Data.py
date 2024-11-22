import pandas as pd
import plotly.express as px
import streamlit as st
st.title('Dataset Analysis')
# Load your data
data = pd.read_csv('pages/knn_imputed_v2.csv')
st.subheader('Salary vs Location Visualization')
st.write('The following plot shows the salary ranges and distributions for different jobs accross the states.\
You can hover over a dot to show job titles and salary information.')
# Create a scatter plot for salary vs location
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




st.subheader('Job Counts ans Average Salaries per Location')
st.write('The location seems to affect the number of jobs and the average salary. To check this out, try\
         selecting from the following menu:')
#Upadted plot

# Create a container for the checkboxes
# Create a container for the checkboxes
with st.container():
    qualifications = ['Python', 'Java', 'C++', 'SQL', 'Javascript', 'linux']
    
    # Create horizontal checkboxes
    cols = st.columns(len(qualifications))
    selected_qualifications = {}
# Filter data based on selected qualifications
filtered_data = data.copy()
average_salary_by_location = filtered_data.groupby('Location')['Average Salary'].mean().reset_index()
# Count the number of jobs requiring each qualification by location
job_counts = filtered_data.groupby('Location').size().reset_index(name='Job Count')
# Create a Plotly bar chart for job counts per location
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

# Create a Plotly bar chart for average salary per location
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
with st.container():
    st.write("Select Qualifications to Filter:")
    qualifications = ['Python', 'Java', 'C++', 'SQL', 'Javascript', 'linux']
    
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

# Display the selected plot with unique keys
if option == 'Job Count by Location':
    st.subheader('Job Counts Per Location')
    st.write('Certain location may have different industry requirements and therefore may have \
    different qualification requirements. The following plot shows the job count per location based \
    on qualifications. You can check/uncheck qualifications to see the job counts.')
    st.plotly_chart(fig1, key="job_count_plot")
else:
    st.subheader('Average Salary Per State - Qualification Based')
    st.write('Having experience in one or more programming languages and being familiar with some technologies \
    is a big factor in getting a job which can also affect the salary range. Use the following plot to find \
    the average salary per state based on the qualifications listed above the plot. \
    Check/uncheck any of the qualifications to see the salary ranges.')
    st.plotly_chart(fig2, key="salary_plot")


st.subheader('Relationship Between Salary and Qualifications')
st.write('While experience level plays a role in the salary range, there are other factors that \
may affect that. Moreover, some jobs may ask for more than one technology/qualification. The question \
we are trying to answer here is \'is there a correlation between the different features of the data?\' \
For example, is there a correlation between Python and SQL? which helps you answer the following question \
I\'m very experienced in Python, do I need to learn SQL? To answer such questions, let\'s look at the following \
plot that shows the correlation between different features of the data.')
st.image("Images/ corr_matrix.png", caption="Correlation Matrix")
st.write("When we look at the plot above we can answer the question we asked earlier. As we can see there is \
a positive correlation between Python and SQL which tells us that there's a good percentage of jobs that require\
 both.")
