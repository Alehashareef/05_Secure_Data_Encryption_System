import streamlit as st
import time
import hashlib
import json
import os
from datetime import datetime, timedelta
from time import sleep

# Set page configuration for better layout and theme
st.set_page_config(page_title="Secure Data Encryption", layout="wide", initial_sidebar_state="expanded")

# Dark Theme (optional)
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #121212;
        color: white;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True
)

# Path to the user data file
DATA_FILE = "user_data.json"

# Create columns for a more organized layout
col1, col2 = st.columns([1, 4])

# Add logo/image in the first column
with col1:
    st.image('logo.png.png', width=150)

# Welcome message in the second column
with col2:
    st.title("Secure Data Encryption System!")

# Sidebar with navigation options
with st.sidebar:
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("logo.png.png", width=50)
    with col2:
        st.markdown("### Secure Menu!")
    
    menu = st.radio("**Select an option to get started:**", ["Home", "Insert Data", "Retrieve Data", "Login"])

# Load user data from the file
def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save user data to the file
def save_user_data(user_data):
    with open(DATA_FILE, 'w') as file:
        json.dump(user_data, file)

# Hash password using PBKDF2
def hash_password(password):
    salt = b"some_random_salt"  # You should store salt securely
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

# Handle login attempts
attempts = {}
lockout_time = timedelta(minutes=5)

# Handle the menu options
if menu == "Home":
    st.markdown(""" 
    <div style="text-align: center;">
        <h3><strong>Welcome to your secure vault</strong></h3>
        <p>Use the sidebar to encrypt, store, or retrieve your sensitive data safely.</p>
    </div>
""", unsafe_allow_html=True)

elif menu == "Insert Data":
    st.markdown("### Insert Data")
    # Input fields with icons
    user = st.text_input("Enter Username", max_chars=20)
    data = st.text_area("Enter Data to Encrypt", height=150)
    passkey = st.text_input("Enter Passkey", type="password")

    # Stylish button with emoji
    if st.button('Encrypt & Store'):
        if user and data and passkey:
            # Simulate encryption and store data
            user_data = load_user_data()
            encrypted_data = hashlib.sha256(data.encode()).hexdigest()  # Simple encryption placeholder
            
            if user in user_data:
                user_data[user]['data'] = encrypted_data
            else:
                user_data[user] = {'data': encrypted_data, 'password': hash_password(passkey)}
            
            save_user_data(user_data)
            st.success("Data has been securely stored!")
        else:
            st.warning("Please fill all fields.")

elif menu == "Retrieve Data":
    st.markdown("### Retrieve Data")
    # Retrieve data with passkey
    retrieve_user = st.text_input("Enter Username to Retrieve Data", max_chars=20)
    retrieve_passkey = st.text_input("Enter Passkey", type="password")

    if st.button('Retrieve Data'):
        user_data = load_user_data()

        if retrieve_user in user_data and hash_password(retrieve_passkey) == user_data[retrieve_user]['password']:
            st.info(f"Data for {retrieve_user} retrieved successfully!")
            st.write(f"Encrypted Data: {user_data[retrieve_user]['data']}")
        else:
            st.warning("Invalid credentials or user does not exist.")

elif menu == "Login":
    st.markdown("### Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Lockout logic: track failed attempts
    if username in attempts and attempts[username]['count'] >= 3:
        time_left = attempts[username]['time'] - datetime.now()
        if time_left > timedelta():
            st.warning(f"Too many failed attempts. Please try again in {time_left.seconds//60} minutes.")
        else:
            del attempts[username]  # Reset after lockout

    if st.button("Login"):
        user_data = load_user_data()

        if username in user_data and hash_password(password) == user_data[username]['password']:
            st.success("Login Successful!")
            if username in attempts:
                del attempts[username]  # Reset attempts after successful login
        else:
            st.error("Invalid credentials. Please try again.")
            if username not in attempts:
                attempts[username] = {'count': 1, 'time': datetime.now()}
            else:
                if attempts[username]['time'] > datetime.now() - lockout_time:
                    attempts[username]['count'] += 1
                else:
                    attempts[username] = {'count': 1, 'time': datetime.now()}

# Footer
st.markdown("---")
st.markdown("""<p style='text-align: center; color: gray;'>© 2025 Secure Data Encryption System | Aleha Shareef </p>""", unsafe_allow_html=True)