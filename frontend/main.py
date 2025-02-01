import streamlit as st
import streamlit.components.v1 as components
from schemas import ClientRequest
from utils import generate_response, validate_input

st.set_page_config(page_title="CIA Partners - blablabla", page_icon="🌃")

st.title("SFIL 1 - CIA Partners")
col_chat, col_src, col_images = st.tabs(["Fiche Client 📂", "Recherche 🧪",  "Images 🌇"])

with col_chat:
    st.subheader("Generateur de fiches client")
    prompt = st.chat_input("Rentrez votre collectivité (exemple : Dijon)")

if prompt:
    if not validate_input(prompt):
        st.stop()

    input_obj = ClientRequest(region=prompt)

    with col_chat:
        with st.chat_message("assistant", avatar="🧑‍💻"):
            st.markdown(
                f"Votre demande de fiche client pour {prompt} a bien été reçue. Veuillez patienter quelques instants..."
            )

    # Get the streaming text, images, and URLs from your API
    stream, images, urls = generate_response(input_obj)

    with col_images:
        st.subheader("Images")
        for img, url in zip(images, urls):
            st.image(img, use_container_width=True, caption=url)

    with col_chat:
        with st.chat_message("assistant", avatar="🧑‍💻"):
            st.write_stream(stream)

    with col_src:
        st.subheader("Recherche")
        for url in urls:
            # Embed each URL in an iframe
            iframe_html = (
                f'<iframe src="{url}?embed=true" '
                'style="height: 450px; width: 100%;" frameborder="0"></iframe>'
            )
            components.html(iframe_html, height=450)