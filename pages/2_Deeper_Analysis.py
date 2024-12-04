import pandas as pd
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk import bigrams, trigrams
from nltk.probability import FreqDist
import seaborn as sns
import os
import streamlit as st
# Proof read the paragraphs

# Downloading necessary NLTK resources if they are not already downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Creating csv files to save tobens and n-grams to enhance the performance
BIGRAM_CSV_FILE = "keyword_bigrams.csv"
TRIGRAM_CSV_FILE = "keyword_trigrams.csv"
TOKENS_FILE = "tokens.csv"

# Reading the actual dataset
data = pd.read_csv('pages/us_jobs_data_knn_imputed_v2.csv')

# Will be called if n-grams exist for a keyword
def load_existing_ngrams(ngram_type='bigram'):
    # Check the n-gram type to determine which file to use
    if ngram_type == 'bigram' and os.path.exists(BIGRAM_CSV_FILE):
        return pd.read_csv(BIGRAM_CSV_FILE)
    elif ngram_type == 'trigram' and os.path.exists(TRIGRAM_CSV_FILE):
        return pd.read_csv(TRIGRAM_CSV_FILE)
    else:
        return pd.DataFrame(columns=["ngram", "count", "keyword"])
    
# Adding new n-grams to csv when needed
def save_ngrams_to_csv(data, ngram_type='bigram'):
    if ngram_type == 'bigram':
        data.to_csv(BIGRAM_CSV_FILE, index=False)
    elif ngram_type == 'trigram':
        data.to_csv(TRIGRAM_CSV_FILE, index=False)

# Loading tokens from tokens file if the token file exists
def load_tokens():
    if os.path.exists(TOKENS_FILE):
        return pd.read_csv(TOKENS_FILE)['tokens'].tolist()
    else:
        return None
    
# Adding tokens if new ones get generated
def save_tokens(tokens):
    tokens_df = pd.DataFrame(tokens, columns=["tokens"])
    tokens_df.to_csv(TOKENS_FILE, index=False)

# Generate tokens  - this function is used when token file does not exist
def generate_tokens(data):
    data_clean = data[data['job_summary'].notna()]
    # Combine all job summaries into one large string
    all_job_summaries = ' '.join(data_clean['job_summary'])
    # Tokenize the text
    tokens = nltk.word_tokenize(all_job_summaries)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]
    # Save the tokens in the file
    save_tokens(filtered_tokens)
    # Return the tokens to be used in the app if needed
    return filtered_tokens

# Plotting the n-grams
def plot_keyword_ngrams(data, keywords, ngram_type):
    # Load existing tokens or generate if not available
    tokens = load_tokens()
    if tokens is None:
        # If no tokens file, generate tokens and save them
        with st.spinner('Generating tokens, please wait...'):
            tokens = generate_tokens(data)

    # Choose the appropriate n-gram generator based on user input
    if ngram_type == 'Bigrams':
        ngram_function = bigrams
    elif ngram_type == 'Trigrams':
        ngram_function = trigrams

    # In case the user tries typing into the menu
    else:
        st.error("Invalid ngram type selected")
        return

    # Generate n-grams from the filtered tokens
    ngram_list = list(ngram_function(tokens))
    # Load existing n-grams from CSV
    existing_ngrams = load_existing_ngrams(ngram_type)

    # Create a list to hold the data for the plot
    plot_data = []

    # Create a color palette with a unique color for each keyword
    colors = sns.color_palette("Set2", len(keywords))

    # Save keywords that do not have any n-grams
    missing_keywords = []

    
    with st.spinner(f'Creating {ngram_type}s plot, please wait...'):
        # Loop through each keyword and filter n-grams containing the keyword
        for idx, keyword in enumerate(keywords):
            # Check if n-grams for this keyword already exist in the CSV
            keyword_ngrams = existing_ngrams[existing_ngrams['keyword'] == keyword]

            if keyword_ngrams.empty:
                keyword_ngrams = [ngram for ngram in ngram_list if keyword in ngram]
                
                # Calculate the frequency of n-grams
                ngram_freq = FreqDist(keyword_ngrams)

                # When no n-grams are found, save into missing list and move to the next iteration
                if not ngram_freq:
                    missing_keywords.append(keyword)
                    continue

                # Get the 5 most common n-grams
                most_common_ngrams = ngram_freq.most_common(5)

                # Add n-grams to the plot
                for ngram, count in most_common_ngrams:
                    plot_data.append({
                        'ngram': ' '.join(ngram),
                        'count': count,
                        'keyword': keyword,
                    })

                # Add the new n-grams to the csv file
                new_data = pd.DataFrame(plot_data[-5:])
                existing_ngrams = pd.concat([existing_ngrams, new_data], ignore_index=True)
                save_ngrams_to_csv(existing_ngrams, ngram_type)

            else:
                # Add n-grams form csv file to the plot
                plot_data.extend(keyword_ngrams.to_dict('records'))

        # If no n-grams were found for all provided keywords
        if not plot_data:
            st.write("No n-grams found with the provided keywords.")
            return

        # Making a dataframe for easier plotting
        plot_df = pd.DataFrame(plot_data)

        # testing to see if no n-grams are found
        if 'ngram' not in plot_df.columns:
            st.error("Missing 'ngram' column in plot data.")
            return

        # Dynamically update the plot's height based on the number of bars
        num_keywords = len(keywords)
        num_ngrams = len(plot_data)
        height = num_keywords + num_ngrams * 0.5

        plt.figure(figsize=(12, height))

        # Applying colors to n-grams
        for idx, keyword in enumerate(keywords):
            keyword_data = plot_df[plot_df['keyword'] == keyword]
            keyword_color = colors[idx]
            bars = plt.barh(keyword_data['ngram'], keyword_data['count'], color=keyword_color, label=keyword)
            # Adding numbers on the smaller bars 
            for bar in bars:
                if bar.get_width()  < 25:
                    plt.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                             f'{int(bar.get_width())}', va='center', ha='left', fontsize=10, color='black')

        plt.xlabel('Frequency')
        plt.ylabel(f'{ngram_type.capitalize()}')
        plt.title(f'Top 5 {ngram_type.capitalize()} for Each Keyword')
        # Place the higher numbers in every group on top
        plt.gca().invert_yaxis() 
        plt.legend(title="Keywords")

        # Show keywors in the missing list
        if missing_keywords:
            st.write(f"Keywords not found: {', '.join(missing_keywords)}\n \
                     Plotting the rest of the keywords.")
        st.pyplot(plt)

# Streamlit user interface
st.title('Keyword N-gram Analysis for Job Summaries')
#st.header('Bigrams and Trigrams')
st.write("""On this page, you can dive deeper into the job descriptions and gain more insights by exploring n-grams.
         more specifically **Bigrams** and **Trigrams**. \n\n **To get more information bout n-grams, please 
         read the next paragrpahs or scroll beyound them for analysis.**""")
st.header('N-Grams Explained')
st.write("""When we talk about bigrams and trigrams, we're referring to **pairs** and **triplets** of words that 
         often appear together in a sentence or a piece of text.

- **Bigrams** are simply **two consecutive words**. For example, in the sentence "The cat sleeps," 
         the bigrams would be "The cat" and "cat sleeps."
  
- **Trigrams** are **three consecutive words**. So, from the sentence "The cat sleeps on the mat," 
         the trigrams would be "The cat sleeps," "cat sleeps on," and "sleeps on the," and "on the mat."

These word pairs and triplets are useful because they help us understand how words tend to group 
         together in language. By analyzing them, we can discover patterns in text, which is helpful 
         for tasks like text analysis, search engines, or even making predictions about what words might 
         come next.
""")

st.subheader("How Are Bigrams and Trigrams Extracted?")

st.write("""
The process of finding these pairs and triplets of words involves looking at a body of text 
         and grouping the words that appear together. It's a bit like breaking down a sentence 
         into smaller, manageable chunks that represent how words typically fit together in a sentence.

In our app, we use a tool called **NLTK** (which is like a helper for working with language). 
         NLTK helps us automatically look through text and identify which words are grouped together 
         as bigrams or trigrams. It does this by looking at the words in order, one by one, and pulling 
         out the ones that are next to each other. This is done after removing common stop words such as
         "in","the", "for"...etc. For example, if we have the qualification phrase 
         "Experience in Python, Java, and SQL" the bigrams would be "Experience Python",  
         "Python Java", and "Java SQL". On the other hand, trigrams would be "Experience Python Java", 
         and "Python Java SQL"

By breaking up the text this way, we can uncover meaningful insights into how words are related
          to each other and make search results more relevant based on the keywords you enter.
""")
st.header("Explore N-Grams")
st.write('To further explore the data utilizing n-grams, please search for the terms below:')
# Getting user input for keywords
user_input = st.text_input("Enter keywords (space-separated). Hit 'Enter' when done!").lower()

# Dropdown menu to select between n-grams
ngram_type = st.selectbox("Select N-gram type", ['Bigrams', 'Trigrams'])

if user_input:
    # Splitting  user input into keywords
    keywords = user_input.strip().split()
    with st.spinner(f'Loading/creating {ngram_type}.... Please wait'):
        plot_keyword_ngrams(data, keywords, ngram_type)

    # maybe add more text here as an analysis part?
    st.write("")
