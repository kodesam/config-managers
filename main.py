import streamlit as st
from hashlib import sha256

def check_password(stored_password, user_password):
    if stored_password == user_password:
        return True
    else:
        return False

def hash_pass(password):
    return sha256(password.encode('utf-8')).hexdigest()

def main():
    stored_password = 'yourhashedpassword' # replace with any hashed password
    menu = ["Login","HomePage"] 
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User_Name")
        password = st.sidebar.text_input("Password",type='password')
        hashed_password = hash_pass(password)
        
        if st.sidebar.button("Login"):
            result = check_password(stored_password, hashed_password)

            if result:
                st.success("Logged In as {}".format(username))
                task = st.selectbox("Task",["Add_Post","Manage_Blog","Analytics","Profiles"])
                if task == "Add_Post":
                    st.subheader("Add Your Blog Post")
                elif task == "Manage_Blog":
                    st.subheader("Manage Your Posts")
                elif task == "Analytics":
                    st.subheader("Analytics")
                elif task == "Profiles":
                    st.subheader("User Profiles")
            
            else:
                st.warning("Invalid Username/Password")
    elif choice == "HomePage":
        st.subheader("Home")
        st.info("This is a HomePage")

if __name__ == '__main__':
    main()
