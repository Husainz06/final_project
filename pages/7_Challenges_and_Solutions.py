import pandas as pd
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk import bigrams, trigrams  # Import both bigrams and trigrams
from nltk.probability import FreqDist
import seaborn as sns
import os
import streamlit as st
import time  # For simulation of loading delays

# Download necessary NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Path to store the CSV files for bigrams and trigrams
BIGRAM_CSV_FILE = "keyword_bigrams.csv"
TRIGRAM_CSV_FILE = "keyword_trigrams.csv"
TOKENS_FILE = "tokens.csv"
data = pd.read_csv('pages/us_jobs_data_knn_imputed_v2.csv')

def load_existing_ngrams(ngram_type='bigram'):
    """Load existing n-grams data from CSV based on ngram_type (bigram or trigram)."""
    if ngram_type == 'bigram' and os.path.exists(BIGRAM_CSV_FILE):
        return pd.read_csv(BIGRAM_CSV_FILE)
    elif ngram_type == 'trigram' and os.path.exists(TRIGRAM_CSV_FILE):
        return pd.read_csv(TRIGRAM_CSV_FILE)
    else:
        return pd.DataFrame(columns=["ngram", "count", "keyword"])

def save_ngrams_to_csv(data, ngram_type='bigram'):
    """Save the new n-grams to the corresponding CSV file."""
    if ngram_type == 'bigram':
        data.to_csv(BIGRAM_CSV_FILE, index=False)
    elif ngram_type == 'trigram':
        data.to_csv(TRIGRAM_CSV_FILE, index=False)

def load_tokens():
    """Load tokens from CSV file if available."""
    if os.path.exists(TOKENS_FILE):
        return pd.read_csv(TOKENS_FILE)['tokens'].tolist()
    else:
        return None

def save_tokens(tokens):
    """Save tokens to a CSV file."""
    tokens_df = pd.DataFrame(tokens, columns=["tokens"])
    tokens_df.to_csv(TOKENS_FILE, index=False)

def generate_tokens(data):
    """Generate tokens from job summaries, removing stop words and non-alphabetic tokens."""
    # Ensure there are no NaN values in 'job_summary'
    data_clean = data[data['job_summary'].notna()]

    # Combine all non-NaN job summaries into one large string
    all_job_summaries = ' '.join(data_clean['job_summary'])

    # Tokenize the text (split into words)
    tokens = nltk.word_tokenize(all_job_summaries)

    # Remove stop words (common words that don't contribute to meaningful analysis)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]

    # Save the tokens for later use
    save_tokens(filtered_tokens)
    return filtered_tokens

def plot_keyword_ngrams(data, keywords, ngram_type):
    """
    Given a DataFrame `data` and a list of `keywords`, this function extracts n-grams
    involving those keywords from the 'job_summary' column and plots their frequencies.
    
    Parameters:
    - data (DataFrame): The dataset containing job descriptions.
    - keywords (list): A list of keywords to analyze in relation to other words.
    - ngram_type (str): The type of n-grams to generate ('bigram' or 'trigram').
    """
    # Load existing tokens or generate if not available
    tokens = load_tokens()

    if tokens is None:
        # If no tokens file, generate tokens and save them
        with st.spinner('Generating tokens, please wait...'):
            tokens = generate_tokens(data)

    # Choose the appropriate n-gram generator based on user input
    if ngram_type == 'bigram':
        ngram_function = bigrams  # Generate bigrams
    elif ngram_type == 'trigram':
        ngram_function = trigrams  # Generate trigrams
    else:
        st.error("Invalid ngram type selected")
        return

    # Generate n-grams from the filtered tokens
    ngram_list = list(ngram_function(tokens))

    # Load existing n-grams from CSV
    existing_ngrams = load_existing_ngrams(ngram_type)

    # Create a list to hold the data for plotting
    plot_data = []

    # Create a color palette with a unique color for each keyword
    colors = sns.color_palette("Set2", len(keywords))  # Generate distinct colors

    # Track if any keyword is missing n-grams
    missing_keywords = []

    # Use a spinner while processing n-grams
    with st.spinner(f'Creating {ngram_type}s plot, please wait...'):
        # Loop through each keyword and filter n-grams containing the keyword
        for idx, keyword in enumerate(keywords):
            # Check if n-grams for this keyword already exist in the CSV
            keyword_ngrams = existing_ngrams[existing_ngrams['keyword'] == keyword]

            if keyword_ngrams.empty:
                # Filter n-grams to only include those that contain the keyword
                keyword_ngrams = [ngram for ngram in ngram_list if keyword in ngram]
                
                # Calculate the frequency distribution of the keyword n-grams
                ngram_freq = FreqDist(keyword_ngrams)

                # If no n-grams were found with the keyword, skip to next keyword
                if not ngram_freq:
                    missing_keywords.append(keyword)
                    continue

                # Get the most common n-grams involving the keyword
                most_common_ngrams = ngram_freq.most_common(5)

                # Append the new n-grams to the plot_data list with keyword info
                for ngram, count in most_common_ngrams:
                    plot_data.append({
                        'ngram': ' '.join(ngram),  # Make sure 'ngram' column is added correctly
                        'count': count,
                        'keyword': keyword,
                    })

                # Save the new n-grams to the CSV file
                new_data = pd.DataFrame(plot_data[-5:])
                existing_ngrams = pd.concat([existing_ngrams, new_data], ignore_index=True)
                save_ngrams_to_csv(existing_ngrams, ngram_type)

            else:
                # If n-grams exist in the CSV, add them to the plot_data list
                plot_data.extend(keyword_ngrams.to_dict('records'))

        # If no n-grams were found for any keyword
        if not plot_data:
            st.write("No n-grams found with the provided keywords.")
            return

        # Convert the plot_data list into a DataFrame for easier plotting
        plot_df = pd.DataFrame(plot_data)

        # Ensure 'ngram' column is present
        if 'ngram' not in plot_df.columns:
            st.error("Missing 'ngram' column in plot data.")
            return

        # Calculate the dynamic height of the plot based on the number of keywords and n-grams
        num_keywords = len(keywords)
        num_ngrams = len(plot_data)
        height = num_keywords + num_ngrams * 0.5  # Adjust height multiplier as needed

        # Plot the combined n-grams in one plot
        plt.figure(figsize=(12, height))

        # Loop through each keyword and plot its n-grams with the corresponding color
        for idx, keyword in enumerate(keywords):
            keyword_data = plot_df[plot_df['keyword'] == keyword]
            keyword_color = colors[idx]  # Color corresponding to the keyword

            # Plot the n-grams for this keyword
            bars = plt.barh(keyword_data['ngram'], keyword_data['count'], color=keyword_color, label=keyword)

            # Annotate the bars with frequency numbers
            for bar in bars:
                if bar.get_width() > 0:
                    plt.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                             f'{int(bar.get_width())}', va='center', ha='left', fontsize=10, color='black')

        plt.xlabel('Frequency')
        plt.ylabel(f'{ngram_type.capitalize()}')
        plt.title(f'Top 5 {ngram_type.capitalize()}s for Each Keyword')
        plt.gca().invert_yaxis()  # Invert the y-axis to have the most frequent n-gram at the top
        plt.legend(title="Keywords")

        # Display message if some keywords had no n-grams
        if missing_keywords:
            st.write(f"Keywords not found: {', '.join(missing_keywords)}")

        # Display the plot
        st.pyplot(plt)

# Streamlit user interface
st.title('Keyword N-gram Analysis for Job Summaries')

# Input: User can input keywords as a space-separated string
user_input = st.text_input("Enter keywords (space-separated). Hit enter when done!")

# Ngram type selection: 'bigram' or 'trigram'
ngram_type = st.selectbox("Select N-gram type", ['bigram', 'trigram'])

if user_input:
    # Split the user input into a list of keywords
    keywords = user_input.strip().split()

    # Use a spinner while processing the plot
    with st.spinner(f'Loading/creating {ngram_type}s.... Please wait'):
        plot_keyword_ngrams(data, keywords, ngram_type)
