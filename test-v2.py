import streamlit as st
from streamlit_ssh import ssh

# Display the title
st.title('SSH Terminal')

# SSH Terminal
ssh_host = st.text_input("SSH Host (IP Address)")
ssh_user = st.text_input("SSH User")
ssh_password = st.text_input("SSH Password", type="password")
terminal_title = st.text_input("Terminal Title", value="SSH Terminal")

if ssh_host and ssh_user and ssh_password:
    with st.beta_expander("SSH Terminal"):
        ssh(ssh_host, ssh_user, ssh_password, terminal_title)