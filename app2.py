import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# App Title
st.title("THE MULTIVERSE OF CHATBOTS")

# Sidebar
st.sidebar.title("App Settings")

personality = st.sidebar.selectbox(
    "Who do you want to talk to?",
    [
        "An Expert Hacker",
        "Ironman",
        "Any Random Personality",
        "Virat Kohli",
        "An Angry Ravi Shastri",
        "A Crazy Ronaldo Fan",
        "Donald Trump",
        "A Panicked College Student at 3 AM",
        "A 1920s Mafia Boss",
        "A Highly Sarcastic Fitness Coach"
    ]
)

# Intensity Slider
intensity = st.sidebar.slider(
    "Intensity Level",
    min_value=1,
    max_value=10
)

# User Input
user_message = st.text_input("Say Something:")

# Send Button
if st.button("SEND"):

    if user_message:

        # Dynamic Avatar
        if personality == "An Expert Hacker":
            bot_avatar = "💻"

        elif personality == "Ironman":
            bot_avatar = "🤖"

        elif personality == "Virat Kohli":
            bot_avatar = "🏏"

        elif personality == "An Angry Ravi Shastri":
            bot_avatar = "🎙️"

        elif personality == "A Crazy Ronaldo Fan":
            bot_avatar = "⚽"

        elif personality == "Donald Trump":
            bot_avatar = "🇺🇸"

        elif personality == "A Panicked College Student at 3 AM":
            bot_avatar = "😰"

        elif personality == "A 1920s Mafia Boss":
            bot_avatar = "🎩"

        elif personality == "A Highly Sarcastic Fitness Coach":
            bot_avatar = "🏋️"

        else:
            bot_avatar = "🎭"

        # Prompt Engineering
        ai_instructions = f"""
        You are acting as {personality}.

        Your personality intensity level is {intensity}/10.
        The higher the intensity, the more strongly you should
        express and maintain this personality.

        Respond to the user's message while staying completely
        in character.

        User message:
        {user_message}
        """

        # Gemini API
        with st.spinner("Connecting to the multiverse!....."):

            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=ai_instructions
            )

        # User Chat
        with st.chat_message("user"):
            st.write(user_message)

        # AI Chat
        with st.chat_message("assistant", avatar=bot_avatar):
            st.write(response.text)

    else:
        st.warning("Please type a message first")