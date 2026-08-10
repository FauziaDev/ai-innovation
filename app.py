import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

st.title("THE MULTIVERSE OF CHATBOATS")

personality = st.sidebar.selectbox(
    "Who do you want to talk to?",
    [
        "An Expert Hacker",
        "Ironman",
        "Any random personality",
        "Virat Kohli",
        "An angry Ravi Shastri",
        "A crazy Ronaldo fan",
        "Donald Trump"
    ]
)

intensity = st.sidebar.slider(
    "Intensity",
    min_value=1,
    max_value=10
)

user_message = st.text_input("Say Something:")

# -----------------------------
# TASK 5: Dynamic Avatars
# -----------------------------
if personality == "An Expert Hacker":
    bot_avatar = "💻"
elif personality == "Ironman":
    bot_avatar = "🦾"
elif personality == "Any random personality":
    bot_avatar = "🎲"
elif personality == "Virat Kohli":
    bot_avatar = "🏏"
elif personality == "An angry Ravi Shastri":
    bot_avatar = "🎙️"
elif personality == "A crazy Ronaldo fan":
    bot_avatar = "⚽"
elif personality == "Donald Trump":
    bot_avatar = "🦅"
else:
    bot_avatar = "🤖"

if st.button("SEND"):
    if user_message:

        ai_instructions = f"""
        You are acting as {personality}
        with an intensity level of {intensity}.

        Respond to the user's message while staying completely
        in character.

        User message:
        {user_message}
        """

        with st.spinner("Connecting to the multiverse!....."):

            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=ai_instructions
            )

        # -----------------------------
        # TASK 4: Chat UI elements
        # -----------------------------
        with st.chat_message("user"):
            st.write(user_message)

        with st.chat_message("assistant", avatar=bot_avatar):
            st.write(response.text)

    else:
        st.warning("Please type a message first")