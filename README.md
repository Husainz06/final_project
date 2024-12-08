This file explains the organization of this project's files and pages.
Pages have prefixes to tell what type of user they're aimed at:
- U: Used pages.
- DS: Data scienctists.
- I: General project information.

The homepage is under the main directory and is named 'Home.py'
All other pages are under the pages sub-directory
All images are under Images sub-directory
Datasest are also under pages sub-directory
'data_cleaning_encoding.py' has the code used for data cleaning and encoding
'Visualizations.ipynb' is a notebook containing some of the visualizations created
for this application.
The 'requirements.txt' file includes the required libraries that are imported throughut the application pages and this needs to be updated whenever a new library is added.
As this application is currently uploaded on streamlit, any update on the files on the GitHub repository will be reflected immediately on https://husainz06-final-project-home-jpqcgv.streamlit.app

To setup the application on a new streamlit domain, the files must be uploaded to a GitHub repository first making sure to include the requirements file and the devcontainer folder. An account must be created for stramlit community cloud which will allow deploying the application. Checkout streamlit's documentation for more info.

