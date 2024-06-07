# import streamlit as st
# from firebase_admin import credentials, auth, firestore, initialize_app, get_app
# from PIL import Image
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Initialize Firebase
# try:
#     get_app()
# except ValueError:
#     cred = credentials.Certificate("firebase-adminsdk.json")
#     initialize_app(cred)

# db = firestore.client()

# # Configure Google API key for Generative AI
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Streamlit app setup
# st.set_page_config(page_title="Medical Intellect")
# st.header("Medical Intellect")

# # Firebase Authentication
# def login():
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         user = auth.get_user_by_email(email)
#         # Add your authentication logic here
#         st.session_state['user'] = user.uid

# def register():
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Register"):
#         user = auth.create_user(email=email, password=password)
#         st.session_state['user'] = user.uid

# def logout():
#     st.session_state.pop('user', None)

# # User authentication
# if 'user' not in st.session_state:
#     login_or_register = st.radio("Login or Register", ("Login", "Register"))
#     if login_or_register == "Login":
#         login()
#     else:
#         register()
# else:
#     st.button("Logout", on_click=logout)

# # Main app functionality
# def get_gemini_response(input, images, prompt):
#     model = genai.GenerativeModel('gemini-pro-vision')
#     response = model.generate_content([input, images[0], prompt])
#     return response.text

# def input_image_setup(uploaded_files):
#     image_parts = []
#     for uploaded_file in uploaded_files:
#         bytes_data = uploaded_file.getvalue()   
#         image_parts.append({
#             "mime_type": uploaded_file.type,
#             "data": bytes_data
#         })
#     return image_parts 


# input_prompt = """
# You are an expert in the medical field. You will receive input images of medical conditions 
# and answer questions based on the input image with accuracy.
# """

# if 'user' in st.session_state:
#     input_text = st.text_input("Input Prompt:", key="input")
#     uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

#     if uploaded_files and st.button("Analyze Images"):
#         image_data = input_image_setup(uploaded_files)
#         response = get_gemini_response(input_prompt, image_data, input_text)
#         st.subheader("The Response is")
#         st.write(response)

# # Run the app
# if __name__ == '__main__':
#     st.title("Medical Intellect")

import streamlit as st
from firebase_admin import credentials, auth, firestore, initialize_app, get_app
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv
from firebase_admin import exceptions

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase
try:
    get_app()
except ValueError:
    cred = credentials.Certificate("firebase-adminsdk.json")
    initialize_app(cred)

db = firestore.client()

# Configure Google API key for Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit app setup
st.set_page_config(page_title="Medical Intellect")
st.header("Medical Intellect")

# Firebase Authentication
def login():
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        try:
            user = auth.get_user_by_email(email)
            # Add your authentication logic here
            st.session_state['user'] = user.uid
            st.success("Logged in successfully!")
        except exceptions.FirebaseError as e:
            st.error(f"An error occurred during login: {str(e)}")

def register():
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    if st.button("Register"):
        try:
            user = auth.create_user(email=email, password=password)
            st.session_state['user'] = user.uid
            st.success("User registered successfully!")
        except exceptions.FirebaseError as e:
            if 'EMAIL_EXISTS' in str(e):
                st.error("The user with the provided email already exists. Please log in or use a different email.")
            else:
                st.error(f"An unexpected error occurred: {str(e)}")

def logout():
    st.session_state.pop('user', None)
    st.success("Logged out successfully!")

# User authentication
if 'user' not in st.session_state:
    login_or_register = st.radio("Login or Register", ("Login", "Register"))
    if login_or_register == "Login":
        login()
    else:
        register()
else:
    st.button("Logout", on_click=logout)

# Main app functionality
def get_gemini_response(input, images, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, images[0], prompt])
    return response.text

def input_image_setup(uploaded_files):
    image_parts = []
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.getvalue()   
        image_parts.append({
            "mime_type": uploaded_file.type,
            "data": bytes_data
        })
    return image_parts 

input_prompt = """
You are an expert in the medical field. You will receive input images of medical conditions 
and answer questions based on the input image with accuracy.
"""

if 'user' in st.session_state:
    input_text = st.text_input("Input Prompt:", key="input")
    uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files and st.button("Analyze Images"):
        image_data = input_image_setup(uploaded_files)
        response = get_gemini_response(input_prompt, image_data, input_text)
        st.subheader("The Response is")
        st.write(response)

# Run the app
if __name__ == '__main__':
    st.title("Medical Intellect")
