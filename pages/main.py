

def check_password(stored_password, user_password):
    if stored_password == user_password:
        return True
    else:
        return False

def hash_pass(password):
    return password # replace with a real hashing function if desired

def main():
    st.title("My App")

    menu = ["Login","Home","Profile"] 
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        
        if st.sidebar.button("Login"):
            hash_pass(password) # hash the password entered by the user
            result = check_password('stored_password', password) # replace 'stored_password' with your hash password

            if result:
                st.success("Logged In Successfully")
                # your app after login
            else:
                st.warning("Incorrect Username/Password")

if __name__ == "__main__":
    main()
