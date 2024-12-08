import streamlit as st
import pandas as pd
# Need to update this page to add the new data sources
# Proof read the paragraphs

st.title("Data Overview")
st.write("For this application, we have used multpile datasets. Below,we will discuss each one of these \
         datasets.")
st.header('Data Science Job Postings')
st.subheader('Raw Data')
st.write("This dataset began as raw data scraped from 'indeed.com'.")
st.write("The dataset contains a little over 12,300 Data Science job postings for \
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
st.write('While this version of the data was used to compare the imputation methods, it is not the one that is used for the \
application as one used was further processed to be ready. See \'Data Preparation\' tab and \'Imputation Comparison\' tab for more details.')

st.header('Programming Language Popularity')
st.subheader('Wikipedia/GitHub Popularity')
st.write('This dataset contains a lot of useful information that helped us in the analysis. It contains \
         things like number of jobs, GitHub repositories, Wikipedia page visits...etc. Below is a sample \
         from this dataset.')
wiki = pd.read_csv('pages/languages_gitbub_wikipedia.csv')
st.write(wiki.head(50))
st.write('With this dataset, we did not need to do any cleaning as the data in the columns we needed did not \
         have any missingness. However, we needed to filter the data to be compatible with the popularity \
         dataset that we discuss below. This dataset had many languages that are not present in the other \
         dataset and trying to combine them will results in a lot of missingness. Since the next dataset \
         is the one we want to use for forecasting, we do not want any missingness there and at the same \
         time, we do not want any imputed data as we want our prediction to be as accurate as possible.')

st.subheader('Language Tutorial Search Trends')
st.write('This dataset is the one we used for forecasting as it contains historical language popularity \
         data that is based on Google\'s search trends for language tutorials. A snapshot of this dataset \
         can be seen below.')
trends = pd.read_csv('pages/Popularity of Programming Languages from 2004 to 2024.csv')
st.write(trends.head(50))
st.write('As we have established in the \'Job Market Trajectory\' page, there is a strong correlation \
         between language popularity and the number of available jobs. For this reason, we combined \
         the knowledge we can gain from the three datasets to try to predict the trajectory of data science \
         jobs based on the trajectory of the languages that are required for these jobs.')
