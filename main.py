import streamlit as st
import os

def login():
    # Get username and password from the user
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

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
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.title("Welcome to the app")

        # Provide access to the 'pages' folder
        folder_path = "Pages"
        files = os.listdir(folder_path)
        file_names = [os.path.splitext(file)[0] for file in files]

        st.write("Available files in 'pages' folder:")
        selected_file_name = st.selectbox("Select a file", file_names)

        if selected_file_name:
            index = file_names.index(selected_file_name)
            file_path = os.path.join(folder_path, files[index])
            execute_python_file(file_path)

        if st.button("Logout"):
            st.session_state.logged_in = False

    else:
        if login():
            st.session_state.logged_in = True

            st.button("Logout")  # Display the logout button instead of the login form

# Run the app
if __name__ == "__main__":
    main()
