import streamlit as st
import pandas as pd

# Proof read the paragraphs
# Update to add new parts
st.title("Findings and Thoughts")
st.write("In this page, we will discuss what we did with the data and what we \
         found so far. We will also discuss what we think about the data at this\
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
                    "Location such as MI, California, Detroit MI ...etc.",
                      "Salaries as numbers, ranges, or empty",
                      'A full description of the job including qualification and \
                      sometimes the salary information']
})
st.table(d[['Column','Description']])
st.write("As we can see from the table above, there are many issues preventing using \
         the data as is. One of the reasons was inconsistency. A good example that shows\
          that would be the location column. When we look at the location, there are multiple\
          ways used to specify the location such as state name only, city and state, city, \
         state and zip code, state abbreviation, and remote jobs. We needed to unify those \
         to help in the analysis. More details on how we did that are in the 'Data Preparation'\
         tab.")
st.write("One of the issues was the salary information. This feature is one of the main features\
          of the analysis in this application. However, it needed a lot of work to be ready\
          to use. There were multiple problems when it came to salary information. Some salaries\
         are listed under the salary column, others are included within the job description,\
          and others are completely missing. Another issue is the formats, as some salaries \
         are listed as annual salaries, some are hourly, and some employers would list a range \
         that's contingent on experience. An extensive extraction and cleaning were needed to \
         make this data ready to use. See 'Data Preparation' tab and 'Imputation Comparison' \
         tab for more details.")
st.write("While job description has lots of useful data, it has lots of unnecessary data \
         as well. We had to parse this field to extract the needed data such as salary \
         information if available and the programming languages/qualifications required \
         for the job listing. Checkout the 'Data Preparation' Tab for more details.")
st.subheader("Cleaned Data")
st.write("We cleaned and re-organized the data to make sure that we can use it in the application. \
         There were multiple steps needed to get to the final cleaned data. Check out\
          'Data Preparation' tab for more info. We could not use the data directly even after\
          cleaning as we had missing data. We had to impute salary information as it was missing\
          lots of cells.")
st.subheader("Imputed Data")
st.write("Trying to make a decision with missing data can be challenging. This missingness \
         we had to deal with in this dataset was the salary information. Unfortunately, \
         salary information is one of the main points of decision making in this application \
         so, we had to do something about it. While some people may not be comfortable with \
         making decision based on synthesized data, others find totally fine if the data \
         is 'close enough' to the actual data. For that reason, we tested more than one \
         imputation method to fill in the missing data. Check out 'Imputation Comparison' \
         tab for more info.")
st.subheader("Findings")
st.write('While there\'s still much to explore about this dataset, we will be using some \
         of the figures from the application and some statistical data here to talk \
         about our findings. For this discussion, we considered Python, Java, SQL, JavaScript, and Linux.\
          Let\'s start with the distribution on the salary.')
st.image('Images/salary_dist.png', caption = '')
st.write('As someone may expect locations with relatively high cost of living have\
          relatively higher salaries and the data in the plot above supports that. \
         Looking at the plot, we can see that there are salaries that are placed very low \
         in the plot .However, when you hover over them, you\'ll notice that the starting \
         salary is very low while the high range is normal. We do not know at this point \
         what exactly is going on, but we plan to investigate this as see what the cause is \
         and determine whether it is an issue with the data preparation of it is in the \
         job listing itself.\n Another interesting finding is the job distribution as can be seen \
         in the figures below.')
st.image('Images/dist_all.png', caption = 'Job Counts per Location')
st.image('Images/dist_no_python.png', caption = 'Jobs Counts - Not Requiring Python')
st.image('Images/sal_all.png', caption = 'Salary Distributions')
st.image('Images/sal_no_pythin.png', caption = 'Salary Distributions - Not Requiring Python')
st.write('An interesting insigts are gained from these plots that really shows how the \
         popularity of a language or technology plays a role in the job market. \
         An example of what we can also infer from this plot is when we hear that \
         a language or technology is\'dying\'. While some say that Java for example \
         is dying and others do not agree, the plot above supports the fact that it is \
         actually dying at least from the data science employers\' point of view.\
         On the other hand, we know that Python is very popular in the data science job\
         market and we can clearly see the impact of removing it from the analysis on all plots above.\
         A very interesting and surprising finding can be seen from the correlation \
         heat map below as well.')
st.image('Images/ corr_matrix.png', caption = 'Correlation Heat Map')
st.write('Looking at the heatmap above, it is expected to see a correlation between \
         low salary range and high salary range. However, the heatmap helps us answer \
         a very interesting question, that is: if a person is qualified in a certain \
         programming language, will it be beneficial for them to invest in learning another \
         one. For example, if a person knows Python, do they need to learn SQL? based on the \
         heatmap above, we can see a correlation between these two qualifications which suggests \
         that it would be beneficial in that case. Another example would be Java and Linux \
         which as the heatmap suggests has almost zero correlation which means there are extremely \
         few job listings that require both of these.')
st.write('As we mentioned above, there\'s still much to learn from this data and we plan \
         on exploring more to see what we can find.')
st.subheader("Thoughts about the Dataset and Imputation")
st.write("While the dataset we had is real data from a real job board, we still think \
         that we cannot come up with an accurate prediction model based on this data alone. \
         We think that we need to compare more data from different timelines to be able to \
         predict where the job market is headed.")
st.write("In terms of imputation, we think that there might be a better imputation approach \
         that could utilize other things such as the location and experience level \
         as that may produce a more accurate prediction of the salary information.")
st.subheader("Insights from N-Grams")
st.write("Next, let's see what information we can gainfrom analyzing n-grams")
st.subheader("Analyzing Bigrams")
st.write("""
After analyzing the top 5 bigrams for each of the searched keywords, we can gain valuable insights into how different search terms are related. For example, in the data science job market, we observe that **Python** and **SQL** frequently appear together as qualifications. Similarly, we notice a connection between **Java** and **Scala**.

One intriguing finding from the bigram analysis is the relationship between **Python** and **Java**. When examining the top bigrams for **Python**, **Java** does not appear among the top 5. However, when we search for **Java's** bigrams, we see **Python** featured prominently. 

What does this reveal? It suggests that, in the data science job market, **having Python experience does not necessarily require Java experience**, but the reverse is not true—**if you have Java experience, Python skills become a valuable complement**. 

This insight highlights how bigrams can uncover important patterns and relationships within job qualifications, offering a deeper understanding of the market trends and skill demands.

""")
st.image('Images/bigrams.png', caption = 'Bigrams for the selected keywords')
st.subheader("Can Trigrams Provide More Insights?")

st.write("Now that we've seen how bigrams can help us understand relationships between skills, \
         let's explore whether **trigrams**—sequences of three words—can offer even more detailed \
         insights. Next, we will analyze trigrams to see if they provide additional \
         value in our job market analysis.")

st.image('Images/trigrams.png', caption = 'Trigrams for the selected keywords')

st.write("""
Upon examining trigrams, we can see that they provide even deeper insights into the relationships 
         between job qualifications. For instance, we find that **R** appears in the trigrams related 
         to **Python**, which suggests a connection between these two skills. This makes sense, as 
         both **Python** and **R** are heavily used in data analysis, a key component of the data 
         science job market.

Additionally, trigrams reveal other important relationships. For example, we notice that **Git** is 
         associated with **SQL**. Since **SQL** is also frequently linked with **Python**, this suggests
          that, as a **Python developer**, having **Git** experience is highly beneficial, as it plays 
         an important role in version control and collaborative development.

These trigrams provide more granular insights into the specific skills that are often required 
         together in the job market, helping to paint a clearer picture of the most sought-after 
         skill sets in the industry.
""")


st.subheader("Predicting the Job Market's Trends")
st.write("In this section we will discuss our trajectory prediction for some of the popular programming\
         languages which in terms predicts the trajectory of data science jobs. First, let's look at \
         two examples: Pyhton and Java.")
st.image('Images/python_forecast.png', caption = 'Python\'s Trajectory')
st.image('Images/java_forecast.png', caption = 'Java\'s Trajectory')

st.write("""
As we can see from the figures above, we are utilizing three distinct models for forecasting the 
         job market trends (which are explained in greater detail on the 'Deeper Analysis' page). 
         The reason for using multiple models is that different models tend to perform better for 
         specific languages. Some models are more effective at fitting the curve of a language's 
         historical trend, making them more reliable in predicting future trajectories.

For instance, when analyzing **Java**, the **logistic model** appears to provide the best fit and 
         prediction of its future trajectory. This suggests that the popularity of Java follows a 
         pattern where growth initially accelerates and then levels off over time, which is 
         characteristic of the logistic growth curve.

On the other hand, when examining **Python**, both the **polynomial** and **exponential models** 
         seem to fit the curve quite well. However, the **logistic model** also provides a good fit 
         for Python’s trend. This creates some uncertainty in predicting Python’s future trajectory, 
         as all three models appear to be valid options. In this case, we lean towards the **logistic 
         model** as the most appropriate fit for Python, though others may find that the **polynomial 
         model** provides a more intuitive understanding of Python’s growth.

To resolve this uncertainty and improve the accuracy of predictions, it would be ideal to incorporate 
         additional variables that could influence the trajectory of these programming languages. 
         Unfortunately, we currently lack access to such data, but integrating factors such as market 
         demand, technological advances, or industry-specific usage could provide a more complete picture 
         of the future job market trends.
""")
st.header("Next Steps for Enhancing the Application")

st.write("""
As we continue to develop and refine this application, several key areas for improvement and future exploration have emerged.

**1. Explore Additional Imputation Techniques:**  
We plan to experiment with different imputation techniques to assess whether we can achieve more accurate and reliable results. By experimenting with various methods, we aim to further enhance the quality of our data and improve the overall performance of the application.

**2. Expand Job Postings Dataset for Better Forecasting:**  
Increasing the volume of job listings is crucial for improving the accuracy of our forecasting. While the current job postings data has provided valuable insights, expanding the dataset will allow us to incorporate a broader range of variables, leading to more robust and precise predictions. We will focus on gathering more job postings and explore the possibility of integrating data from multiple sources. This approach will help us offer more comprehensive insights by incorporating data from various platforms.

These next steps will play a pivotal role in continuously improving the application's capabilities, ensuring it remains a valuable tool for forecasting and analyzing the job market.
""")

