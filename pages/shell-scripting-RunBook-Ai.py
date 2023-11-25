


import streamlit as st
from github import Github, GithubException
from openai import OpenAI
import streamlit as st

# Get available models
available_models = ['gpt-3.5-turbo', 'gpt-3.5', 'gpt-3.0']

title_style = (
    "color: blue;"
    "font-weight: bold;"
)

# Display the title with the defined style
st.markdown(f"<h1 style='{title_style}'>💬 iRunBook-AI</h1>", unsafe_allow_html=True)

with st.sidebar:


    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    models = st.multiselect("Select Models", available_models, default=available_models)
    instruction = "code in linux shell scripting"
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 iRunBook-AI")

st.caption("🚀 X-runBook for ansible code generation powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can assist you on linux scripting ?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    
    
    # Include the instruction in the conversation
    st.session_state.messages.append({"role": "assistant", "content": instruction})
    
    # Include the instruction in the API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
    )
    
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

# Assuming you have a GitHub personal access token
    github_token = "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"
    repo_owner = "kodesam"
    repo_name = "collection-i-runbooks"
    base_filename = prompt

try:
    # Your existing code here
    
    # Specify the folder path in the repository
    folder_path = "Shell"
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
