import streamlit as st
from password_strength import PasswordPolicy

def check_form_inputs(
    first_name,
    last_name,
    email,
    password,
    password_check,
    org
):
    # Check if the items are empty or not
    check_vars = [
        first_name,
        last_name,
        email,
        password,
        password_check,
        org
    ]
    # Define the password policy
    policy = PasswordPolicy.from_names(
        length=8,  # min length: 8
        uppercase=1,  # need min. 2 uppercase letters
        numbers=1,  # need min. 2 digits
    )
    
    if not all(check_vars):
        st.error('Please insert all the required information to proceed (*)')
    elif password != password_check:
        st.error('Passwords do not match')
    elif len(policy.test(password)) > 0:
        st.error('Please use at least 8 characters with 1 uppercase and 1 digit in your password')
    else:
        return True