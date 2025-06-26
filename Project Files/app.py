import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="HealthAI Chatbot", layout="centered")

API_KEY = os.getenv("IBM_API_KEY")
ENDPOINT = os.getenv("IBM_GRANITE_ENDPOINT")

def get_granite_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "ibm/granite-13b-chat-v2",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "Error: Could not get a response from Granite."
    except Exception as e:
        return f"Error: {e}"

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h2 class='title'>🩺 HealthAI: Healthcare Chatbot</h2>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask your health question...", key="input")

if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        with st.spinner("HealthAI is thinking..."):
            reply = get_granite_response(user_input)
        st.session_state.chat_history.append(("HealthAI", reply))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"<div class='user-msg'><b>You:</b> {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'><b>HealthAI:</b> {message}</div>", unsafe_allow_html=True)
