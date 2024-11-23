import streamlit as st

st.title("Data Preparation")

st.write("The dataset began as raw scraped data with lots of un-needed information.\
         The first step prior to using the data is cleaning it to make it ready to use.\
         Below we take a look at each cleaning and preparation phase and explain why it was\
         needed and how it was done.")
st.subheader("Job Location")
st.write('One of the first columns that needed to be cleaned was the location columns as the\
         data in the column was not consistent. Some postings had state name, others had city, State\
         format and other just say \'United States\'. We needed to make sure to get the state \
         appreviations from each of those postings to help in the analysis and visualization down\
          the line. ')
st.write("To accomplish this, we used a dictionary conatining state names and appreviations\
          and wrote the code to match them and put them in a list to be used in the output\
          dataset.")
st.image('Images/edcode_states.png', caption = 'State Appreviation Encoding')

st.subheader("Job Salary")
st.write('Gettig the job salary was one of the most challenging parts of the data cleaning. This\
          is because of many issues. First, the salary information can sometimes be found in the\
          salary column as a single value e.g. \$75,000. Other times it is a range e.g. \$70,000 - \$80,000\
         or \$70,000 to \$80,000. Sometimes it is not an annual rate but an hourly rate. The second issue is that\
          sometimes the salary information is found within the job\'s description, which required a different\
          approach to extract the salary information')
st.write("To tackle this problem, we implemented two functions that extract the job salary information. Both\
          functions utilized Regular Expression to extract the salary information. In both scenarios, the\
          extracted data needed to be saved into two lists, one containing the high salary range and the\
          other contained the low salary range. In the case of missing salary information, the code inserts\
          'np.nan' in the cell.")
st.image('Images/get_sals1.png', caption = 'Extracting Salary Information from Salary')
st.image('Images/get_sals2.png', caption = 'Extracting Salary Information from Job Description')

st.write("After extracting the salary data, the salaries extracted from both locations needed to be merged\
          into one list for high salaries, and another list for low salaries. To do that, we defined the following function.")
st.image('Images/merge_sals.png', caption = 'Merging Salaries')

st.subheader("Languages  and Qualifications")
st.write("To make it easier to analyze and use the data down the line, we decided to perform binary encoding on the \
          Langauges and qualifications. The idea here is to pass the required languages and qualifications as an array\
          and use that array to first look these up in the job descirption, and second use them as column names for the\
          generated dataset. Doing this ensures that we can dynamically create new datasets based on whatever the user\
         searches when we implement a search functionality.")
st.image('Images/get_langs.png', caption = 'Extracting and Encoding Languages and Qualifications')

st.write('The results from calling each of the above function is then combined into one dataset. Some results needed\
          further processing before adding them into the datase. For a more detailed code, look at \'data_cleaning_encoding.py\'\
          in the application\'s GitHub repo.')
