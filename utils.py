import base64
import math
import os
import streamlit as st
import asyncio

# Set global variables
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data(show_spinner=False)
def get_local_img(file_path: str) -> str:
    # Load a byte image and return its base64 encoded string
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        st.error(f"Image file not found at path: {file_path}")
        return ""

def get_star_rating(rating):
    if not math.isnan(rating):  # Check if rating is not NaN
        filled_stars = '⭐' * round(rating)
        empty_stars = '⭒' * (5 - round(rating))
        return f"{filled_stars}{empty_stars}"
    else:
        return "Rating not available"  # or any other appropriate handling for NaN values

@st.cache_data(show_spinner=False)
def get_css() -> str:
    # Construct relative file path
    css_file_path = os.path.join(ROOT_DIR, "FCSITCareerBuddy", "style.css")

    # Debugging: print constructed file path
    st.write("Constructed CSS file path:", css_file_path)

    # Read CSS code from style.css file
    try:
        with open(css_file_path, "r") as f:
            return f"<style>{f.read()}</style>"
    except FileNotFoundError:
        st.error(f"CSS file not found at path: {css_file_path}")
        return ""

def clear_chat():
    st.session_state.LOG = ["Hello! How can I assist you today?"]
    st.session_state.MEMORY = [{'role': "system", 'content': "Hello! How can I assist you today?"}]
    st.session_state.SHOW_FEEDBACK_FORM = False
    st.session_state.stop = False

def get_chat_message(
        contents: str = "",
        align: str = "left"
) -> str:
    # Formats the message in a chat fashion (user right, reply left)
    div_class = "AI-line"
    color = "rgb(54, 65, 85)"
    file_path = os.path.join(ROOT_DIR, "FCSITCareerBuddy", "assets", "bot.png")
    src = f"data:image/gif;base64,{get_local_img(file_path)}"

    if align == "right":
        div_class = "human-line"
        color = "rgb(51, 78, 255)"
        if "USER" in st.session_state:
            src = st.session_state.USER.avatar_url
        else:
            file_path = os.path.join(ROOT_DIR, "FCSITCareerBuddy", "assets", "user_icon.png")
            src = f"data:image/gif;base64,{get_local_img(file_path)}"
    icon_code = f"<img class='chat-icon' src='{src}' width=32 height=32 alt='avatar'>"
    formatted_contents = f"""
        <div class="{div_class}">
            {icon_code}
            <div class="chat-bubble" style="background: {color}; color: white;">
            &#8203;{contents}
        </div>
        """
    return formatted_contents

async def type_reply(reply_box, message):
    typing_indicator = "<div class='typing-indicator'>Career Buddy is typing...</div>"
    reply_box.markdown(get_chat_message(typing_indicator), unsafe_allow_html=True)
    typed_message = ""
    for char in message:
        typed_message += char
        reply_box.markdown(get_chat_message(typed_message), unsafe_allow_html=True)
        await asyncio.sleep(0.010)  # Increased sleep time for better visibility
    reply_box.markdown(get_chat_message(typed_message), unsafe_allow_html=True)
