import streamlit as st
import uuid

from classes import ChatMessage, UserInput
from utils import display_chat_message, generate_response, validate_input, choose_random_emoji


st.set_page_config(
    page_title="Motibot - Trainer Specialist 🏋🏼‍♂️🏃🏼‍♀️",
    page_icon="💪",
)

st.title("Motibot - Trainer Specialist 🏋🏼‍♂️🏃🏼‍♀️")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "talk_id" not in st.session_state:
    st.session_state.talk_id = str(uuid.uuid4())

display_chat_message(st.session_state.messages)

if prompt := st.chat_input("Hey Motibot, can you help me with my fitness plan?"):

    if not validate_input(prompt):
        st.stop()
    
    user_message = [ChatMessage(role="user", avatar="🧑‍💻", content=prompt)]
    display_chat_message(user_message)
    st.session_state.messages.append(user_message[0])
    
    input = UserInput(message=prompt, talk_id=st.session_state.talk_id)

    avatar = choose_random_emoji()
    with st.chat_message("assistant", avatar=avatar):
        response = st.write_stream(generate_response(input))
        
    st.session_state.messages.append(ChatMessage(role="assistant", avatar=avatar, content=response))