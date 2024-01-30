import streamlit as st
import os

def login():
    # Get username and password from the user
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

# Main Streamlit app
def main():
    if login():
        st.sidebar.success("Login successful!")
        st.sidebar.write("Welcome to the app.")

        folder_path = "Pages"
        files = os.listdir(folder_path)
        file_names = [os.path.splitext(file)[0] for file in files]
        
        # Add Logout option
        if st.sidebar.button("Logout"):
            st.experimental_rerun()
        
        st.sidebar.write("Available files in 'pages' folder:")
        selected_file_name = st.sidebar.selectbox("Select a file", file_names)

        if selected_file_name:
            index = file_names.index(selected_file_name)
            file_path = os.path.join(folder_path, files[index])
            execute_python_file(file_path)

    else:
        st.title("Login")
        if st.button("Submit"):
            st.error("Login failed. Please check your credentials.")

# Run the app
if __name__ == "__main__":
    main()
