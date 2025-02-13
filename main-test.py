import streamlit as st
from github import Github, GithubException
import openai
import random
import re

filtered_prompt = None

def filter_sensitive_content(prompt):
    # Existing filtering logic remains the same
    ip_address_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    masked_prompt = re.sub(ip_address_pattern, 'IP ADDRESS="XXX.XXX.XXX.XXX"', prompt)
    
    if masked_prompt != prompt:
        return masked_prompt
    
    sensitive_keywords = ["token", "password", "confidential"]
    additional_instruction_lower = prompt.lower()
    
    for keyword in sensitive_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in additional_instruction_lower:
            return None
    
    return prompt

available_models = ['gpt-4','gpt-4-1106-preview', 'gpt-3.5-turbo-16k-0613', 
                   'gpt-3.5-turbo-16k-1106', 'gpt-3.5-turbo', 'gpt-3.5', 'gpt-3.0']

title_style = "color: #001C7B; font-weight: bold;"
st.markdown(f"<h1 style='{title_style}'>💬 🚀🚀 Config-Manager 🚀🚀 </h1>", unsafe_allow_html=True)

with st.sidebar:
    st.title("💬 Config-Manager 🚀🚀")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    selected_model = st.selectbox("Select Model", available_models, index=2)
    
    module = [
        "ansible Playbook jinja2 template",
        "ansible Playbook yaml file",  
        "yaml script", 
        "python script", 
        "shell script", 
        "docker file", 
        "kubernetes yaml file", 
        "juypter notebook",
        "Windows PowerShell",
        "terraform script",
        "error correction",
    ]
    
    instruction_1 = st.selectbox("Select Module", module)
    github_token = st.text_input("GitHub Personal Access Token", type="password")
    repo_owner = st.text_input("Repository Owner")
    repo_name = st.text_input("Repository Name")
    folder_path = st.text_input("Folder Path")
    branch_name = st.text_input("Branch Name", value="main")

st.caption("🚀 🚀 🚀 Config-Manager powered by OpenAI LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can assist you on Script Generation ?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def handle_error_correction(prompt):
    return (
        "Analyze the following code for errors. Identify any syntax, logical, or security issues. "
        "Provide:\n1. A bullet-point list of found issues\n2. The corrected code\n3. A brief explanation of the fixes\n\n"
        f"Code to analyze:\n{prompt}"
    )

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    filtered_prompt = filter_sensitive_content(prompt)
    
    if not filtered_prompt:
        st.warning("The prompt contains sensitive content. Please remove any sensitive information and try again.")
        st.stop()

    # Handle module-specific prompts
    if instruction_1 == "error correction":
        filtered_prompt = handle_error_correction(filtered_prompt)
    else:
        filtered_prompt = f"{instruction_1}: {filtered_prompt}"

    client = openai.ChatCompletion(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": filtered_prompt})
    st.chat_message("user").write(filtered_prompt)

    try:
        response = client.create(
            model=selected_model,
            messages=st.session_state.messages,
            temperature=0.2 if instruction_1 == "error correction" else 0.7,
        )
        msg = response.choices[0].message.content
    except openai.error.OpenAIError as e:
        msg = f"Error: {str(e)}"
        st.error(msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

# GitHub integration remains the same
random_number = random.randint(1, 1000)
base_filename = "code"
file_ext = ".py" if "python" in instruction_1.lower() else ".yaml"
filename = f"{base_filename}_{random_number}{file_ext}"

try:
    if github_token and repo_owner and repo_name:
        g = Github(github_token)
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        file_path = f"{folder_path}/{filename}" if folder_path else filename

        try:
            repo.get_contents(file_path, ref=branch_name)
            st.warning(f"File '{filename}' already exists in the repository.")
        except GithubException:
            content = msg
            commit_message = f"Add {instruction_1} correction" if instruction_1 == "error correction" else f"Add {instruction_1}"
            repo.create_file(file_path, commit_message, content, branch=branch_name)
            st.success(f"File '{filename}' created successfully in GitHub repository!")
except Exception as e:
    st.error(f"GitHub Error: {str(e)}")
