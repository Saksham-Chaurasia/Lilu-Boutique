# streamlit_authenticator.py

import streamlit as st
from connection_database import db
import streamlit_authenticator as stauth
# Function to authenticate user

def authenticate(username, password):
    conn = db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to add new user to database
def add_user(username, password):
    conn = db()
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    conn.commit()
    conn.close()


# Signup form
def signup_form():
    st.header("Sign Up")
    username = st.text_input("Username", key="signup_username_input")  # Unique key for username input
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if password == confirm_password:
            # Check if username already exists
            conn = db()
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            existing_user = cursor.fetchone()
            conn.close()
            if existing_user:
                st.error("Username already exists. Please choose a different username.")
            else:
                # Add user to database
                add_user(username, password)
                st.success("Account created successfully! You can now log in.")
        else:
            st.error("Passwords do not match. Please try again.")


# Login form
# Login form
def login_form():
    st.header("Login")
    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")
    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.success("Login successful!")
            return username, True  # Return username and authentication status
        else:
            st.error("Invalid username or password")
            return None, False  # Return None for username and False for authentication status
    else:
        return None, None  # Return None for both username and authentication status if button not clicked



login_form()
signup_form()