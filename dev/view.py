import requests
import streamlit as st

# Input the GitHub repository details
repo_owner = st.text_input("Repository Owner")
repo_name = st.text_input("Repository Name")
file_path = st.text_input("File Path (relative file path within the repository)")

if st.button("View File"):
    # Make a request to the GitHub API to get the raw content of the file
    url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{file_path}"
    response = requests.get(url)
    if response.status_code == 200:
        # Display the file content
        file_content = response.text
        st.code(file_content, language="text")
    else:
        st.error("Failed to retrieve the file. Please ensure the repository and file path are correct.")
