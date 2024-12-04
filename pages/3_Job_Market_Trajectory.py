import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import curve_fit
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
# Proof read the paragraphs
# Correlation heatmap shows a white background on black theme  --  need to fix this
# Loading datasets
df = pd.read_csv('pages/Popularity of Programming Languages from 2004 to 2024.csv')
languages_gh_wiki = pd.read_csv('pages/languages_gitbub_wikipedia.csv')

# Fixing date formatting
df['Date'] = pd.to_datetime(df['Date'], format='%B %Y')

# defining a start date for curve_fit
start_date = pd.to_datetime("July 2004", format='%B %Y')
df['Month_Index'] = (df['Date'].dt.year - start_date.year) * 12 + (df['Date'].dt.month - start_date.month)

# Defineing fitting models
def polynomial_model(x, a, b, c):
    return a * x**2 + b * x + c

def exp_model(x, a, b, c):
    return a * np.exp(b * x) + c

def logistic_model(x, L, K, x0):
    return L / (1 + np.exp(-K * (x - x0)))

# Pulling the languages for the dropdown menu
languages = df.columns.tolist()
# Removing the Date column
languages.pop(0)  

st.title("Forecasting")

filtered_languages_gh_wiki = languages_gh_wiki[languages_gh_wiki['title'].isin(languages)]
# Selecting the columns for the correlation matrix
selected_columns = ['appeared', 'number_of_users', 'number_of_jobs', 'wikipedia_backlinks_count', 'github_language_repos',
                    "book_count", 'wikipedia_daily_page_views']
corr_matrix = filtered_languages_gh_wiki[selected_columns].corr()

st.subheader("Exploring Correlation")
st.write("Since we do not have enough job posting data to allow predicting the job market in the \
         future, we need to find a correlation between the number of available jobs and other features \
         we can use to forecast the trajectory. Let's first explore the correlation heatmap below to see \
         what features we can use.")


plt.title("Correlation Heatmap")
st.write("We can see from the heatmap above that there are many features that strongly correlate with the\
          number of available jobs such as the number of GitHub repositories, the number of a language's \
         Wikipedia page visits, the number of backlinks, the number of available books, and the number of users. \
         This tells us that in general the languages popularity strongly influences the number of available jobs.")
# Correlation heatmap

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', linewidths=0.5, cmap='viridis', ax=ax)
st.pyplot(fig)

st.subheader("Forecasting the Job Market")
st.write("As we can see from the heatmap above, there's a strong correlation between a language's popularity and the number of available jobs. \
         We have a dataset that shows contains programming languages' popularity between 2004 and 2024.\
          Therefore, we can use that to forecast programming languages' trajectory which will help us understand \
         where the job market might be headed. Use the interactive plot below to check out the \
         trajectories of some of the most popular programming languages based on Google programming language\
         tutorial searches.")


# Dropdown menu to select a language
language = st.selectbox("Select a programming language", options=languages, index=languages.index('Python'))

# User input for the number of years of forecasting
forecast_years = st.number_input(
    "Enter the number of years for forecasting", 
    min_value=1, 
    max_value=100,
    # Starting with 10 years as default value 
    value=10,
    step=1
)

def create_plot(language, forecast_years):
    x_data = df['Month_Index']
    y_data = df[language]
    with st.spinner('Fitting models and creating plot....'):
        # Creating fits
        params_poly, _ = curve_fit(polynomial_model, x_data, y_data, maxfev=100000)
        params_exp, _ = curve_fit(exp_model, x_data, y_data, p0=[max(y_data), 0.1, min(y_data)], maxfev=100000)
        p0_logistic = [max(y_data), 0.1, np.median(x_data)]
        bounds_logistic = ([0, -np.inf, 0], [np.inf, np.inf, np.inf])
        params_logistic, _ = curve_fit(logistic_model, x_data, y_data, p0=p0_logistic, bounds=bounds_logistic, maxfev=100000)

        # Generating predictions using curve_fit() parameters
        y_poly = polynomial_model(x_data, *params_poly)
        y_exp = exp_model(x_data, *params_exp)
        y_log = logistic_model(x_data, *params_logistic)

        # Forecasting for the user-specified number of years x 12 to convert to months
        # since the original curve is based on months
        future_months = np.arange(x_data.max() + 1, x_data.max() + 1 + (forecast_years * 12))
        future_poly = polynomial_model(future_months, *params_poly)
        future_exp = exp_model(future_months, *params_exp)
        future_log = logistic_model(future_months, *params_logistic)

        # Making sure values do not go below zero
        future_poly = np.clip(future_poly, 0, None)
        future_exp = np.clip(future_exp, 0, None)
        future_log = np.clip(future_log, 0, None)

    # Creating interactive plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers', name=f'{language} Data', marker=dict(color='blue')))

    # Fit values
    fig.add_trace(go.Scatter(x=x_data, y=y_poly, mode='lines', name='Polynomial Fit', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=x_data, y=y_exp, mode='lines', name='Exponential Fit', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=x_data, y=y_log, mode='lines', name='Logistic Fit', line=dict(color='purple')))

    # Forecast values
    fig.add_trace(go.Scatter(x=future_months, y=future_poly, mode='lines', name=f'Polynomial {forecast_years}-Year Forecast', line=dict(dash='dash', color='red')))
    fig.add_trace(go.Scatter(x=future_months, y=future_exp, mode='lines', name=f'Exponential {forecast_years}-Year Forecast', line=dict(dash='dash', color='green')))
    fig.add_trace(go.Scatter(x=future_months, y=future_log, mode='lines', name=f'Logistic {forecast_years}-Year Forecast', line=dict(dash='dash', color='purple')))

    # Updating to update the language name and the legend
    fig.update_layout(
        title=f'{language} Popularity (Polynomial, Exponential, Logistic Fits & {forecast_years}-Year Forecasting)',
        xaxis_title="Year",
        yaxis_title=f"Popularity ({language})",
        xaxis=dict(
            tickmode='array',
            tickvals=np.arange(x_data.min(), x_data.max() + (forecast_years * 12), 12),  # Every 12 months is a year
            ticktext=[str(start_date.year + (i // 12)) for i in np.arange(x_data.min(), x_data.max() + (forecast_years * 12), 12)]  # Convert months to years
        ),
        # dynamically increase width   --  need to fix this part
        width=1500+ forecast_years*10,  
        height=600,  
    )

    return fig



fig = create_plot(language, forecast_years)
st.plotly_chart(fig)
st.write("As can be seen from the above trajectory plot, there are three prediction models, \
         a polynomial model, an exponential model, and a logistic model. The reason for \
         keeping all three models to show the trajectory is that for some languages, different \
         models seem to fit the data better. The user will need to make an informed decision based \
         on the language and which model fits its trajectory the best.")