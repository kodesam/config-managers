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


# Rest of your code goes here...
        
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

# Assuming you have a GitHub personal access token
   # github_token = "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"
   # repo_owner = "kodesam"
   # repo_name = "collection-i-runbooks"
    base_filename = prompt

try:
    # Your existing code here
    
    # Specify the folder path in the repository
    folder_path = "ansible"
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
    st.error("File alredy exist in Github Repository folder.")
except NameError as e:
    # Handle the NameError
    st.error("An error occurred with a variable name. Please check your code and try again.")
except Exception as e:
    # Handle other exceptions
    st.error("An unexpected error occurred. Please try again later.")
