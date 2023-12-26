import streamlit as st
from github import Github, GithubException

# Create sidebar inputs
st.sidebar.header("GitHub Repository Configuration")

source_token = st.sidebar.text_input("Source Repository Access Token", type="password")
source_owner = st.sidebar.text_input("Source Repository Owner")
source_repo_name = st.sidebar.text_input("Source Repository Name")

target_token = st.sidebar.text_input("Target Repository Access Token", type="password")
target_owner = st.sidebar.text_input("Target Repository Owner")
target_repo_name = st.sidebar.text_input("Target Repository Name")

# Check if all inputs are provided
if (
    not source_token
    or not source_owner
    or not source_repo_name
    or not target_token
    or not target_owner
    or not target_repo_name
):
    st.sidebar.error("Please provide all the necessary inputs.")
    st.stop()

# Function to recursively fetch subfolders in a directory
def get_folders(repo, path):
    contents = repo.get_contents(path)
    folders = []
    for content in contents:
        if content.type == "dir":
            folders.append(content.path)
            folders.extend(get_folders(repo, content.path))
    return folders

# Fetch the list of folders in the source repository
try:
    source_repo = Github(source_token).get_repo(f"{source_owner}/{source_repo_name}")
    source_folders = get_folders(source_repo, "")

    # Select the top-level folder from the source repository
    selected_folder = st.selectbox("Select Folder", source_folders)

    # Fetch and display subfolders in a recursive manner
    all_folders = get_folders(source_repo, selected_folder)
    selected_folder = st.selectbox("Select Subfolder", all_folders)

    # Get the list of files in the selected subfolder
    source_files = [
        content.name
        for content in source_repo.get_contents(selected_folder)
        if content.type == "file"
    ]

    st.subheader(f"Files in the '{selected_folder}' folder:")
    st.write(source_files)

    # Select the file to copy
    selected_file = st.selectbox("Select File", source_files)

    # Fetch the list of folders in the target repository
    target_repo = Github(target_token).get_repo(f"{target_owner}/{target_repo_name}")
    target_dirs = [content.name for content in target_repo.get_contents("") if content.type == "dir"]

    # Select the target folder in the target repository
    target_folder = st.selectbox("Select Target Folder", target_dirs)

    # Execute button
    execute = st.button("Copy File to Target Repository")

    if execute:
        try:
            with st.spinner("Copying file..."):
                # Create instances of the source and target repositories
                source_repo = Github(source_token).get_repo(f"{source_owner}/{source_repo_name}")
                target_repo = Github(target_token).get_repo(f"{target_owner}/{target_repo_name}")

                # Get the content of the file in the source repository
                file_content = source_repo.get_contents(f"{selected_folder}/{selected_file}").decoded_content

                # Create the file in the target repository with the content from the source file
                target_repo.create_file(
                    f"{target_folder}/{selected_file}",
                    "Copying file",
                    file_content,
                    branch="main"
                )

            st.success(f"File '{selected_file}' copied to the '{target_folder}' folder in the target repository successfully.")

        except GithubException as e:
            st.error(f"An error occurred while copying the file: {str(e)}")

except Exception as e:
    st.error(f"An error occurred while fetching the list of folders from the source repository: {str(e)}")
    st.stop()