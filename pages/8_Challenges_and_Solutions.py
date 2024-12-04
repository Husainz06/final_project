import streamlit as st

# Page Title
st.title("Challenges and Solutions")

# Data Preparation Section
st.subheader("Data Preparation")

st.write("""
Working with raw job data presented significant preprocessing challenges. One specific difficulty was extracting salary information from job descriptions. The presence of URLs within some descriptions caused our extraction algorithm to mistakenly identify numbers within the URLs as salary values. 

To resolve this, we refined our regular expression to ensure that only valid salary figures were captured. Additionally, we implemented a check to validate the length of the number string, ensuring it aligned with the typical length of salary values.
""")

# Slow Bigram Processing Section
st.subheader("Slow Bigram Processing")

st.write("""
Extracting bigrams and trigrams from the job descriptions required tokenizing a large dataset, which resulted in slow processing times. Given the size of the dataset, this step became a bottleneck. 

To improve performance, we implemented a solution that involved storing preprocessed tokens and n-grams in external files. This approach prevents the need to recreate tokens and n-grams each time a user initiates a search, significantly reducing processing time during repeated queries.
""")

# Cluttered Visualizations Section
st.subheader("Cluttered Visualizations")

st.write("""
Another challenge arose when generating visualizations for user queries containing multiple search terms. In such cases, the resulting plots would often become cluttered, making it difficult for users to interpret the data. 

To address this, we developed a dynamic figure resizing feature that adjusts the plot dimensions based on the number of components (keywords) included in the search. This ensures that the visualizations remain clear and readable, regardless of the number of terms entered by the user.
""")

# Job Market Forecasting Challenge Section
st.subheader("Forecasting the Job Market")

st.write("""
A significant challenge arose when attempting to forecast the job market over the next 5+ years. The dataset of job postings we were using did not include historical data, which made it impossible to track trends or forecast future job market conditions. Additionally, we were unable to retrieve more job postings from the same website, as our scraper kept being blocked due to repeated scraping attempts.

To overcome this limitation, we hypothesized that the popularity of programming languages could serve as a reliable indicator for the growth or decline in job opportunities. We validated this hypothesis by analyzing a different dataset, which showed a strong correlation (approximately 0.96) between the popularity of programming languages and the number of job postings.

With this correlation in hand, we were able to leverage a third dataset containing historical data on the popularity of programming languages. Using this data, we were able to forecast job market trends for the coming years, providing a more accurate and data-driven approach to predicting future demand for programming-related jobs.
""")
