import streamlit as st
from chatbot import LegalChatbot
from PIL import Image
import time

def set_custom_style():
    st.markdown("""
        <style>
        .stApp {
            background-color: #6A4F68;
        }
        .stTextInput > div > div > input {
            color: black !important;
        }
        .stButton > button {
            color: #DCDDDC;
            background-color: #6A4F68;
            border-color: #DCDDDC;
        }
        .stMarkdown, .stText, h1, h2, h3, p {
            color: #DCDDDC !important;
        }
        .multilingual-legal-advisor {
            color: black !important;
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .multilingual-legal-advisor * {
            color: black !important;
        }
        /* Style for sidebar */
        [data-testid="stSidebar"] {
            background-color: #f0f0f0;
            padding: 20px;
        }
        [data-testid="stSidebar"] .stSelectbox {
            margin-bottom: 20px;
        }
        .sidebar-label {
            background-color: #6A4F68;
            color: white !important;
            padding: 10px;
            border-radius: 5px;
            font-size: 17px !important;
            font-weight: bold !important;
            margin-bottom: 5px;
            display: block;
        }
        /* Change cursor to hand pointer for dropdown menus */
        [data-testid="stSidebar"] .stSelectbox > div > div > div {
            cursor: pointer !important;
        }
        [data-testid="stSidebar"] .stSelectbox select {
            cursor: pointer !important;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Multilingual Legal Advisor", page_icon="⚖️", layout="wide")
    set_custom_style()
    
    left_column, right_column = st.columns([2, 1])

    with left_column:
        st.markdown("<h1 style='color: #DCDDDC;'>Multilingual Legal Advisor</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #DCDDDC;'>We offer legal advice with reference to criminal law within the United Kingdom in both English and French</p>", unsafe_allow_html=True)
        
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'chatbot' not in st.session_state:
            st.session_state.chatbot = None
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'language' not in st.session_state:
            st.session_state.language = "English"
        if 'jurisdiction' not in st.session_state:
            st.session_state.jurisdiction = "All"
        if 'ending_session' not in st.session_state:
            st.session_state.ending_session = False
        if 'logging_out' not in st.session_state:
            st.session_state.logging_out = False
        if 'satisfaction_response' not in st.session_state:
            st.session_state.satisfaction_response = None

        if st.session_state.logging_out:
            st.info("You are now being logged out...")
            time.sleep(2)  # Wait for 2 seconds
            st.session_state.clear()
            st.rerun()

        if st.session_state.user is None:
            username = st.text_input("Enter your username to log in:")
            if st.button("Log In"):
                st.session_state.user = username
                st.rerun()
        else:
            st.markdown(f"<p style='color: #DCDDDC;'>Welcome to the Multilingual Legal Advisor, {st.session_state.user}!</p>", unsafe_allow_html=True)
            
            # Add language and jurisdiction selection to sidebar
            with st.sidebar:
                st.markdown('<p class="sidebar-label">Kindly select your preferred language:</p>', unsafe_allow_html=True)
                new_language = st.selectbox(
                    label="Language",
                    options=["English", "French"],
                    index=["English", "French"].index(st.session_state.language) if st.session_state.language in ["English", "French"] else 0,
                    label_visibility="collapsed"
                )
                
                st.markdown('<p class="sidebar-label">Select your preferred jurisdiction:</p>', unsafe_allow_html=True)
                new_jurisdiction = st.selectbox(
                    label="Jurisdiction",
                    options=["All", "England & Wales", "Scotland", "Northern Ireland"],
                    index=["All", "England & Wales", "Scotland", "Northern Ireland"].index(st.session_state.jurisdiction) if st.session_state.jurisdiction in ["All", "England & Wales", "Scotland", "Northern Ireland"] else 0,
                    label_visibility="collapsed"
                )
                
                if st.button("Update Language and Jurisdiction"):
                    if st.session_state.chatbot is None:
                        st.session_state.chatbot = LegalChatbot(new_language, new_jurisdiction)
                    else:
                        st.session_state.chatbot.update_language_and_jurisdiction(new_language, new_jurisdiction)
                    
                    st.session_state.language = new_language
                    st.session_state.jurisdiction = new_jurisdiction
                    st.session_state.messages.append({"role": "system", "content": f"Language changed to {new_language} and jurisdiction changed to {new_jurisdiction}."})
                    st.rerun()

            st.markdown(f"<p style='color: #DCDDDC;'>Current Language: {st.session_state.language}, Current Jurisdiction: {st.session_state.jurisdiction}</p>", unsafe_allow_html=True)
            
            if not st.session_state.ending_session:
                st.markdown("<h2 style='color: #DCDDDC;'>Chat with Multilingual Legal Advisor</h2>", unsafe_allow_html=True)
                chat_container = st.container()
                with chat_container:
                    for message in st.session_state.messages:
                        if message['role'] == 'user':
                            st.markdown(f"<p style='color: #DCDDDC;'>You: {message['content']}</p>", unsafe_allow_html=True)
                        elif message['role'] == 'system':
                            st.markdown(f"<div class='multilingual-legal-advisor'><strong>System:</strong> {message['content']}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='multilingual-legal-advisor'><strong>Multilingual Legal Advisor:</strong> {message['content']}</div>", unsafe_allow_html=True)
                
                user_input = st.chat_input("Reply to your Multilingual Legal Advisor")

                if user_input:
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    if st.session_state.chatbot is None:
                        st.session_state.chatbot = LegalChatbot(st.session_state.language, st.session_state.jurisdiction)
                    response = st.session_state.chatbot.get_response(user_input, st.session_state.messages)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("New Chat"):
                        st.session_state.messages = []
                        st.rerun()
                with col2:
                    if st.button("End Session"):
                        st.session_state.ending_session = True
                        st.session_state.satisfaction_response = None
                        st.rerun()
            else:
                if st.session_state.satisfaction_response is None:
                    st.warning("Are you sure you want to end the session?")
                    satisfaction = st.radio("Were you satisfied with the answers from the Multilingual Legal Advisor?", ("Yes", "No"))
                    if st.button("Submit Feedback"):
                        st.session_state.satisfaction_response = satisfaction
                        st.rerun()
                else:
                    if st.session_state.satisfaction_response == "Yes":
                        st.success("Thank you for using our Multilingual Legal Advisor service!")
                    else:
                        st.warning("We apologize that we couldn't meet your expectations. Here are some additional resources that might be helpful:")
                        st.markdown("1. [Government Legal Resources](https://www.gov.uk/browse/justice)")
                        st.markdown("2. [Citizens Advice](https://www.citizensadvice.org.uk/law-and-courts/)")
                        st.success("Thank you for using our Multilingual Legal Advisor service!")
                    
                    if st.button("Confirm End Session"):
                        st.session_state.logging_out = True
                        st.rerun()

        st.markdown("<hr style='border-color: #DCDDDC;'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #DCDDDC;'><strong>Disclaimer:</strong> The Multilingual Legal Advisor provides general legal information only. Our responses are not a substitute for an attorney's advice. Consult a licensed attorney for your specific situation.</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #DCDDDC;'><strong>Data Privacy Statement:</strong> Your privacy is our priority. We ensure that all personal data collected through this chatbot is processed in strict compliance with the General Data Protection Regulation (GDPR). We are committed to safeguarding your information and will only use it for the purposes of providing accurate and relevant legal guidance. For more information, please refer to our Privacy Policy.</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #DCDDDC;'>This is a proof of concept output for Dissertation Project for Adebowale Odufuwa (2236525)</p>", unsafe_allow_html=True)

    with right_column:
        image = Image.open("professional_lady.jpg")
        fixed_width = 400
        aspect_ratio = image.height / image.width
        new_height = int(fixed_width * aspect_ratio)
        image = image.resize((fixed_width, new_height))
        st.image(image)

if __name__ == "__main__":
    main()