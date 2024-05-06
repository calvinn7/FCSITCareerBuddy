import streamlit as st
from job_recommendation import recommend_jobs
from data_preprocessing import load_job_data
from data_preprocessing import load_events
def main():
    st.title("FCSIT Career Buddy")
    st.header("Your Personal AI Compass to Navigate Your Career")
    
    # Load job data
    job_data = load_job_data('dataset/job_data.csv')
    events= load_events ('dataset/networking_events.csv')

    # Initialize conversation state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    
    # Display previous conversation
    for i in range(len(st.session_state.conversation)):
        message = st.session_state.conversation[i]
        if i % 2 == 0:  # User's message
            st.markdown(f"**You:** {message}")
        else:  # Chatbot's response
            st.markdown(f"**Chatbot:** {message}")
    
    # User input
    user_input = st.text_input("Enter your message here", key="user_input")
    
     # Check user input for different commands
    if user_input.lower() == "hello":
            response = "Hello! How can I assist you today?"
    elif "networking event" in user_input.lower() or "networking events" in user_input.lower():
            response = "Here are some upcoming networking events:"
            # Display recommended jobs in a table
            st.header("Upcoming Networking Events:")
            for _, event in events.iterrows():
                st.write(f"**Event:** {event['event']}")
                st.write(f"**Date:** {event['date']}")
                st.write(f"**Location:** {event['location']}")
                st.write(f"**Details:** {event['details']}")
                st.write("---") 
        
    elif user_input.lower() == "faq":
            response = "Here are some frequently asked questions:"
            # Logic to fetch and display FAQs
    else:
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
        
    # Update conversation state
    st.session_state.conversation.append(user_input)
    st.session_state.conversation.append("Here are some recommended jobs based on your input.")

if __name__ == "__main__":
    main()
