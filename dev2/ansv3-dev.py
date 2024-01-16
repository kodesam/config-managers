import openai
import yaml
import streamlit as st
import pandas as pd 
from github import Github, GithubException
import random
import re



title_style = (
    "color: blue;"
    "font-weight: bold;"
)
# Display the title with the defined style
st.markdown(f"<h1 style='{title_style}'>💬 🚀🚀BlueRunBook-AI🚀🚀 </h1>", unsafe_allow_html=True)
st.caption("🚀 🚀 🚀 Blue-Ansible-PlayBook Powered by OpenAI LLM")

# Place your actual OpenAI API key here
#openai.api_key = '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'

with st.sidebar:
    st.title("💬 Blue-Ansible-PlayBook 🚀🚀")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    openai.api_key = st.text_input("OpenAI API Key", type="password")

# Read Ansible modules from file
with open("/workspaces/i-Runbook-AI/dev2/ansible_modules.txt") as f:
    ansible_modules = [line.strip() for line in f]


def generate_ansible_script(module, tasks):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Write an ansible script using the {module} module to {tasks}"},
        ]
    )

    ansible_script = response['choices'][0]['message']['content']
    ansible_script = ansible_script.replace('```yaml', '')
    ansible_script = ansible_script.replace('```', '')

    return ansible_script


module = st.selectbox('Select module', ansible_modules)
tasks = st.text_area('Enter tasks here', '')
response_text = ''

if st.button('Generate Ansible Script'):
    if module and tasks:
        response_text = generate_ansible_script(module, tasks)
        if response_text:
            st.text_area("Response:", value=response_text, height=400)
    else:
        st.markdown('Please enter module and tasks')


# Generate a random number
random_number = random.randint(1, 1000)



# Prompt the user for GitHub credentials
github_token = st.sidebar.text_input("GitHub Personal Access Token", type="password")
repo_owner = st.sidebar.text_input("Repository Owner")
repo_name = st.sidebar.text_input("Repository Name")
folder_path = st.sidebar.text_input("Folder Path")
branch_name = st.sidebar.text_input("Branch Name", value="main")


st.sidebar.markdown("<p class='developer-name'>Developer : Aamir </p>", unsafe_allow_html=True)

# Update the base_filename and filename
base_filename = "code"
filename = f"{base_filename}_{random_number}.yaml"

if response_text and github_token and repo_owner and repo_name and folder_path and branch_name:
    try:
        # Create a connection to the GitHub repository
        g = Github(github_token)
        repo = g.get_repo(f"{repo_owner}/{repo_name}")

        # Check if the file already exists in the folder
        file_path = f"{repo_owner}/{repo_name}/{folder_path}/{filename}"
        file_exists = True

        try:
            repo.get_contents(file_path, ref=branch_name)
        except GithubException as e:
            if e.status == 404:
                file_exists = False
            else:
                raise

        if not file_exists:
            # Create or update the file in the repository
            commit_message = f"Create {tasks}"
            repo.create_file(file_path, commit_message, response_text, branch=branch_name)
            st.sidebar.text(f"File '{filename}' created successfully in the GitHub repository.")
            st.success('Success message')
        else:
            st.sidebar.text(f"File '{filename}' already exists in the GitHub repository. Skipping creation.")
    except AssertionError as e:
        # Handle the AssertionError
        st.error("An error occurred while creating the file. Please try again later.")
    except GithubException as e:
        # Handle the GitHub exception
        st.error("File already exists in GitHub Repository folder.")