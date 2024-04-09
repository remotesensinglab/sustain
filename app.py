import os
import streamlit as st
import pyrebase
from password_strength import PasswordPolicy
from dotenv import load_dotenv

from utils import image_management as im
from utils import analyze_form as af

# Page config
st.set_page_config(
    page_title="SustaiN",
    page_icon=os.path.join(os.getcwd(), 'images', 'icon.png'),
    layout="wide"
)

FBASE_CONFIG = {
  'apiKey': st.secrets["firebase"]["apiKey"],
  'authDomain': st.secrets["firebase"]["authDomain"],
  'databaseURL': st.secrets["firebase"]["databaseURL"],
  'projectId': st.secrets["firebase"]["projectId"],
  'storageBucket': st.secrets["firebase"]["storageBucket"],
  'messagingSenderId': st.secrets["firebase"]["messagingSenderId"],
  'appId': st.secrets["firebase"]["appId"],
  'measurementId': st.secrets["firebase"]["measurementId"]
}

# Optionally, display some Firebase configuration info using Streamlit
# st.write("Firebase Project ID:", FBASE_CONFIG['projectId'])
# st.write("Firebase App ID:", FBASE_CONFIG['appId'])

# Authenticate firebase and database
firebase = pyrebase.initialize_app(FBASE_CONFIG)
auth = firebase.auth()
db = firebase.database()

im.insert_image(
    os.path.join(os.getcwd(), 'images', 'logo.png'),
    sidebar=False,
    margin=(0, 0, 30, 0),
    width='auto'
)

sign_up_placeholder = st.empty()

with sign_up_placeholder.form(key='sign_up_form'):
    col1, col2, col3 = st.columns(3)
    with col1:
        first_name = st.text_input(label='First Name *', placeholder='e.g., John')
    with col2:
        middle_name = st.text_input(label='Middle Name', placeholder='e.g., K.')
    with col3:
        last_name = st.text_input(label='Last Name *', placeholder='e.g., Doe')
    email = st.text_input(
        label='Enter your email *',
        placeholder='e.g., youremail@gmail.com'
    )
    password = st.text_input(
        label='Create a password *',
        type="password",
        placeholder="Password"
    )
    password_check = st.text_input(
        label='Retype password *',
        type="password",
        placeholder="Password again"
    )
    org = st.text_input(
        label='Organization/Company *',
        placeholder="Name of your organization or company"
    )
    col4, col5, col6 = st.columns(3)
    with col4:
        org_type = st.radio(
            label='Occupation*',
            options=[
                'Researcher',
                'Student',
                'Farmer',
                'Policy Developer'
            ]
        )
    with col5:
        industry = st.radio(
            label='Industry Type *',
            options=[
                'University',
                'Private',
                'Government',
                'Non-profit'
            ]
        )
    with col6:
        crop = st.radio(
            label='Which crop do you work with? *',
            options=[
                'Corn/Maize',
                'Sorghum',
                'Both'
            ]
        )
    with st.expander("By signing up, you are agreeing to the following terms and conditions"):
        st.write(
            """
            ### Terms and conditions

            Welcome to SustaiN, a software application designed to assist in the
            decision-making process of the registered users. Please read the following
            Terms and Conditions carefully as they govern the use of the software
            application.

            1. Acceptance of Terms and Conditions: By accessing and using SustaiN, you
            acknowledge that you have read, understood, and agree to comply with these
            Terms and Conditions, as well as any applicable laws, rules, or regulations.
            If you do not agree to these Terms and Conditions, you must not use SustaiN.

            2. Use of SustaiN: The results from SustaiN cannot be sold elsewhere. The
            information from SustaiN can only be used for accelerating the decision-making
            procedure of the registered user in their farming or educational or research
            purposes. The user cannot share his account information to other parties.

            3. Intellectual Property Rights: All intellectual property rights, including
               but
            not limited to trademarks, copyrights, patents, trade secrets, and other
            proprietary rights, in and to SustaiN, are the property of the developer of
            SustaiN. You shall not reproduce, modify, distribute, display, or sell any
            part of SustaiN without the prior written consent of the developer of SustaiN.

            4. Disclaimer of Warranties: SustaiN is provided on an "as-is" and "as
               available"
            basis. The developer of SustaiN does not guarantee or warrant that SustaiN
            will be uninterrupted, error-free, or virus-free. The developer of SustaiN
            makes no representation or warranty of any kind, either express or implied,
            with respect to SustaiN, including but not limited to warranties of
            merchantability, fitness for a particular purpose, non-infringement, or
            suitability for any purpose.

            5. Limitation of Liability: In no event shall the developer of SustaiN be
               liable
            for any direct, indirect, incidental, consequential, special, punitive, or
            exemplary damages, including but not limited to damages for loss of profits,
            goodwill, use, data or other intangible losses (even if the developer of
            SustaiN has been advised of the possibility of such damages), arising out of
            or in connection with the use or inability to use SustaiN.

            6. Modification of Terms and Conditions: The developer of SustaiN reserves the
            right to modify these Terms and Conditions at any time, and any modifications
            will be effective immediately upon posting. Your continued use of SustaiN
            after the modifications have been posted will constitute your acceptance of
            the modified Terms and Conditions.

            7. Governing Law and Jurisdiction: These Terms and Conditions shall be
               governed by
            and construed in accordance with the laws of the jurisdiction where the
            developer of SustaiN is located. Any dispute arising out of or in connection
            with these Terms and Conditions shall be resolved by the courts in that
            jurisdiction.

            8. Termination of Access: The developer of SustaiN reserves the right to
               terminate
            your access to SustaiN at any time, without notice, for any reason whatsoever.

            By signing up or by using SustaiN, you signify that you have read, understood,
            and agree to be bound by these Terms and Conditions. If you have any
            questions, please reach out to [Sourav Bhadra](mailto:sourav.bhadra@slu.edu)
            or [Vasit Sagan](mailto:vasit.sagan@slu.edu) regarding your questions.

            """
        )
    submit_button = st.form_submit_button(label='Sign Up')
    st.markdown(
        '<a href="https://sustain-app-twpetauroxftmkklm4qunx.streamlit.app/" target="_blank">Already have an account? Sign In Instead!</a>',
        unsafe_allow_html=True
    )

if submit_button:

    check_result = af.check_form_inputs(
        first_name,
        last_name,
        email,
        password,
        password_check,
        org
    )

    if check_result:
        try:
            # Sign up the user
            user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])

            # Push user information to the database
            table_ref = db.child("user_info")
            new_record = {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "email": email,
                "organization": org,
                "organization_type": org_type,
                "industry": industry,
                "crop": crop
            }
            table_ref.push(new_record)
            sign_up_placeholder.empty()
            st.balloons()
            st.success('Your account has been created. Check your email to verify.', icon="✅")
            st.markdown(
                '<a href="https://sustain-app-twpetauroxftmkklm4qunx.streamlit.app/" target="_blank">Go to sign In</a>',
                unsafe_allow_html=True
            )
        except Exception as e:
            # print(e)
            st.error('There is already an account registered using the email')
