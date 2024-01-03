import streamlit as st
from github import Github, GithubException
from openai import OpenAI
import streamlit as st
import random

# Get available models
available_models = ['gpt-3.5-turbo-16k-0613','gpt-3.5-turbo-16k-1106','gpt-3.5-turbo', 'gpt-3.5', 'gpt-3.0']

title_style = (
    "color: blue;"
    "font-weight: bold;"
)

# Display the title with the defined style
st.markdown(f"<h1 style='{title_style}'>💬 🚀🚀BlueRunBook-AI🚀🚀 </h1>", unsafe_allow_html=True)

with st.sidebar:
    st.title("💬 BlueRunBook-AI 🚀🚀")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    models = st.multiselect("Select Models", available_models, default=available_models)
    instructions = ["docker file,"ansible Playbook yaml file ", "yaml script", "python script", "shell script","kubernetes yaml file"]
    instruction_1 = st.selectbox("Select Instruction", instructions)
    instruction_2 = st.text_area("Additional Instruction", key="additional_instruction", height=200)
    #st.title("💬 BlueRunBook-AI")
    

    # st.sidebar.markdown("<p class='developer-name'>Developer: Syed Aamir</p>", unsafe_allow_html=True)

    # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
 
    

st.caption("🚀 🚀 🚀 Blue-runBook for code generation powered by OpenAI LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can assist you on generating code ?"}]

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
    st.session_state.messages.append({"role": "assistant", "content": instruction_1})
    st.session_state.messages.append({"role": "assistant", "content": instruction_2})

    # Include the instruction in the API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
    )

    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

# Generate a random number
random_number = random.randint(1, 1000)

# Prompt the user for GitHub credentials
#github_token = st.sidebar.text_input("GitHub Personal Access Token", type="password")
#repo_owner = st.sidebar.text_input("Repository Owner")
#repo_name = st.sidebar.text_input("Repository Name")
#folder_path = st.sidebar.text_input("Folder Path")

# Assuming you have a GitHub personal access token
github_token = "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"
repo_owner = "kodesam"
repo_name = "collection-i-runbooks"
folder_path= "code"


#st.sidebar.title("💬 BlueRunBook-AI")
#"[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
 
st.sidebar.markdown("<p class='developer-name'>Developer: Syedff Aamir</p>", unsafe_allow_html=True)

# Update the base_filename and filename
base_filename = "code"
filename = f"{base_filename}_{random_number}.yaml"

try:
    # Your existing code here

    # Create a connection to the GitHub repository
    g = Github(github_token)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")

    # Check if the file already exists in the folder
     #file_path = f"{repo_owner}/{repo_name}/{folder_path}/{filename}"
     file_path = f"{{folder_path}/{filename}"
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
        commit_message = f"Create {prompt}"
        repo.create_file(file_path, commit_message, content)
        print(f"File '{filename}' created successfully in the GitHub repository.")
    else:
        print(f"File '{filename}' already exists in the GitHub repository. Skipping creation.")
except AssertionError as e:
    # Handle the AssertionError
    st.error("An error occurred while creating the file. Please try again later.")
except GithubException as e:
    # Handle the GitHub exception
    st.error("File already exists in GitHub Repository folder.")
