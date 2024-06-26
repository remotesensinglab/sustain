import streamlit as st
import pyrebase
import os
from streamlit import session_state as sess
load_dotenv(".env")

# Load the Firebase configuration from Streamlit secrets

FBASE_CONFIG = {
    'apiKey': os.getenv("FBASE_API_KEY"),
    'authDomain': os.getenv("FBASE_AUTH_DOMAIN"),
    'projectId': os.getenv("FBASE_PROJECT_ID"),
    'storageBucket': os.getenv("FBASE_STORAGE_BUCKET"),
    'messagingSenderId': os.getenv("FBASE_MESSAGING_SENDER_ID"),
    'appId': os.getenv("FBASE_APP_ID"),
    'measurementId': os.getenv("FBASE_MEASUREMENT_ID"),
    'databaseURL': os.getenv("FBASE_DATABASE_URL")
}
# Optionally, display some Firebase configuration info using Streamlit
# st.write("Firebase Project ID:", FBASE_CONFIG['projectId'])
# st.write("Firebase App ID:", FBASE_CONFIG['appId'])

# Initialize Firebase with the configuration
firebase = pyrebase.initialize_app(FBASE_CONFIG)

auth = firebase.auth()
db = firebase.database()
# Temporarily replace quote function
def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote


def get_full_name_from_db(
        email
):
    query = db.child("user_info").order_by_child("email").equal_to(email).limit_to_first(1).get()
    for i in query.each():
        first_name = i.val()['first_name']
        middle_name = i.val()['middle_name']
        last_name = i.val()['last_name']
        if middle_name is None:
            full_name = f"{first_name} {last_name}"
        else:
            full_name = f"{first_name} {middle_name} {last_name}"
    return full_name


def logged_in_clicked(
        email,
        password
):
    try:
        _ = auth.sign_in_with_email_and_password(
            email,
            password
        )
        sess['username'] = get_full_name_from_db(email)
        sess['logged_in'] = True
    except :
        sess['logged_in'] = False
        st.error('Invalid user name or password')


def show_login_page():
    placeholder = st.container()
    with placeholder:
        if sess.logged_in == False:
            email = st.text_input(
                label='Enter your email *'
            )
            password = st.text_input(
                label='Enter your password',
                type="password"
            )
            st.button(
                label='Sign In',
                on_click=logged_in_clicked,
                args=(email, password)
            )
            signup_link = '<a href="https://sustain-reg-ld2wj8dbxecjbibe9znbuc.streamlit.app/" target="_bank">New user? Sign Up here!</a>'
            st.markdown(signup_link, unsafe_allow_html=True)
