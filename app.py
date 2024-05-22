import base64
import os.path
import asyncio
import traceback
import random
import streamlit as st
from models.job_recommendation import recommend_jobs
from data_preprocessing import load_job_data
from data_preprocessing import load_events
from data_preprocessing import preprocess_text
from intent_classification import classify_intent

# Set global variables
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False

st.set_page_config(page_title="FCSIT Career Buddy", page_icon=":technologist:", layout="wide")

@st.cache_data(show_spinner=False)
def get_local_img(file_path: str) -> str:
    # Load a byte image and return its base64 encoded string
    return base64.b64encode(open(file_path, "rb").read()).decode("utf-8")

@st.cache_data(show_spinner=False)
def get_css() -> str:

    # Read CSS code from style.css file
    with open(os.path.join(ROOT_DIR, "FCSITCareerBuddy" ,  "style.css"), "r") as f:
        return f"<style>{f.read()}</style>"

def get_chat_message(
        contents: str = "",
        align: str = "left"
) -> str:

    # Formats the message in an chat fashion (user right, reply left)
    div_class = "AI-line"
    color = "rgb(54, 65, 85)"
    file_path = os.path.join(ROOT_DIR, "FCSITCareerBuddy" , "assets", "bot.png")
    src = f"data:image/gif;base64,{get_local_img(file_path)}"

    if align == "right":
        div_class = "human-line"
        color = "rgb(51, 78, 255)"
        if "USER" in st.session_state:
            src = st.session_state.USER.avatar_url
        else:
            file_path = os.path.join(ROOT_DIR, "FCSITCareerBuddy" ,"assets", "user_icon.png")
            src = f"data:image/gif;base64,{get_local_img(file_path)}"
    icon_code = f"<img class='chat-icon' src='{src}' width=32 height=32 alt='avatar'>"
    formatted_contents = f"""
        <div class="{div_class}">
            {icon_code}
            <div class="chat-bubble" style="background: {color}; color: white;">
            &#8203;{contents}
            </div>
        </div>
        """
    return formatted_contents

greet_responses = [
    "Hi there, I am your career buddy! How can I help you today?",
    "Hello! How can I assist you today?",
    "Hi! What can I do for you today?",
    "Greetings! How can I be of service today?"
]

bye_responses = [
    "Thank you for using career buddy! See you soon.",
    "Goodbye! Have a great day!",
    "See you later! Take care.",
    "Farewell! Hope to assist you again soon."
]

#when user inputs
async def main(human_prompt: str) -> dict:

    res = {'status': 0, 'message': "Success"}
    try:

        # Update both chat log and the model memory
        st.session_state.LOG.append(f"Human: {human_prompt}")
        st.session_state.MEMORY.append({'role': "user", 'content': human_prompt})

        # Clear the input box after human_prompt is used
        prompt_box.empty()

        # Load job data
        job_data = load_job_data('dataset/preprocessed_job_data.csv')
        events= load_events ('dataset/networking_events.csv')

        with chat_box:
            #Write the latest human message first
            line = st.session_state.LOG[-1]
            contents = line.split("Human: ")[1]
            st.markdown(get_chat_message(contents, align="right"), unsafe_allow_html=True)

            reply_box = st.empty()
            reply_box.markdown(get_chat_message(), unsafe_allow_html=True)

            reply_text = ""

            preprocessed_input = preprocess_text(human_prompt)

            # Classify intent
            intent = classify_intent(preprocessed_input)

            if intent == "faq":
                reply_text = "Here are some frequently asked questions:"

                # Logic to fetch and display FAQs
                # TO BE INSERTED THE NLP MODEL

            elif intent == "networking_event":
                reply_text = "Here are some upcoming networking events:<br><br>"

                # Display networking events in a table
                # TO BE INSERTED THE NLP MODEL
                st.header("Upcoming Networking Events:")
                for _, event in events.iterrows():
                    reply_text += f"""
                                        Event: {event['event']}<br>
                                        Date: {event['date']}<br>
                                        Location: {event['location']}<br>
                                        Details: {event['details']}<br>
                                        -----------------------------------------------------------------------------------<br>"""

            

            elif intent == "job_recommendation": # Check if user input is not empty or only whitespace
                # Recommend jobs based on user input
                recommended_jobs = recommend_jobs(preprocessed_input, job_data)

                #Display recommended jobs in a table

                reply_text = "Here are some personalised jobs for you: <br><br>"

                for _, job in recommended_jobs.iterrows():
                    reply_text += f""" 
                                        Job Title: {job['JobTitle']}<br>
                                        Company: {job['company']}<br>
                                        Location: {job['location']}<br>
                                        Salary: {job['salary']}<br>
                                        Date Posted: {job['date_posted']}<br>
                                        Find out more about the job <a href="{job['job_url']}" target="_blank">here </a><br>
                                        Company rating: {job['overall_rating']} from {job['num_ratings']} reviews<br>
                                        Learn more about the company culture <a href="{job['review_url']}" target="_blank"> here.</a><br>                                        
                                        -----------------------------------------------------------------------------------<br>"""
            elif intent == 'greet':
                reply_text = random.choice(greet_responses)
            
            elif intent == 'bye':
                reply_text = random.choice(bye_responses)

            # Render the reply as chat reply
            b64str = None
            message = f"{reply_text}"
            if b64str:
                message += f"""<br><img src="data:image/png;base64,{b64str}" width=256 height=256>"""
            reply_box.markdown(get_chat_message(message), unsafe_allow_html=True)

            # Update the chat log and the model memory
            st.session_state.LOG.append(f"AI: {message}")
            st.session_state.MEMORY.append({'role': "assistant", 'content': reply_text})

    except:
        res['status'] = 2
        res['message'] = traceback.format_exc()

    return res

### INITIALIZE AND LOAD ###

### MAIN STREAMLIT UI STARTS HERE ###

# Define main layout
gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, rgb(51, 78, 255), rgb(197, 153, 233));
    background: linear-gradient(to right, rgb(51, 78, 255), rgb(197, 153, 233));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 3em;
}
</style>
<div class="gradient-text">Welcome to the FCSIT Career Buddy</div>
"""
st.markdown(gradient_text_html, unsafe_allow_html=True)
st.subheader ("Your personal AI-powered career companion ")
chat_box = st.container()
st.write("")
prompt_box = st.empty()

#sidebar
with open("sidebar.md", "r") as sidebar_file:
    sidebar_content = sidebar_file.read()

with open("style.css", "r") as styles_file:
    styles_content = styles_file.read()

st.sidebar.markdown(sidebar_content)
st.write(styles_content, unsafe_allow_html=True)

# Load CSS code
st.markdown(get_css(), unsafe_allow_html=True)

# Initialize/maintain a chat log and chat memory in Streamlit's session state
if "MEMORY" not in st.session_state:

    INITIAL_PROMPT = "Hello! How can I assist you today?"
    st.session_state.LOG = [INITIAL_PROMPT]
    st.session_state.LOG.append(f"AI: {INITIAL_PROMPT}")
    st.session_state.MEMORY = [{'role': "system", 'content': INITIAL_PROMPT}]

# Render chat history so far
with chat_box:
    for line in st.session_state.LOG[1:]:
        # For AI response
        if line.startswith("AI: "):
            contents = line.split("AI: ")[1]
            st.markdown(get_chat_message(contents), unsafe_allow_html=True)

        # For human prompts
        if line.startswith("Human: "):
            contents = line.split("Human: ")[1]
            st.markdown(get_chat_message(contents, align="right"), unsafe_allow_html=True)

# Define an input box for human prompts
with prompt_box:
    human_prompt = st.chat_input("Ask me anything about FCSIT career", key=f"text_input_{len(st.session_state.LOG)}")

#Gate the subsequent chatbot response to only when the user has entered a prompt
if human_prompt is not None and len(human_prompt) > 0:
    run_res = asyncio.run(main(human_prompt))
    if run_res['status'] == 0 and not DEBUG:
        st.rerun()

    else:
        if run_res['status'] != 0:
            st.error(run_res['message'])
        with prompt_box:
            if st.button("Show text input field"):
                st.rerun()

