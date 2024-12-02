import streamlit as st
import pandas as pd

st.title("Data Overview")
st.subheader('Raw Data')
st.write("This dataset began as raw data scraped from 'indeed.com'.")
st.write("The dataset contsains a little over 12,300 Data Science job postings for \
         Data Science jobs of all experience levels. Below is a sample of the original \
         raw data that show the first 50 rows:\n")
original_df = pd.read_csv('pages/originalOverview.csv')
st.write(original_df.head(50))

st.subheader('Cleaned Data Sample:')
st.write('The data had to be cleaned in several ways to get it to be usable for this project.\
         To read more details about the cleaning and encoding process, check out the\
          \'Data Preparation\' tab. Below is a sample of the cleaned data. Note that the columns\
         after \'Salary To\' change depending on the searched data.')
df = pd.read_csv('pages/cleaned_v2.csv')
st.write(df.head(50))



st.subheader("Basic Statistics")
st.write('Below is some basic statistics of the cleaned sample above. This just shows some\
         basic things like minimum value, maximum value, average, and standard deviation.')
st.write(df.describe())
st.write('While this veriosn of the data was used to compare the imputation methods, it is not the one that is used for the \
application as one used was further processed to be ready. See \'Data Preparation\' tab and \'Imputation Comparison\' tab for more details.')
