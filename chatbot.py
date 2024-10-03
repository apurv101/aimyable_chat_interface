import streamlit as st
from openai import OpenAI

client = OpenAI(api_key='')

# Set your OpenAI API key

# App layout and styling
st.set_page_config(page_title="Chatbot with History", layout="wide")
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

# Function to get response from OpenAI GPT
def get_openai_response(user_input):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # You can change this to "gpt-4" if you have access to GPT-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},  # Optional system message for context
            {"role": "user", "content": user_input}
        ])
        message = response.choices[0].message.content.strip()
        return message
    except Exception as e:
        return f"Error: {e}"

# Sidebar for chat history
st.sidebar.title("Chat History")

if st.session_state.history:
    for chat in st.session_state.history:
        st.sidebar.markdown(
            f"<div class='chat-message user-message'>{chat['user']}</div><div class='chat-message bot-message'>{chat['bot']}</div>",
            unsafe_allow_html=True,
        )

# Main chat interface
st.title("AI Chatbot")

with st.form(key="chat_form"):
    user_input = st.text_input("You:", key="user_input", placeholder="Type your message here...")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    with st.spinner("Thinking..."):
        # Get response from OpenAI
        bot_response = get_openai_response(user_input)

        # Save the chat to history
        chat_entry = {
            "user": user_input,
            "bot": bot_response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.history.append(chat_entry)

        # Display chat
        st.markdown(f"<div class='chat-message user-message'>{user_input}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-message bot-message'>{bot_response}</div>", unsafe_allow_html=True)

# Clear chat history button
if st.sidebar.button("Clear History"):
    st.session_state.history = []
    st.experimental_rerun()