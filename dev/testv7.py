import streamlit as st
from github import Github, GithubException
from openai import OpenAI
import streamlit as st

# Get available models
available_models = ['gpt-3.5-turbo-16k-0613','gpt-3.5-turbo-16k-1106','gpt-3.5-turbo', 'gpt-3.5', 'gpt-3.0']

title_style = (
    "color: blue;"
    "font-weight: bold;"
)

# Display the title with the defined style
st.markdown(f"<h1 style='{title_style}'>💬 BlueRunBook-AI</h1>", unsafe_allow_html=True)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    models = st.multiselect("Select Models", available_models, default=available_models)
    instruction = "code in ansible Playbook"
    st.title("💬 BlueRunBook-AI")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    st.sidebar.markdown("<p class='developer-name'>Developer: Syed Aamir</p>", unsafe_allow_html=True)

    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.caption("🚀 Blue-runBook for ansible code generation powered by OpenAI LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can assist you on ansible code ?"}]

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

# Prompt the user for GitHub credentials
source_token = st.sidebar.text_input("Source Repository Access Token", type="password")
source_owner = st.sidebar.text_input("Source Repository Owner")
source_repo_name = st.sidebar.text_input("Source Repository Name")
source_folder = st.sidebar.text_input("Source Folder Path")

target_token = st.sidebar.text_input("Target Repository Access Token", type="password")
target_owner = st.sidebar.text_input("Target Repository Owner")
target_repo_name = st.sidebar.text_input("Target Repository Name")
target_folder = st.sidebar.text_input("Target Folder Path")

base_filename = prompt

try:
    # Create instances of the source and target repositories
    source_repo = Github(source_token).get_repo(f"{source_owner}/{source_repo_name}")
    target_repo = Github(target_token).get_repo(f"{target_owner}/{target_repo_name}")

    # Get the content of the file in the source repository
    file_content = source_repo.get_contents(f"{source_folder}/{base_filename}.yaml").decoded_content

    # Create the file in the target repository with the content from the source file
    target_repo.create_file(
        f"{target_folder}/{base_filename}.yaml",
        "Copying file",
        file_content,
        branch="main"
    )

    st.success(f"File '{base_filename}.yaml' copied to '{target_folder}' in the target repository successfully.")

except GithubException as e:
    st.error(f"An error occurred while copying the file: {str(e)}")

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")