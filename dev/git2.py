import streamlit as st
from github import Github

# Create sidebar inputs
st.sidebar.header("GitHub Repository Configuration")

source_token = st.sidebar.text_input("Source Repository Access Token")
source_owner = st.sidebar.text_input("Source Repository Owner")
source_repo_name = st.sidebar.text_input("Source Repository Name")

target_token = st.sidebar.text_input("Target Repository Access Token")
target_owner = st.sidebar.text_input("Target Repository Owner")
target_repo_name = st.sidebar.text_input("Target Repository Name")

file_path = st.sidebar.text_input("Path to File in Source Repository")
new_file_path = st.sidebar.text_input("Path to New File in Target Repository")

# Check if all inputs are provided
if (
    not source_token
    or not source_owner
    or not source_repo_name
    or not target_token
    or not target_owner
    or not target_repo_name
    or not file_path
    or not new_file_path
):
    st.sidebar.error("Please provide all the necessary inputs.")
    st.stop()

try:
    # Create instances of the source and target repositories
    source_repo = Github(source_token).get_repo(f"{source_owner}/{source_repo_name}")
    target_repo = Github(target_token).get_repo(f"{target_owner}/{target_repo_name}")

    # Get the content of the file in the source repository
    file_content = source_repo.get_contents(file_path).content

    # Create the file in the target repository
    target_repo.create_file(new_file_path, "Copying file", file_content, branch="main")

    st.success(f"File '{file_path}' copied to '{new_file_path}' in the target repository successfully.")

except Exception as e:
    st.error(f"An error occurred while copying the file: {str(e)}")