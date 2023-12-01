import paramiko
import streamlit as st

# Get the Ansible server connection details from the sidebar input fields
ansible_host = st.sidebar.text_input("Ansible Host")
ansible_username = st.sidebar.text_input("Ansible Username")
ansible_password = st.sidebar.text_input("Ansible Password", type="password")

# Connect to the Ansible server via SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ansible_host, username=ansible_username, password=ansible_password)

# Execute the command on the Ansible server
msg = "ls"
command = f"echo '{msg}' >> output.txt"  # Replace with the appropriate command to run on the server
 #stdin, stdout, stderr = ssh_client.exec_command(command)

# Print the results (optional)
# print(stdout.read().decode())

# Close the SSH connection
#ssh_client.close()
