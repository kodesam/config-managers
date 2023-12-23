import streamlit as st
from github import Github, GithubException
from openai import OpenAI

# Get available models
available_models = ['gpt-3.5-turbo-16k-0613', 'gpt-3.5-turbo-16k-1106', 'gpt-3.5-turbo', 'gpt-3.5', 'gpt-3.0']

title_style = (
    "color: blue;"
    "font-weight: bold;"
)

# Display the title with the defined style
st.markdown(f"<h1 style='{title_style}'>💬 BlueRunBook-AI</h1>", unsafe_allow_html=True)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    models = st.multiselect("Select Models", available_models, default=available_models)
    instruction_1 = "code in ansible Playbook"
    instruction_2 = st.text_area("Additional Instruction", key="additional_instruction", height=200)
    st.title("💬 BlueRunBook-AI")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    st.sidebar.markdown("<p class='developer-name'>Developer: Syed Aamir</p>", unsafe_allow_html=True)
    
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    
    # Integrate with AWS Cloud
    aws_cloud = st.selectbox("Select Cloud", ["AWS", "Azure", "Google Cloud"])
    cloud_url = st.text_input("Cloud URL")
    cloud_user = st.text_input("Cloud User")
    cloud_token = st.text_input("Cloud Token")

    # Assuming you have a GitHub personal access token
    github_token = st.text_input("GitHub Token")
    repo_owner = st.text_input("GitHub Repo Owner")
    repo_name = st.text_input("GitHub Repo Name")

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

    # Include the instructions in the conversation
    st.session_state.messages.append({"role": "assistant", "content": instruction_1})
    st.session_state.messages.append({"role": "assistant", "content": instruction_2})

    # Include the instructions in the API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
    )

    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    if github_token and repo_owner and repo_name:
        try:
            # Specify the folder path in the repository
            folder_path = "ansible"
            filename = f"{folder_path}/{prompt}.yaml"

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
                st.info(f"File '{filename}' created successfully in the GitHub repository.")
            else:
                st.warning(f"File '{filename}' already exists in the GitHub repository. Skipping creation.")

        except AssertionError as e:
            # Handle the AssertionError
            st.error("An error occurred while creating the file. Please try again later.")
        except GithubException as e:
            # Handle the GitHub exception
            st.error("File already exists in the GitHub Repository folder.")
        except NameError as e:
            # Handle the NameError
            st.error("An error occurred with a variable name. Please check your code and try again.")
        except Exception as e:
            # Handle other exceptions
            st.error("An unexpected error occurred. Please try again later.")

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