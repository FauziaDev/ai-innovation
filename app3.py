import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.title("AI CHAT with Chat HISTORY")


@st.cache_resource
def get_ai_client():
    return genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )


client = get_ai_client()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Initialize Gemini chat
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = client.chats.create(
        model="gemini-2.5-flash"
    )


# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# Chat input
if user_message := st.chat_input("Say something..."):

    # Display user message
    with st.chat_message("user"):
        st.write(user_message)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Generate AI response
    with st.spinner("Thinking..."):
        response = st.session_state.gemini_chat.send_message(
            user_message
        )

    # Display AI response
    with st.chat_message("assistant"):
        st.write(response.text)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.text
    })
    