import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API credentials from .env
load_dotenv()
API_KEY = os.getenv("IBM_API_KEY")
ENDPOINT = os.getenv("IBM_END_POINT")

# Function to get response from IBM Granite
def get_granite_response(user_input):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "ibm/granite-13b-chat-v2",
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception: {str(e)}"

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Page configuration
st.set_page_config(page_title="HealthAI Chatbot", layout="centered")
st.markdown("<h2 style='text-align: center;'>🩺 HealthAI: Healthcare Chatbot</h2>", unsafe_allow_html=True)

# Chat input box
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Enter your health question here...")
    submit = st.form_submit_button("Send")

    if submit and user_input:
        st.session_state.chat_history.append(("You", user_input))
        with st.spinner("HealthAI is responding..."):
            response = get_granite_response(user_input)
        st.session_state.chat_history.append(("HealthAI", response))

# Display chat history
for sender, message in st.session_state.chat_history:
    align = "right" if sender == "You" else "left"
    color = "#1a73e8" if sender == "You" else "#2e7d32"
    st.markdown(
        f"<div style='text-align: {align}; padding: 8px; color: {color};'><b>{sender}:</b> {message}</div>",
        unsafe_allow_html=True
    )
