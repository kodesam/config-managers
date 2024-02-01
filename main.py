import streamlit as st
import os
import datetime
import socket
from PIL import Image

def login():
    # Get username and password from the user
    st.sidebar.title("Login Here <>")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    # Hard-coded username and password for demonstration purposes
    if username == "admin" and password == "password":
        return True
    else:
        return False

def execute_python_file(file_path):
    try:
        # Execute the Python file
        exec(open(file_path).read())
    except Exception as e:
        st.error(f"Error executing {file_path}: {e}")

def log_session(event):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = socket.gethostbyname(socket.gethostname())
    log_message = f"Event: {event}\nTimestamp: {timestamp}\nIP Address: {ip_address}\n"

    with open("session_log.txt", "a") as file:
        file.write(log_message)
        file.write("\n")

def set_background():
    image = Image.open("aiexpo365.jpg")
    st.image(image,  use_column_width=True)

# Main Streamlit app
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        if login():
            st.session_state.logged_in = True
            log_session("login")

    if st.session_state.logged_in:
        st.sidebar.success("Login successful!")
        st.sidebar.write("Welcome to the app.")

        folder_path = "Pages"
        files = os.listdir(folder_path)
        file_names = [os.path.splitext(file)[0] for file in files]
        
        # Add Logout option
        if st.sidebar.button("Logout"):
            log_session("logout")
            st.session_state.logged_in = False
            st.experimental_rerun()
        
        # st.sidebar.write("Available files in 'Pages' folder:")
        selected_file_name = st.sidebar.selectbox("Select a Module", file_names, index=3)

        if selected_file_name:
            index = file_names.index(selected_file_name)
            file_path = os.path.join(folder_path, files[index])
            execute_python_file(file_path)

    else:
        #st.sidebar.title("Login")
        st.markdown(""" <h1 style='color: #002147; font-family: Arial, sans-serif;'>Script AI</h1> """, unsafe_allow_html=True)
        set_background()
        if st.button("Submit"):
            st.error("Login failed. Please check your credentials.")

# Run the app
if __name__ == "__main__":
    main()
