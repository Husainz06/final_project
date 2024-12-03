import streamlit as st
# Proof read the paragraphs
st.title("Challenges and Solutions")
st.write("During the implementation of this application, we have faced multiple challenges. \
         We will discuss them here along with the solutions we have used to conquer them so \
         other developers may use some similar solutions when facing similar problems.")

st.subheader("Data Preparation")
st.write("Since we were dealing with raw job data, there was a lot to process to be able to use the data. \
         One of the challenges we faced is when extracting salary information form job descriptions. \
         As some descriptions contained URLs, our extraction approach was pulling any number in the \
         URL as the salary information. To solve this, we had to revisit our regular expression and check \
         the length of the string containing the number to make sure it is within the length of the salaries' \
         length.")
st.subheader("Slow Bigram Processing")
st.write("When trying to extract bigrams and trigrams, we needed to tokenize all the job descriptions, \
         which was taking a very long time as the dataset is not small. To solve this problem, we created \
         some files to store all tokens and to store n-grams as they get created to avoid having to \
         recreate tokens and tokens and n-grams everytime the user searches for them. ")
st.subheader("Cluttered Figures")
st.write("Some figuress get cluttered when the user is searching for multiple terms. This makes the plots \
         hard to read. To resolve this, we implemented dynamic figure resizing based on the number of \
         components that are going to be on the plot. This number is determined by the number of keywords \
         the user enters.")