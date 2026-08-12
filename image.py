import streamlit as st
import requests
import random
from urllib.parse import quote
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide"
)
st.title("🎨 AI Image Studio")
st.write("Create amazing AI-generated images with your imagination!")
# Surprise Prompts
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo at night",
    "A futuristic city floating above the clouds",
    "A magical forest with glowing trees and tiny dragons",
    "A robot exploring an ancient underwater civilization"
]
# Sidebar Settings
st.sidebar.header("⚙️ Image Settings")
art_style = st.sidebar.selectbox(
    "🎨 Choose Art Style",
    [
        "Digital Art",
        "Photorealistic",
        "Anime",
        "Cinematic",
        "3D Render",
        "Fantasy Art"
    ]
)
width = st.sidebar.slider(
    "📏 Width",
    min_value=256,
    max_value=1024,
    value=768,
    step=64
)
height = st.sidebar.slider(
    "📐 Height",
    min_value=256,
    max_value=1024,
    value=768,
    step=64
)
# Task 3: Magic Enhance
magic_enhance = st.sidebar.checkbox(
    "✨ Enable Magic Enhance"
)
# Prompt Input
user_prompt = st.text_input(
    "💭 Enter your image prompt",
    placeholder="Example: Ronaldo winning the World Cup with Portugal"
)
# Buttons
col1, col2 = st.columns(2)
with col1:
    generate_button = st.button(
        "🚀 Generate Image",
        use_container_width=True
    )
with col2:
    surprise_button = st.button(
        "🎲 Surprise Me!",
        use_container_width=True
    )
# Image Generation Function
def generate_image(prompt):
    
    full_prompt = f"{prompt}, {art_style}"
    # Task 3: Magic Enhance
    if magic_enhance:
        full_prompt += (
            ", masterpiece, 8k resolution, highly detailed, "
            "trending on artstation, unreal engine 5 render"
        )
    # Encode prompt safely for URL
    encoded_prompt = quote(full_prompt)
    # Task 1: Width and Height URL Parameters
    url = (
        f"https://image.pollinations.ai/prompt/"
        f"{encoded_prompt}?width={width}&height={height}"
    )
    st.info("🎨 Generating your image...")
    response = requests.get(url)
    if response.status_code == 200:
        st.image(
            response.content,
            caption=f"{art_style} | {width} × {height}"
        )
        # Task 2: Correct file extension + dynamic filename
        st.download_button(
            label="⬇️ Download Image",
            data=response.content,
            file_name=f"{art_style}_image.png",
            mime="image/png"
        )
    else:
        st.error("❌ Error generating image. Please try again.")
if generate_button:
    if user_prompt.strip():
        generate_image(user_prompt)
    else:
        st.warning("⚠️ Please enter a prompt first.")
# Task 4: Surprise Me
if surprise_button:
    random_prompt = random.choice(surprise_prompts)
    st.success(f"🎲 Surprise Prompt: {random_prompt}")
    generate_image(random_prompt)