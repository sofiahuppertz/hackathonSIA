import time
import requests
import streamlit as st
from schemas import ClientRequest
from utils import validate_input, generate_response

st.set_page_config(page_title="CIA Partners - blablabla", page_icon="🌃")

# Define two columns: left for images, right for the chat
col_chat, col_images = st.columns([4, 1])

with col_chat:
    st.title("CIA Partners")
    prompt = st.chat_input("Rentrez votre collectivité (exemple : Dijon)")

if prompt:
    if not validate_input(prompt):
        st.stop()

    input_obj = ClientRequest(region=prompt)

    with col_chat:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

    # Get the streaming text, images and URLs from your API
    stream, images, urls = generate_response(input_obj)

    # Update the left column with images
    with col_images:
        st.subheader("Images")
        for img, url in zip(images, urls):
            st.image(img, caption=url)

    # Display the assistant's streaming response in the chat area
    with col_chat:
        with st.chat_message("assistant", avatar="🤖"):
            st.write_stream(stream)