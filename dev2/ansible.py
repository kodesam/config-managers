import openai
import yaml
import streamlit as st
import pandas as pd 

openai.api_key = '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'

def generate_ansible_script(module, tasks):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Write an ansible script using the {module} module to {tasks}"},
        ]
    )

    ansible_script = response['choices'][0]['message']['content']

    st.text(ansible_script)  # Just to print and debug the returning prompt.

    try:
        ansible_yaml = yaml.safe_load(ansible_script)
    except yaml.YAMLError as e:
        ansible_yaml = {"Error": f"Failed to generate YAML - {str(e)}"}

    return ansible_yaml


module = st.text_input('Enter module here', '')
tasks = st.text_area('Enter tasks here', '')

if st.button('Generate Ansible Script'):
    if module and tasks:
        yaml_dict = generate_ansible_script(module, tasks)
        if "Error" in yaml_dict:
            st.error(yaml_dict["Error"])  # Show error message if there was a problem parsing YAML.
        else:
            yaml_script = yaml.safe_dump(yaml_dict)
            st.code(yaml_script, language='yaml')
    else:
        st.markdown('Please enter module and tasks')