import streamlit as st
from job_recommendation import recommend_jobs
from data_preprocessing import load_job_data
from data_preprocessing import load_events

st.set_page_config(page_title="FCSIT Career Buddy", page_icon=":technologist:", layout="wide")

def on_click_callback():
    conversation = st.session_state.conversation
    st.session_state.history.append(conversation)

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
initialize_session_state()

def main():
    # -- header --- 
    st.title ("Welcome to the FCSIT Career Bot :wave:")
    st.subheader ("Your personal AI-powered career companion ")
    st.write ("Check out our GitHub repo [here](https://github.com/calvinn7/FCSITCareerBuddy)")

    # Clear conversation history at the beginning of each session
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    else:
        st.session_state.conversation.clear()

    # Load job data
    job_data = load_job_data('dataset/job_data.csv')
    events= load_events ('dataset/networking_events.csv')
    
    # Display previous conversation
    for i in range(len(st.session_state.conversation)):
        message = st.session_state.conversation[i]
        if i % 2 == 0:  # User's message
            st.markdown(f"**You:** {message}")
        else:  # Chatbot's response
            st.markdown(f"**Chatbot:** {message}")
    
    # User input
    user_input = st.text_input("Enter your message here", key="user_input")

    chat_placeholder = st.container()
    prompt_placheholder = st.form("chat-form")
    credit_card_placeholder = st.empty()

    # UI chat

    with chat_placeholder:
        for chat in st.session_state.history:
            st.markdown(chat)

    with prompt_placheholder:
        st.markdown("**Chat** - _press Enter to Submit_")
        cols = st.columns((6, 1))
        user_input = cols[0].text_input(
            "Chat",
            value="Hello bot",
            label_visibility="collapsed",
            key="conversation"
        )
        cols[1].form_submit_button(
            "Submit",
            type="primary",
            on_click=on_click_callback,
        )

    # Check user input for different commands
    if user_input.lower() == "hello":
        response = "Hello! How can I assist you today?"
        st.write(response)
    elif "networking event" in user_input.lower() or "networking events" in user_input.lower():
        response = "Here are some upcoming networking events:"
        # Display networking events in a table
        st.header("Upcoming Networking Events:")
        for _, event in events.iterrows():
            st.write(f"**Event:** {event['event']}")
            st.write(f"**Date:** {event['date']}")
            st.write(f"**Location:** {event['location']}")
            st.write(f"**Details:** {event['details']}")
            st.write("---")
    elif user_input.lower() == "faq":
        response = "Here are some frequently asked questions:"
        st.write(response)
        # Logic to fetch and display FAQs
    elif user_input.strip():  # Check if user input is not empty or only whitespace
        # Recommend jobs based on user input
        recommended_jobs = recommend_jobs(user_input, job_data)
        
        # Display recommended jobs in a table
        st.header("Recommended jobs based on your input:")
        for _, job in recommended_jobs.iterrows():
            st.write(f"**Job Title:** {job['JobTitle']}")
            st.write(f"**Company:** {job['company']}")
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Salary:** {job['salary']}")
            st.write(f"**Date Posted:** {job['date_posted']}")
            st.write(f"**Job URL:** [{job['job_url']}]({job['job_url']})")
            st.write(f"**Company rating:** {job['overall_rating']} from {job['num_ratings']} reviews")
            st.write("---")
    else:
        response = "I'm sorry, I didn't understand that. Can you please rephrase or ask something else?"
        st.write(response)

    # Update conversation state
    st.session_state.conversation.append(user_input)
    st.session_state.conversation.append(response)

if __name__ == "__main__":
    main()
