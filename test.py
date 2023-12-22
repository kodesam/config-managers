import streamlit as st
from github import Github, GithubException
from openai import OpenAI
import streamlit as st

# Get available models
available_models = ['gpt-3.5-turbo-16k-0613','gpt-3.5-turbo-16k-1106','gpt-3.5', 'gpt-3.0']

title_style = (
    "color: blue;"
    "font-weight: bold;"
)

# Display the title with the defined style
st.markdown(f"<h1 style='{title_style}'>💬 BlueRunBook-AI</h1>", unsafe_allow_html=True)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    models = st.multiselect("Select Models", available_models, default=available_models)
    instructions = st.text_area("Instructions", height=200)
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
    
    # Split the instructions by lines
    instruction_lines = instructions.split("\n")
    
    # Add each instruction separately to the messages
    for instruction in instruction_lines:
        st.session_state.messages.append({"role": "assistant", "content": instruction})
    
    # Include the instructions in the API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
    )
    
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
