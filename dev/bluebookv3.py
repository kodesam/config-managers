import streamlit as st
from github import Github, GithubException
from openai import OpenAI
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
    module = ["ansible Playbook yaml file", "yaml script", "python script", "shell script", "docker file",
              "kubernetes yaml file", "juypter notebook"]

    instruction_1 = st.selectbox("Select Module", module)
    instruction_2 = st.text_area("Additional Instruction", key="additional_instruction", height=200)
    temperature = st.slider("Temperature", 0.1, 1.0, 0.8, step=0.1)
    max_tokens = st.number_input("Max Tokens", min_value=1, max_value=2048, value=100)
    top_p = st.slider("Top P", 0.1, 1.0, 0.5, step=0.1)

st.caption("🚀 🚀 🚀 Blue-runBook for code generation powered by OpenAI LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you in generating code?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Connect to OpenAI
    client = OpenAI(api_key=openai_api_key)
    
    # Create a conversation with assistant messages
    messages = [
        {"role": "system", "content": "You are a user"},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "How can I assist you on generating code?"}
    ]
    
    while True:
        # Include the instruction in the conversation
        messages.append({"role": "user", "content": instruction_1})
        messages.append({"role": "user", "content": instruction_2})

        # Include the messages in the API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,   # User-defined temperature
            max_tokens=max_tokens,     # User-defined max_tokens
            top_p=top_p                # User-defined top_p
        )

        # Extract the assistant's response
        msg = response.choices[0].message.content
        messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

        if st.button("Add more instructions"):
            continue
        else:
            break

# Generate a random number
random_number = random.randint(1, 1000)

with st.sidebar:
    # Prompt the user for GitHub credentials
    github_token = st.text_input("GitHub Personal Access Token", type="password")
    repo_owner = st.text_input("Repository Owner")
    repo_name = st.text_input("Repository Name")
    folder_path = st.text_input("Folder Path")
    branch_name = st.text_input("Branch Name", value="main")

st.sidebar.markdown("<p class='developer-name'>Developer: Syed Aamir</p>", unsafe_allow_html=True)

# Update the base_filename and filename
base_filename = "code"
filename = f"{base_filename}_{random_number}.yaml"

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
        content = msg
        commit_message = f"Create {prompt}"
        repo.create_file(file_path, commit_message, content, branch=branch_name)
        st.info(f"File '{filename}' created successfully in the GitHub repository.")
    else:
        st.warning(f"File '{filename}' already exists in the GitHub repository. Skipping creation.")
except AssertionError as e:
    # Handle the AssertionError
    st.error("An error occurred while creating the file. Please try again later.")
except GithubException as e:
    # Handle the GitHub exception
    st.error("File already exists in the GitHub Repository folder.")