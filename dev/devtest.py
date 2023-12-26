import requests
import streamlit as st
import paramiko

# Input Ansible server details in the sidebar
ansible_host = st.sidebar.text_input("Ansible Server Host")
ansible_user = st.sidebar.text_input("Ansible Server Username")
ansible_password = st.sidebar.text_input("Ansible Server Password", type="password")

# Input the GitHub repository details
repo_owner = st.text_input("Repository Owner")
repo_name = st.text_input("Repository Name")
file_path = st.text_input("File Path (relative file path within the repository)")

# View the file from the GitHub repository
if st.button("View File"):
    url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{file_path}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        file_content = response.text
        st.code(file_content, language="text")
    except requests.exceptions.RequestException as e:
        st.error(str(e))
        st.stop()

# Execute the file on the selected Ansible server when the button is clicked
if st.button("Execute File"):
    # Connect to the Ansible server via SSH
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    with st.spinner(f"Connecting to Ansible server..."):
        ssh_client.connect(
            hostname=ansible_host,
            username=ansible_user,
            password=ansible_password
        )

    # Execute the file content on the Ansible server
    with st.spinner("Executing file on Ansible server..."):
        ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(file_content)
    
    # Print the execution results (optional)
    st.text(ssh_stdout.read().decode())
        
    # Close the SSH connection
    ssh_client.close()
