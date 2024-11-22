import pandas as pd
import regex as re
import numpy as np

# functions
# Read locations and convert to state codes
def extract_state_codes(locations):
    # Dictionary of state names and their abbreviations
    state_abbreviations = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
        "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
        "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
        "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
        "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
        "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
        "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
        "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
        "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
        "Wisconsin": "WI", "Wyoming": "WY"
    }
    
    state_codes = []  # Use a list to preserve order
    for s in locations:
        first = False
        second = False
        us = False
        for k in state_abbreviations.keys():
            if k in s:
                state_codes.append((state_abbreviations.get(k)))
                first = True
                break
        if not first:
            for v in state_abbreviations.values():
                if v in s:
                    state_codes.append(v)
                    second = True
                    break
        if not first and not second:
            state_codes.append('US')

    return state_codes

# Read salary information from salary column and convert to high and low lists
def get_salaries(sals):
    low_salaries = []
    high_salaries = []

    for range_str in sals:
        if len(str(range_str))>0:
            numbers = re.findall(r'[\$]?([\d,]+)', str(range_str))
          #  print(f"Processing: {range_str}, found numbers: {numbers}")

            if len(numbers) == 2:
                try:
                    low_salary = int(numbers[0].replace(',', ''))
                    high_salary = int(numbers[1].replace(',', ''))

                    if low_salary < 1000:
                        low_salary *= 8 * 5 * 52
                    low_salaries.append(low_salary)
                    
                    if high_salary < 1000:
                        high_salary *= 8 * 5 * 52
                    high_salaries.append(high_salary)
                    
                except ValueError as e:
                    print(f"ValueError: {e} for entry: {range_str}")
                    low_salaries.append(np.nan)
                    high_salaries.append(np.nan)

            elif len(numbers) == 1:
                try:
                    low_salary = int(numbers[0].replace(',', ''))
                    low_salaries.append(low_salary)
                    high_salaries.append(np.nan)
                except ValueError as e:
                    print(f"ValueError: {e}")
                    low_salaries.append(np.nan)
                    high_salaries.append(np.nan)
            else:
                low_salaries.append(np.nan)
                high_salaries.append(np.nan)               

        else:
            low_salaries.append(np.nan)
            high_salaries.append(np.nan)

    return low_salaries, high_salaries
    
# Read salaries from description column and convert to high and low arrays

def get_salaries_description(descriptions):
    low_salaries = []
    high_salaries = []
    
    # Define a regex pattern for matching salary information
    salary_pattern = re.compile(r'\$?([\d,]+)(?:\s*-\s*\$?([\d,]+))')

    for description in descriptions:
        #if the job has no description or is not a string, add np.nan
        if pd.isna(description) or not isinstance(description, str):
            low_salaries.append(np.nan)  
            high_salaries.append(np.nan)
            # ignore the rest and move to the next iteration
            continue 
        # compare the job description with the defined regex
        if salary_pattern.search(description):
            # before the dash
            low_salary_str = salary_pattern.search(description).group(1)
            # after the dash
            high_salary_str = salary_pattern.search(description).group(2)

            try:
                # Convert low salary to int
                low_salary = int(low_salary_str.replace(',', '').strip())
                # Convert to annual if needed
                if low_salary < 1000:
                        low_salary *= 8 * 5 * 52
                low_salaries.append(low_salary)
                
                # Check if the high salary information is available, convert it to int
                if high_salary_str:
                    high_salary = int(high_salary_str.replace(',', '').strip())
                    # Convert to annual if needed
                    if high_salary < 1000:
                        high_salary *= 8 * 5 * 52
                    high_salaries.append(high_salary)
                # append np.nan if no high salary information is available
                else:
                    high_salaries.append(np.nan)
            # handle exceptions by adding np.nan if everything else failed   
            except ValueError:
                low_salaries.append(np.nan)  
                high_salaries.append(np.nan)
        # if no description found or not a string, add np.nan
        else:
            low_salaries.append(np.nan)
            high_salaries.append(np.nan)

    return low_salaries, high_salaries


# Merge salaries from both sources

def merge_salaries(from_salaries , from_descriptions):
    result = []
    for i in range(len(from_salaries)):
        if not np.isnan(from_salaries[i]):
            result.append(from_salaries[i])
            continue
        result.append(from_descriptions[i])
    return result

# Parse the description to extract the languages/qualifications and encode them
def parse_languages(job_descriptions, languages_list):
    row = 0
    result = [[0 for _ in range(len(languages_list))] for _ in range(len(job_descriptions))]
    for i in range(len(job_descriptions)):
        
        for j in range(len(languages_list)):
            if str(languages_list[j]).lower() in str(job_descriptions[i]).lower():
                result[i][j] = 1
    return result
# convert a column into a list of strings
# needed for some functions
def col_to_str_list(col):
    l = []
    for e in col:
        l.append(str(e))
    return l 



# Create a cleaned dataset

# read dataset
data = pd.read_csv('US_data_science_jobs_2023-6-19_0.csv')
#print(data.info())
#data

# Extract state codes into location list ------ need to check why it is adding more data
location = extract_state_codes(col_to_str_list(data['job_location']))

# Extract salary information from salaries column into hi, low lists
low , hi = get_salaries(data['job_salary'])

# Extract salary information from job descriptions into hi2, low2 lists

low2 , hi2 = get_salaries_description(data['job_summary']) 

# Merge salary lists

low_range = merge_salaries(low , low2)
high_range = merge_salaries(hi , hi2)

# Define a list of languages/qualifications
# Get it from streamlit interfacce later
lang_qual = ['Python', 'Java', 'C++','SQL','Javascript','linux']
qualifications = parse_languages(data['job_summary'], lang_qual)

#Create 2d list for the dataframe
#cols_list = [col_to_str_list(data['job_title']), location, low_range, high_range]#+ lang_qual


# create column initial dataframe
generated = {
    'Job Title': col_to_str_list(data['job_title']),
    'Location': location,
    'Salary From': low_range,
    'Salary To': high_range
    
}
cleaned_data = pd.DataFrame(generated)
# Add the encoded columns
#qualifications = [[5.5, 6.0, 5.7],[1,1,1]]  # List of heights
flipped_matrix = [list(row) for row in zip(*qualifications)]
cols= ['t1','t2']
for i in range(len(flipped_matrix)):
    cleaned_data[lang_qual[i]] = flipped_matrix[i]

cleaned_data