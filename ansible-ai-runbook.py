from github import Github
from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    instruction = "code in ansible Playbook"
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 iRunBook-AI")

st.caption("🚀 X-runBook for ansible code generation powered by OpenAI LLM")
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

# Assuming you have a GitHub personal access token
github_token = "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"
repo_owner = "kodesam"
repo_name = "collection-i-runbooks"
base_filename = prompt

# Create a connection to the GitHub repository
g = Github(github_token)
repo = g.get_repo(f"{repo_owner}/{repo_name}")
# Get the list of all existing files
existing_files = [file.name for file in repo.get_contents("")]

# Generate a new file name based on the number of existing files
# file_number = len(existing_files)
filename = f"{base_filename}.yaml"

# Create the file in the repository
content = "   "
content = msg
commit_message = f"Create {filename}"

# Create or update the file in the repository
#content = msg
#commit_message = "Update output file"

repo.create_file(filename, commit_message, content)

print(f"File '{filename}' created successfully in the GitHub repository.")

#try:
    # Check if the file already exists
  #  existing_file = repo.get_contents(filename)
   # repo.update_file(existing_file.path, commit_message, content, existing_file.sha)

  #  print(f"File '{filename}' updated successfully in the GitHub repository.")
#except Exception as e:
    # If the file doesn't exist, create a new one
#    repo.create_file(filename, commit_message, content)

 #   print(f"File '{filename}' created successfully in the GitHub repository.")
    
    
