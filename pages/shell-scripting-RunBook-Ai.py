


import streamlit as st
from github import Github, GithubException

# ...

try:
    # Your existing code here
    
    # Specify the folder path in the repository
    folder_path = "folder/path"
    filename = f"{folder_path}/{base_filename}.yaml"

    # Create a connection to the GitHub repository
    g = Github(github_token)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    
    # Check if the file already exists in the folder
    file_path = f"{repo_owner}/{repo_name}/{filename}"
    file_exists = True
    try:
        repo.get_contents(file_path)
    except GithubException as e:
        if e.status == 404:
            file_exists = False
        else:
            raise

    if not file_exists:
        # Create or update the file in the repository
        content = msg
        commit_message = f"Create {filename}"
        repo.create_file(filename, commit_message, content)
        print(f"File '{filename}' created successfully in the GitHub repository.")
    else:
        print(f"File '{filename}' already exists in the GitHub repository. Skipping creation.")
        
except AssertionError as e:
    # Handle the AssertionError
    st.error("An error occurred while creating the file. Please try again later.")
except GithubException as e:
    # Handle the GitHub exception
    st.error("An error occurred while interacting with GitHub. Please check your GitHub credentials or try again later.")
except NameError as e:
    # Handle the NameError
    st.error("An error occurred with a variable name. Please check your code and try again.")
except Exception as e:
    # Handle other exceptions
    st.error("An unexpected error occurred. Please try again later.")
