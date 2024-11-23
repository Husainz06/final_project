import streamlit as st
import pandas as pd
st.title("Findings and Thoughts")
st.write("In this page, we will diacuss what we did with the dataand what we \
         found so far. We will aslo discuss what we think about the data at this\
          point and what we plan to do next for this application.")
st.subheader("Raw Data")
st.write("Let's start by discussing the raw data and why we could not use it directly. \
         The raw data is a scraped dataset from 'indeed.com' that has about 12,300\
          data science job postings. The columns of the original dataset were as follows:\
         ")
raw_data = pd.read_csv("pages/originalOverview.csv")
d = pd.DataFrame({
    "Column": ["Job Title", "Location", "Job Salary","Job Description"],
    "Description": ["This column contained the job title from the posting ", 
                    "Location such as MI, California, Detroit MI ...etc",
                      "Salaries as numbers, ranges, or empty",
                      'A full description of the job inclus=ding qualification and \
                      sometimes the salary information']
})
st.table(d[['Column','Description']])
st.write("As we can see from the table above, there are many issues preventig using \
         the data as is. One of the reasons was inconsistency. A good example that shows\
          that would be the location column. Whne we look at the location, there are multiple\
          ways used to specify the location such as state name only, city and state, city, \
         state and zip code, state appreviation, and remote jobs. We needed to unify those \
         to help in the analysis. More details on how we did that are in the 'Data Preparation'\
         tab.")
st.write("One of the issues was the salary information. This feature is one of the main features\
          of the analysis in this application. However, it needd alot of work to be ready\
          to use. There were multiple problems when it came to salary information. Some salaries\
         are listed under the salary column, others are included within the job description,\
          and others are completely missing. Another issue is the formats, as some salaries \
         are listed as annual salaries, some are hourly and some eployers would list a range \
         that's contingent on experience. An extensive extraction and cleaning was neede to \
         make this data ready to use. See 'Data Preparation' tab and 'Imputation Comparison' \
         tab for more details.")
st.write("While job description has lots of useful data, it has lots of unnecessary data \
         as well. We had to parse this field to extract the needed data such as salary \
         information if available and the programming languages/qualifications required \
         for the job listing. Checkout the 'Data Preparation' Tab for more details.")
st.subheader("Cleaned Data")
st.write("We cleaned and re-organized the data to make sure that we can use it in the application. \
         There were multiple steps needed to get to the final cleaned data. Check out\
          'Data Preparation' tab for more info. We could not use the data direcly even after\
          cleaning as we had missing data. We had to impute salary information as it was missing\
          lots of cells.")
st.subheader("Imputed Data")
st.write("Trying to make a decision with missing data can be challenging. This missingess \
         we had to deal with in this dataset was the salary information. Unfortunately, \
         salary information is one of the main points of decision making in this application \
         so we had to do something about it. While some people may not be comfortable wtih \
         making decision based on synthesized data, others find totally fine if the data \
         is 'close enough' to the actual data. For that reason, we tested more than one \
         imputation method to fill in the missing data. Check out 'Imputation Comparison' \
         tab for more info.")
st.subheader("Findings")
st.write('While there\'s still much to explore about this dataset, we will be using some \
         of the figures from the application and some statistical data here to talk \
         about our finidings so far. Let\'s start with the distibution on the salary.')
st.image('Images/salary_dist.png', caption = '')
st.write('As someone may expect, locations with relatively high cost of living have\
          relatively higher salaries and the data in the plot above supports that. \
         Looking at the plot, we can see that there are salaries that are placed very low \
         in the plot .However, when you hover over them, you\'ll notice that the starting \
         salary is very low while the high range is normal. We do not know at this point \
         what exactly is going on but we plan to investigate this as see what the cause is \
         and determine whether it is an issue with the data preparationof it is in the \
         job listing itself.\n Another intresting finding is the job distribution as can be seen \
         in the figures below.')
st.image('Images/dist_all.png', caption = 'Job Counts per Location')
st.image('Images/dist_no_python.png', caption = 'Jobs Counts - Not Requiring Python')
st.image('Images/dist_no_java.png', caption = 'Jobs Counts - Not Requiring Java')
st.write('An intresting finding is coming from this plot that really shows how the \
         popularity of a language or technology plays a role in the job market. \
         An example of what we can also infer from this plot is when we hear that \
         a language or technology is\'dying\'. While some say that Java for example \
         is dying and others do not agree, the plot above supports the fact thatit is \
         actually dying at least from the data science employers\' point of view.\
         A very intresting and surprising finding can be seen from the correlation \
         heat map below.')
st.image('Images/ corr_matrix.png', caption = 'Correltaion Heat Map')
st.write('Looking at the heatmap above, it is expected to see a correlation between \
         low salary range and high salary range. However, the heatmap helps us answer \
         a very intresting question, that is: if a person is qualified in a certain \
         programming language, will it be benificial for them to invest in learning another \
         one. For example, if a person knows Python, do they need to learn SQL? based on the \
         heatmap above, we can see a correlation between these two qualifications which suggests \
         that it would be benificial in that case. Another example would be Java and Linux \
         which as the heatmap suggests has almost zero correlation which means there are extremely \
         few job listings that require both of these.')
st.write('As we mentioned above, there\'s still much to learn from this data and we plan \
         on exploring more to see what we can find.')
st.subheader("Thoughts about the Dataset and Imputation")
st.write("While the dataset we had is real data from a real job borad, we still think \
         that we can not come up with an accurate prediction model based on this data alone. \
         We think that we need to compare more data from different timelines to be able to \
         predict where the job market is headed.")
st.write("In terms of imputation, we think that there might be a better imputation approach \
         that could utilize other things such as the location and experience level \
         as that may produce a more accurate prediction of the salary information.")
st.subheader("What's Next")
st.write("For the next part of this application, we plan to investigate and implement \
         a better and more accurate way to impute the data. Another feature to be implemented \
         is allowing the user to type in the qualifications they have or intrested in \
         and do the analysis based on the user's entry. Another feature that we will try to \
         impelemnt is allowing the user to upload data (if possible) that can be used \
         in the analysis.")
st.write("One of the features that we will investigate the possibility of adding is \
         trying to compare data from different time periods to try to predict the \
         trajectory of the job market. We also plan on trying to improve the application's \
         performance as loading some of the plots is slow at this time. Last but not least, we plan on doing more EDA \
         to see what questions we can answer based on the dataset we have.")

