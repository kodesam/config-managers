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

        folder_path = "pages"
        files = os.listdir(folder_path)
        
        # Add Logout option
        if st.sidebar.button("Logout"):
            st.caching.clear_cache()
            st.experimental_rerun()
        
        st.sidebar.write("Available files in 'pages' folder:")
        selected_file = st.sidebar.selectbox("Select a file", files)

        if selected_file:
            file_path = os.path.join(folder_path, selected_file)
            execute_python_file(file_path)

    else:
        st.title("Login")
        if st.button("Submit"):
            st.error("Login failed. Please check your credentials.")

# Run the app
if __name__ == "__main__":
    main()
