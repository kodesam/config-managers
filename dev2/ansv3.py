import openai
import yaml
import streamlit as st
import pandas as pd 

# Place your actual OpenAI API key here
openai.api_key = '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'

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

if st.button('Generate Ansible Script'):
    if module and tasks:
        response_text = generate_ansible_script(module, tasks)
        st.text_area("Response:", value=response_text, height=200)
    else:
        st.markdown('Please enter module and tasks')