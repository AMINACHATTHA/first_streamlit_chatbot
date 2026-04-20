import streamlit as st
from groq import Groq
import time

# Page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Groq client (from Hugging Face Secrets)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Title
st.title("🤖 AI Chatbot using Groq + Streamlit")
st.caption("ChatGPT-style chatbot powered by Llama 3.1")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Assistant response area
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            time.sleep(0.5)

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    *st.session_state.messages
                ]
            )

            reply = response.choices[0].message.content

        # ✨ Typing animation
        placeholder = st.empty()
        typed_text = ""

        for word in reply.split():
            typed_text += word + " "
            placeholder.markdown(typed_text)
            time.sleep(0.03)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})

  