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

# Main Streamlit app
def main():
    st.title("My App")

    if login():
        st.success("Login successful!")
        st.write("Welcome to the app.")

        # Provide access to the 'pages' folder
        folder_path = 'dev2'
        files = os.listdir(folder_path)

        # Display the available files in the 'pages' folder
        st.write("Available files in 'pages' folder:")
        for index, file in enumerate(files):
            st.write(f"{index + 1}. {file}")

        selected_file = st.selectbox("Select a file to execute", files)
        if selected_file:
            file_path = os.path.join(folder_path, selected_file)

            # Execute the chosen Python file
            try:
                exec(open(file_path).read())
            except Exception as e:
                st.error(f"Error executing {selected_file}: {e}")

    else:
        st.error("Login failed. Please check your credentials.")

# Run the app
if __name__ == "__main__":
    main()
