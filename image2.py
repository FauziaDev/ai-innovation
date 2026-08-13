import streamlit as st
import requests
import json
import io
import os
from urllib.parse import quote
from dotenv import load_dotenv
from google import genai
from google.genai import types
from gtts import gTTS

st.set_page_config(page_title="AI Visual Novel", page_icon="🎭", layout="wide")

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@st.cache_resource
def get_gemini_client():
    if not GEMINI_API_KEY:
        return None
    return genai.Client(api_key=GEMINI_API_KEY)

client = get_gemini_client()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = None
if "story_started" not in st.session_state:
    st.session_state.story_started = False

st.sidebar.title("📖 Story Settings")

genre = st.sidebar.selectbox(
    "🎭 Story Genre",
    ["Fantasy", "Science Fiction", "Mystery", "Horror", "Adventure", "Romance"]
)

art_style = st.sidebar.selectbox(
    "🎨 Art Style",
    ["Anime", "Photorealistic", "3D Render", "Watercolor",
     "Comic Book", "Vintage Victorian", "Digital Art"]
)

st.title("🎭 AI Visual Novel")
st.caption("Choose your path. AI creates the story, visuals, choices and narration.")

if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY not found. Please add it to your .env file.")
    st.stop()

system_prompt = f"""
You are the director of an interactive visual novel.

Genre: {genre}
Art Style: {art_style}

Return ONLY a valid JSON object. Do not use markdown or ```json.

The JSON MUST contain exactly these keys:
{{
    "story_text": "A cinematic narrative paragraph.",
    "image_prompt": "A highly detailed prompt for an AI image generator.",
    "options": [
        "First possible action",
        "Second possible action",
        "Third possible action"
    ]
}}

Rules:
1. story_text must be an engaging cinematic narrative.
2. image_prompt must describe characters, environment, lighting, mood, camera angle, objects and visual details in {art_style} style.
3. options must contain 2 or 3 distinct choices.
4. Choices must meaningfully change what happens next.
5. Keep the story suitable for a general audience.
6. Return valid JSON only.
"""

def create_chat():
    try:
        return client.chats.create(
            model="gemini-3.6-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            )
        )
    except Exception as e:
        st.error(f"❌ Gemini initialization failed:\n\n{e}")
        return None

def parse_story(response_text):
    try:
        response_text = response_text.strip()

        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "")
            response_text = response_text.replace("```", "").strip()

        story_data = json.loads(response_text)

        for key in ["story_text", "image_prompt", "options"]:
            if key not in story_data:
                raise ValueError(f"Missing JSON key: {key}")

        if not isinstance(story_data["options"], list):
            raise ValueError("options must be a list.")

        if len(story_data["options"]) < 2:
            raise ValueError("At least 2 choices are required.")

        return story_data

    except json.JSONDecodeError as e:
        st.error(f"❌ Gemini returned invalid JSON:\n\n{e}")
        st.code(response_text, language="text")
        return None
    except Exception as e:
        st.error(f"❌ JSON parsing error:\n\n{e}")
        return None

def generate_image(image_prompt):
    try:
        encoded_prompt = quote(image_prompt)
        url = (
            "https://image.pollinations.ai/prompt/"
            f"{encoded_prompt}?width=768&height=768"
        )

        response = requests.get(url, timeout=40)

        if response.status_code == 200:
            return response.content

        raise Exception(f"Pollinations returned status {response.status_code}")

    except Exception as e:
        st.toast("Image server is busy, skipping visual...")
        st.warning(f"Image generation failed: {e}")
        return None

def generate_audio(story_text):
    try:
        audio_buffer = io.BytesIO()

        tts = gTTS(
            text=story_text,
            lang="en",
            slow=False
        )

        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return audio_buffer

    except Exception as e:
        st.toast("Narration unavailable, continuing without audio...")
        st.warning(f"TTS error: {e}")
        return None

def generate_scene(user_choice=None):
    try:
        if st.session_state.gemini_chat is None:
            st.session_state.gemini_chat = create_chat()

            if st.session_state.gemini_chat is None:
                return False

            first_prompt = """
Start a brand-new interactive visual novel.
Introduce the main character, the world and the initial conflict.
End the scene with 2 or 3 meaningful choices.
"""

            response = st.session_state.gemini_chat.send_message(first_prompt)
        else:
            response = st.session_state.gemini_chat.send_message(user_choice)

        story_data = parse_story(response.text)

        if story_data is None:
            return False

        image_data = generate_image(story_data["image_prompt"])
        audio_data = generate_audio(story_data["story_text"])

        st.session_state.messages.append({
            "story_text": story_data["story_text"],
            "image_prompt": story_data["image_prompt"],
            "options": story_data["options"],
            "image": image_data,
            "audio": audio_data
        })

        st.session_state.story_started = True
        return True

    except Exception as e:
        st.error(f"❌ Story generation failed:\n\n{e}")
        return False

if not st.session_state.story_started:
    st.write("Choose your genre and art style, then begin your adventure.")

    if st.button("🚀 Start Adventure", use_container_width=True):
        with st.spinner("🎬 Director is creating your first scene..."):
            success = generate_scene()

        if success:
            st.rerun()

for index, scene in enumerate(st.session_state.messages):
    st.divider()
    st.subheader(f"🎬 Scene {index + 1}")

    if scene["image"]:
        st.image(scene["image"], use_container_width=True)

    st.markdown(
        f"### 📖 Story\n\n{scene['story_text']}"
    )

    if scene["audio"]:
        st.audio(scene["audio"], format="audio/mp3")

    if index == len(st.session_state.messages) - 1:
        st.markdown("### 🤔 What will you do?")

        for option_index, option in enumerate(scene["options"]):
            if st.button(
                f"👉 {option}",
                key=f"choice_{index}_{option_index}",
                use_container_width=True
            ):
                with st.spinner("✨ The story continues..."):
                    success = generate_scene(option)

                if success:
                    st.rerun()

if st.session_state.story_started:
    st.sidebar.divider()

    if st.sidebar.button("🔄 Restart Story", use_container_width=True):
        st.session_state.messages = []
        st.session_state.gemini_chat = None
        st.session_state.story_started = False
        st.rerun()