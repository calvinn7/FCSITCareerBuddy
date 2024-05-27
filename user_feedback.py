import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def feedback():
    # Display title & description
    st.title("User Form Evaluation")
    st.markdown("We love to hear from you !")

    # Establishing a Google Sheet Connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fetch existing data
    existed_data = conn.read(worksheet="Users", usecols=list(range(6)), ttl=5)
    existed_data = existed_data.dropna(how="all")

    # Initialize the options to choose from
    year_category = [1, 2, 3, 4, 5]
    radio_options = [1, 2, 3, 4, 5]

    # Create User Form
    with st.form(key="user_form"):
        username       = st.text_input(label="Name*")
        year_of_study  = st.selectbox(label="Year of Study*", options=year_category, index=None)

        # like how helpful, how precise, is there any bug(later will put text box),
        # anything need to improve for the chatbot

        st.write("From 1 (Very not helpful) to 5 (Very Helpful)")

        helpfulness    = st.radio(label="How would you like to rate our chatbot helpfulness?", options=radio_options)
        precision      = st.radio(label="How precise does the chatbot able to answer the questions?", options=radio_options)
        bug_text       = st.text_input(label="Is there any bug that you have encounter in our chatbot?")
        suggestion     = st.text_input(label="We would like to hear your suggestion to improve our chatbot.")

        # Mark Mandatory Fields
        st.markdown("***required**")

        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            # Check if all mandatory is filled

            if not username or not year_of_study:
                st.warning("Ensure all the mandatory fields are filled.")
                st.stop()
            elif existed_data["Users"].str.contains(username).any():
                st.warning("This user has already exists.")
                st.stop()
            else:
                # Create new user and data
                user_data = pd.DataFrame(
                    [
                        {
                            "Users": username,
                            "Year Category": year_of_study,
                            "Precision": precision,
                            "Helpfulness": helpfulness,
                            "Bug Encountered" :bug_text,
                            "Suggestion" :suggestion
                        }
                    ]
                )

                # Add data into existed data
                update_data = pd.concat([existed_data, user_data], ignore_index=True)

                # Update Google Sheet
                conn.update(worksheet="Users", data=update_data)
                st.success("The details has been submitted! Thank You!")



            st.write("Thank you for your feedback")

            # Reset chat history and other states for a new conversation
            st.session_state.LOG = ["Hello! How can I assist you today?"]
            st.session_state.MEMORY = [{'role': "system", 'content': "Hello! How can I assist you today?"}]
            st.session_state.SHOW_FEEDBACK_FORM = False


if __name__ == '__main__':
    feedback()