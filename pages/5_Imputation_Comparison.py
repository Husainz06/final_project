import streamlit as st
from sklearn.impute import SimpleImputer
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.impute import KNNImputer


original = pd.read_csv('pages/cleaned_v2.csv')

st.title('Handling Missing Data - Imputation')
st.write('The dataset has missing salary information and the data is missing \
         compeletely at random (MCAR) as it is missing not because of a raltionship\
         to another feature or to certain values of the salary\
         Here, we compare the results of different imputation methods to see \
         how the dataset is affected\n In this page, we apply different\
         Data Imputation Techniques to see how the dataset is affected. First, let\'s see \
         the missing data that needs to be imputed.')

st.image("Images/missing_heat_map.png", caption="Missing Data")

st.write('As can be seen from the figure above, there\'s a lot of missing salary data \
         which is a very important feature for the purposes of this application. Imputation \
         takes care of that and fills in the missing data. However, which imputation technique \
         is better? That\'s what we will try to answer in the follwoing sections.')
st.subheader('Data Distribution')
st.write('Since we implemented more than one imputation technique, we want to know which one is better \
         for this application. Below we will compare these to see what sort of information we can get \
         and if that information can help us pick an imputation technique over another.\n')

st.image("Images/histograms.png", caption="Data Distribution Comparison")

st.write('Let\'s see what information we can get from a box plot as it will help us better see the \
         quartiles and outliers')
st.image("Images/box_plots.png", caption="Box Plots")

st.write("From the box plot above, we can clearly see a wider second and third quartiles for the mean \
         imputed data. However, there's clearly a problem here with some salaries reaching zero or even \
         below zero. This tells us that we cannot reliably rely on this imputation method for this application \
         as a negative salary is not a thing. Let\'s combine the boxes and distributions in a violin plot to paint a broader image of the imputed\
          data.")
st.image("Images/violin_box.png", caption="Violin Plots")

st.write('Looking at the violin plot, we can see that there\'s a good amount of salaries below zero \
         in the mean imputed dataset. This could be a result of using the mean and standard deviation \
         in the imputation process but we are not 100\% sure as to why that\'s happening but the hard \
         conclusion is that it is not a reliable imputation method for this applicatopm. However, \
         when we combine the information we can get from the histograms above, the box plots, and the \
         violin plots, we can clearly see that KNN imputation performed much better in this particular \
         case.')
st.subheader('Statistical Comparison')
st.write("Let's do check some basic statistics on the datasets to help us come to \
         a conclusion.")
original = pd.read_csv('pages/cleaned_v2.csv')
mean_imputed = pd.read_csv('pages/mean_imputed_v2.csv')
knn_imputed = pd.read_csv('pages/knn_imputed_v2.csv')

st.table(original.describe())
st.markdown("<h5 style='text-align: center;'>Original Data Before Imputation</h5>", unsafe_allow_html=True)

st.caption("Original Data Without Imputation")
st.table(mean_imputed.describe())
st.markdown("<h5 style='text-align: center;'>Mean Imputed Data</h5>", unsafe_allow_html=True)

st.table(knn_imputed.describe())
st.markdown("<h5 style='text-align: center;'>KNN Imputed Data</h5>", unsafe_allow_html=True)
st.write("Looking at the tables above we can first see the large amount of missing salary \
         data. This raises a good question that is 'How effective and accurate an \
         imputation method is going to be? and do we have enough data to get good \
         results?'")
st.write("Comparing the minimum and maximum salaries in the imputed datasets and \
         the original, we ca see that in all three datasets the maximums are the \
         same. However, we can see the problem in the mean imputed dataset which \
         is the negative salary values. This confirms to us that we can not reliably use \
         mean imputation here.")
st.subheader('Thoughts and Conclusion')
st.write('While KNN imputation performed better than mean imputation in this applcation, there might be \
         more to explore here. Other imputation techniques might yeild better results. There could be some \
         useful correlations that can be used to impute salaries here such as the location of the job, \
         the experience level and the required qualifications. Some questions remain unasnwered here \
         such as \'Will another imputation method be more reliable? and how to test that?\' \'Is it \
         still a vaibale solution to imput while having this much missing data?\' \'Is there a better \
         solution? or should we just use the original dataset with missingness?\' Some of these \
         qustions are subjective but we need to come up with a way to quantify the results to better \
         answer them.')
st.write("We feel that will need to do more testing using other imputation methods that more factors  and features into \
         consideration but in the meantime, we will be using the KNN imputed dataset for the rest of this \
         application and may compare it sometimes to the original un-imputed dataset. The reson for this \
         comparison is because the purpose of the application is to help you make a decision that could be \
         based on the salary and not everyone would be comfortable using synthesized data for such a decision.")
