from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from datetime import datetime

# Loading environment variables from .env file
load_dotenv()

# Streamlit Page Setup

st.set_page_config(page_title="GenAI Chatbot", page_icon="🤖", layout="centered")

now = datetime.now()
hour = now.hour
if hour < 12:
    greeting = "Morning"
elif hour < 18:
    greeting = "Afternoon"
else:
    greeting = "Evening"

st.markdown("<h1 style='text-align: center;'>GenAI Chatbot 🤖</h1>", unsafe_allow_html=True)

st.markdown(f"<h3 style='text-align: center; color: #FFDAB9;'>Good {greeting}!</h3>", unsafe_allow_html=True)

# Initiate Chat History

# chat_history = [] // Avoiding as it resets every time the streamlit app reruns

if "chat_history" not in st.session_state:   # Session state is a dictionary that is persisted across reruns of the Streamlit app. So this code runs only once when the app is first loaded, and initializes the chat_history key in the session state to an empty list.
    st.session_state.chat_history = [] 

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]): # When the role is "user" we will get human emoji and when the role is "assistant" we will get robot emoji. This is a built in feature of streamlit chat_message function.
        st.markdown(message["content"])

# LLM Initiate
# llm = ChatGroq(model="llm-3.1-70b-versatile", temperature=0.0)
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.0)

# Input from user
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = llm.invoke(input=[{"role": "system", "content": "You are a helpful assistant."}, *st.session_state.chat_history])

    assistant_response = response.content

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
