import streamlit as st

st.subheader('Let\'s Paint a Story') 
st.image("Images/gol.jpeg", caption="The Game of Life")
st.write('Have you ever played the \'The Game of Life\'?  Well, if you have not, then here\'s a brief overview.\
         The goal of the game is to make the most wealth when you retire. Your first decision in the game is\
         to choose between getting a college degree or just start playing and look for a job. Every time you reach \
         A career point, you will be faced with three jobs to choose from. Some of them will require having a\
         College degree while others will not. You probably have guessed it by now, yes jobs that require a college\
         degree pay much better. \nThroughout the game, you will make important decisions that will affect your \
         \'life\' such as getting married, investing some money, or choosing another career. Looking at this\
         one might think, isn\'t or life just that? Making decisions that will affect how our life goes?\n')
st.write("As a college student, you might need to make some decisions that may affect your life on the long run.\
         In this project, we try to analyze what effect learning some programming languages and/or technologies\
         during your degree on your long-term career. Even if you are not a college student, don't you want \
         to know whether it is worth spending time and'/or money learning a language or a technology? Will that\
         land you the job you're looking for? How much will you be paid? How many employers are looking for these\
         qualifications?\n")
st.write("In this application, we will try to help you decide whether you need to put in the effort or not. To do so\
         we will be using real job posting data and analyze the data to get an idea of the job market requirements\
        , employers, needed qualifications, salaries ...etc. Checkout \'Explore Jobs Data\' tab for more info. \
         To get more information about the data used in this application, checkout the 'About Data' tab.")
st.subheader("Application Sections")
st.write("""There are multiple sections of this applications. Some are aimed towards the user and others twoards data scientists.
         Each page will have a prefix to denote a section/part of the application. Below is an explanation of these prefixes:
- U: User pages.
    - These pages are aimed towards an application user and will contain visualizations and user interaction items such as
         inputs, menus and interactive plots.
- DS: Data Scientists Pages.
    - These pages will explain the data science concepts used such as data pre-processing, imputation ...etc.
    - These will also include data analysis, results, thoughts, and conclusions about the data.         
- I: Information Pages.
    - These pages will contain general progect information. """)