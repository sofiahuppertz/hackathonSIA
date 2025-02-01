import streamlit as st
from schemas import ClientRequest
from utils import generate_response, validate_input

st.set_page_config(
    page_title="CIA Partners -  blablabla",
    page_icon="🌃",
)

st.title("CIA Partners")

if prompt := st.chat_input("Rentrez votre collectivité (exemple : Dijon)"):

    if not validate_input(prompt):
        st.stop()  
    
    with st.chat_message("user",  avatar="🧑‍💻"):
            st.markdown(prompt)
    
    input = ClientRequest(region=prompt)

    with st.chat_message("assistant", avatar="🤖"):
        response = st.write_stream(generate_response(input))
        