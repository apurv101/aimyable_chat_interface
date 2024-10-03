import streamlit as st
from datetime import datetime
from langchain_logic import get_lll_steps, store_message, retrieve_relevant_messages

# App layout and styling
st.set_page_config(page_title="Chatbot with History and LangChain", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #2b303b;
        color: white;
    }
    .chat-message {
        background-color: #e5e5e5;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        font-size: 16px;
    }
    .user-message {
        background-color: #3b9a9c;
        color: white;
    }
    .bot-message {
        background-color: #ffffff;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar for chat history
st.sidebar.title("Chat History")

if st.session_state.history:
    for chat in st.session_state.history:
        st.sidebar.markdown(
            f"<div class='chat-message user-message'>{chat['user']}</div><div class='chat-message bot-message'>{chat['bot']}</div>",
            unsafe_allow_html=True,
        )

# Main chat interface
st.title("AI Chatbot with Task Breakdown")

# Chat form for user input
with st.form(key="chat_form"):
    user_input = st.text_input("You:", key="user_input", placeholder="Type your message here...")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    with st.spinner("Thinking..."):
        # Retrieve relevant conversation history from Chroma
        relevant_history = retrieve_relevant_messages(user_input)

        # Call the function from langchain_logic.py to get the low-level steps
        lll_steps = get_lll_steps(user_input, relevant_history)

        # Display the low-level steps
        bot_response = f"Low-Level Language (LLL) Steps:\n{lll_steps}"

        # Save the chat to history
        chat_entry = {
            "user": user_input,
            "bot": bot_response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.history.append(chat_entry)

        # Store the chat in the vector database (Chroma)
        store_message(user_input, bot_response)

        # Display the conversation
        st.markdown(f"<div class='chat-message user-message'>{user_input}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-message bot-message'>{bot_response}</div>", unsafe_allow_html=True)

# Clear chat history button
if st.sidebar.button("Clear History"):
    st.session_state.history = []
    st.experimental_rerun()
