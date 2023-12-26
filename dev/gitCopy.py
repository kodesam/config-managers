import streamlit as st
from github import Github, GithubException
from openai import OpenAI

# Create sidebar inputs
st.sidebar.header("GitHub Repository Configuration")

source_token = st.sidebar.text_input("Source Repository Access Token", type="password")
source_owner = st.sidebar.text_input("Source Repository Owner")
source_repo_name = st.sidebar.text_input("Source Repository Name")

target_token = st.sidebar.text_input("Target Repository Access Token", type="password")
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

# Execute button for executing the file copy process
execute_file_copy = st.sidebar.checkbox("Execute File Copy")

# AWS Cloud integration inputs
aws_cloud = st.sidebar.selectbox("Select Cloud", ["AWS", "Azure", "Google Cloud"])
aws_url = st.sidebar.text_input("AWS URL")
aws_user = st.sidebar.text_input("AWS User")
aws_token = st.sidebar.text_input("AWS Token")

# Execute button for executing cloud integration
execute_cloud_integration = st.sidebar.checkbox("Execute Cloud Integration")

if execute_cloud_integration:
    if aws_cloud == "AWS" and aws_url and aws_user and aws_token:
        # Perform AWS integration
        st.info("Integrating with AWS Cloud...")
        # Your code for AWS integration
        st.write(f"AWS URL: {aws_url}")
        st.write(f"AWS User: {aws_user}")
        st.write(f"AWS Token: {aws_token}")

    elif aws_cloud == "Azure":
        # Perform Azure integration
        pass

    elif aws_cloud == "Google Cloud":
        # Perform Google Cloud integration
        pass

# Check if the file copy should be executed
if execute_file_copy:
    try:
        with st.spinner("Copying file..."):
            # Create instances of the source and target repositories
            source_repo = Github(source_token).get_repo(f"{source_owner}/{source_repo_name}")
            target_repo = Github(target_token).get_repo(f"{target_owner}/{target_repo_name}")

            # Get the content of the file in the source repository
            file_content = source_repo.get_contents(file_path).decoded_content

            # Create the file in the target repository with the content from the source file
            target_repo.create_file(
                new_file_path,
                "Copying file",
                file_content,
                branch="main"
            )

        st.success(f"File '{file_path}' copied to '{new_file_path}' in the target repository successfully.")

    except Exception as e:
        st.error(f"An error occurred while copying the file: {str(e)}")