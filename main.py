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

@st.cache(allow_output_mutation=True)
def get_files_in_folder():
    folder_path = 'pages'
    files = os.listdir(folder_path)
    return files

# Main Streamlit app
def main():
    if login():
        st.sidebar.success("Login successful!")
        st.sidebar.write("Welcome to the app.")

        files = get_files_in_folder()

        # Provide access to the 'pages' folder
        st.write("Available files in 'pages' folder:")
        for index, file in enumerate(files):
            st.write(f"{index + 1}. {file}")

        selected_file = st.selectbox("Select a file to execute", files)

        if st.button("Execute"):
            if selected_file:
                file_path = os.path.join('pages', selected_file)

                # Execute the chosen Python file
                try:
                    exec(open(file_path).read())
                except Exception as e:
                    st.error(f"Error executing {selected_file}: {e}")
    else:
        st.title("Login")
        if st.button("Submit"):
            st.error("Login failed. Please check your credentials.")

# Run the app
if __name__ == "__main__":
    main()
