import openai
import yaml
import streamlit as st
import pandas as pd
from github import Github, GithubException
import random
import re


title_style = (
    "color: #001C7B;"
    "font-weight: bold;"
)

title_style_1 = (
    "color: #001C7B;"
    "font-weight: normal;"
)
# Display the title with the defined style
st.markdown(f"<h1 style='{title_style}'>💬 🚀🚀 Script-AI 🚀🚀 </h1>", unsafe_allow_html=True)
st.caption("🚀 🚀 🚀 Script-AI Powered by OpenAI LLM")
st.markdown(f"<h2 style='{title_style_1}'>💬  Ansible Task </h2>", unsafe_allow_html=True)
# Place your actual OpenAI API key here
# openai.api_key = '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'

with st.sidebar:
    st.title(f"<h1 style='{title_style}'>💬 Script-AI 🚀🚀</h1>", unsafe_allow_html=True)
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    
    openai_api_key = st.text_input("OpenAI API Key", type="password")

if openai_api_key:
    openai.api_key = openai_api_key
else:
    st.warning("Please add your OpenAI API key to continue.")
##############
def read_modules(file_path):
    with open(file_path) as f:
        modules = [line.strip() for line in f]
    return modules


ansible_modules_path = "pages/Module/ansible_module.txt"
azure_modules_path = "pages/Module/azure_module.txt"
aws_modules_path = "pages/Module/aws_module.txt"
win_ans_modules_path = "pages/Module/window_ansible_module.txt"
docker_modules_path = "pages/Module/docker_module.txt"
gcp_modules_path = "pages/Module/gcp_module.txt"
graphana_modules_path = "pages/Module/graphana_module.txt"
junyper_modules_path = "pages/Module/junyper_module.txt"
k8s_modules_path = "pages/Module/k8s_core_module.txt"
microsoft_ad_modules_path = "pages/Module/microsoft_ad_module.txt"
openstack_modules_path = "pages/Module/openstack_module.txt"
openvswitch_module_path = "pages/Module/openvswitch_module.txt"
vmware_module_path = "pages/Module/vmware_module.txt"
vmware_rest_module_path = "pages/Module/vmware_rest_module.txt"
zabbix_module_path = "pages/Module/zabbix_module.txt"


ansible_modules = read_modules(ansible_modules_path)
azure_modules = read_modules(azure_modules_path)
aws_modules = read_modules(aws_modules_path)
ansible_window_modules = read_modules(win_ans_modules_path)
docker_modules        = read_modules(docker_modules_path)      
gcp_modules           = read_modules(gcp_modules_path)       
graphana_modules      = read_modules(graphana_modules_path)    
junyper_modules       = read_modules(junyper_modules_path)    
k8s_modules      = read_modules(k8s_modules_path)         
microsoft_ad_modules  = read_modules(microsoft_ad_modules_path)
openstack_modules     = read_modules(openstack_modules_path)  
openvswitch_module    = read_modules(openvswitch_module_path) 
vmware_module         = read_modules(vmware_module_path)      
vmware_rest_module    = read_modules(vmware_rest_module_path)
zabbix_module         = read_modules(zabbix_module_path)

module_type = st.selectbox("Select Module Type", ["Ansible", "Azure", "AWS", "window:ansible", "Docker", "GCP", "Grafana", "Juniper", "Kubernetes_Core", "Microsoft-AD", "OpenStack", "Openvswitch", "VMware", "VMware-Rest", "Zabbix"])

if module_type == "Ansible":
    modules = ansible_modules
elif module_type == "Azure":
    modules = azure_modules
elif module_type == "AWS":
    modules = aws_modules
elif module_type == "window:ansible":
    modules = ansible_window_modules
elif module_type == "Docker":
    modules =  docker_modules   
elif module_type == "GCP":
    modules = gcp_modules
elif module_type == "Grafana":
    modules = graphana_modules
elif module_type == "Juniper":
    modules = junyper_modules
elif module_type == "Kubernetes_Core":
    modules = k8s_modules
elif module_type == "Microsoft-AD":
    modules = microsoft_ad_modules
elif module_type == "OpenStack":
    modules =  openstack_modules  
elif module_type == "Openvswitch":
    modules =  openvswitch_module
elif module_type == "VMware":
    modules =  vmware_module
elif module_type == "VMware-Rest":
    modules =  vmware_rest_module
elif module_type == "Zabbix":
    modules =  zabbix_module 

module = st.selectbox("Select Module", modules)

#######






def generate_ansible_script(module, tasks):
    # Mask IP addresses
    tasks = re.sub(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', '***.***.***.***', tasks)

    # return tasks  # Return the filtered prompt if it doesn't contain sensitive content

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




#module = st.selectbox('Select module', ansible_modules)
tasks = st.text_area('Enter tasks here', '')
response_text = ''

if st.button('Generate Ansible Script'):
    if module and tasks:
        # List of sensitive keywords
        sensitive_keywords = ['sensitive', 'Nokia', 'vodafoneziggo', 'oddido','kpn','confidential', 'copyright', 'cognizant']

        # Function to check for sensitive keywords in the task input
        def check_sensitive_content(tasks):
            for keyword in sensitive_keywords:
                if re.search(fr'\b{keyword}\b', tasks, flags=re.IGNORECASE):
                    return True
            return False

        # Check for sensitive content in the task input
        sensitive_content = check_sensitive_content(tasks)

        # Display warning if sensitive content is detected
        if sensitive_content:
            st.warning("The task contains sensitive content. Please remove any sensitive information and try again.")
        else:
            response_text = generate_ansible_script(module, tasks)
            if response_text:
                st.text_area("Response:", value=response_text, height=400)
    else:
        st.markdown('Please enter module and tasks')


# Generate a random number
random_number = random.randint(1, 1000)

# Prompt the user for GitHub credentials
github_token_ = st.sidebar.text_input("GitHub Personal Access Token", type="password")
repo_owner_ = st.sidebar.text_input("Repository Owner")
repo_name_ = st.sidebar.text_input("Repository Name")
folder_path_ = st.sidebar.text_input("Folder Path")
branch_name_ = st.sidebar.text_input("Branch Name", value="main")


# Assuming you have a GitHub personal access token
github_token = "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"
repo_owner = "kodesam"
repo_name = "pipeline"
folder_path = "demo"
branch_name = "demo"

st.sidebar.markdown("<p class='developer-name'>Developer : Aamir </p>", unsafe_allow_html=True)

# Update the base_filename and filename
base_filename = "code"
filename = f"{base_filename}_{random_number}.yaml"

if response_text and github_token and repo_owner and repo_name and folder_path and branch_name:
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
            commit_message = f"Create {tasks}"
            repo.create_file(file_path, commit_message, response_text, branch=branch_name)
            st.sidebar.text(f"File '{filename}' created successfully in the GitHub repository.")
            st.success('Success message')
        else:
            st.sidebar.text(f"File '{filename}' already exists in the GitHub repository. Skipping creation.")
    except AssertionError as e:
        # Handle the AssertionError
        st.error("An error occurred while creating the file. Please try again later.")
    except GithubException as e:
        # Handle the GitHub exception
        st.error("File already exists in GitHub Repository folder.")
