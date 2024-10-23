import streamlit as st
import firebase_admin

from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore

import requests





# Firebase configuration

cred = credentials.Certificate('C:\dbmschatapp\dbms-test-c9871-55e52fdea801.json')

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
else:
    print("Firebase app already initialized.")
    
db = firestore.client()  # Initialize Firestore    

FIREBASE_WEB_API_KEY = 'AIzaSyAFP5HU9ebgCYi1Pk3SycHzvwAP0GFnVEA'

# User Authentication
def login(email, password):
    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        
        response = requests.post(url, json=payload)
        
        # Check if the response was successful
        if response.status_code == 200:
            user_data = response.json()
            return user_data['idToken'], user_data['email']  # Return the ID token and email if successful
        else:
            # Handle specific error responses
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", "Login failed. Please try again.")
            
            # Customize messages based on known error codes
            if "INVALID_PASSWORD" in error_message:
                st.warning("Incorrect password. Please try again.")
            elif "USER_NOT_FOUND" in error_message:
                st.warning("No user found with this email.")
            elif "INVALID_EMAIL" in error_message:
                st.warning("Invalid email format. Please check your email.")
            else:
                st.warning(error_message)  # General error message
            
            return None, None  # Ensure we always return two values

    except Exception as e:
        st.warning(f"Login failed: {e}")
        return None, None  # Ensure we always return two values

def signup(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        st.success("User created successfully")
    except Exception as e:
        st.warning(f"Signup failed: {e}")

# Streamlit UI
st.title("Chat App")

menu = ["Login", "Signup", "Chat"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        token, user_email = login(email, password)  # Get token and email from login function
        if token:  # Only set session state and show success if token is valid
            st.session_state['token'] = token
            st.session_state['user_email'] = user_email  # Store user email for later use
            st.success("Login successful!")
        else:
            # No need for additional handling here; error messages are already shown in the login function
            pass

elif choice == "Signup":
    username = st.text_input("Create your username")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    if st.button("Signup"):
        
        user= auth.create_user(email = email, password = password, uid = username)
        
        st.success("User created successfully")
        st.markdown('Please login using your email and password')
        st.balloons()
        
elif choice == "Chat":
    if 'token' in st.session_state:
        friend_email = st.text_input("Enter friend's email:")
        
        if friend_email:
            # Create a unique chat ID based on both users' emails (or IDs)
            chat_id = f"{st.session_state['user_email']}_{friend_email}"
            messages_ref = db.collection('chats').document(chat_id).collection('messages')

            # Fetch messages from Firestore and order by timestamp
            messages = messages_ref.order_by('timestamp').stream()

            # Display chat messages in the UI
            for msg in messages:
                message_data = msg.to_dict()
                with st.chat_message(message_data["role"]):
                    st.markdown(message_data["content"])

            # Accept user input for chat messages
            if prompt := st.chat_input("Type your message here..."):
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Add user message to Firestore with a timestamp
                messages_ref.add({
                    'content': prompt,
                    'role': 'user',
                    'timestamp': firestore.SERVER_TIMESTAMP  # Automatically set timestamp
                })

                # Placeholder for bot response
                response_content = f"Echo: {prompt}"  

                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(response_content)

                # Add assistant response to Firestore (optional)
                messages_ref.add({
                    'content': response_content,
                    'role': 'assistant',
                    'timestamp': firestore.SERVER_TIMESTAMP  # Automatically set timestamp
                })
    else:
        st.warning("Please log in to chat.")