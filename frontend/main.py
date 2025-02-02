import asyncio
import time

import requests
import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from generate_pdf import generate_pdf
from schemas import ClientRequest
from utils import generate_response, validate_input

st.set_page_config(page_title="Sfil 1", page_icon="🌃")


col_chat, col_src, col_images = st.tabs(["Fiche Client 📂", "Recherche 🧪", "Images 🌇"])

with col_src:
    src_container = st.container(height=620, border=False)

with col_images:
    images_container = st.container(height=620, border=False)

with col_chat:
    st.subheader(":grey[_Generateur de fiches client_] 📤")
    
    # Create a container for all chat messages (displayed above the input)
    chat_container = st.container(height=500, border=False)
    
    # Chat input appears below the chat messages container
    if prompt := st.chat_input("Rentrez une collectivité (Exemple: Dijon)"):
        
        if not validate_input(prompt):
            st.stop()

        input_obj = ClientRequest(region=prompt)

        # Add initial assistant message to the chat container
        with chat_container:
            st.chat_message("assistant", avatar="🧑‍💻").markdown(
                f"Votre demande de fiche client pour {prompt} a bien été reçue. Veuillez patienter quelques instants..."
            )

        # Get the streaming text, images, and URLs from your API
        start_time = time.time()
        stream, section_images, section_urls, content_for_pdf = generate_response(input_obj)

        elapsed_time = time.time() - start_time
        elapsed_seconds = round(elapsed_time, 2)  # Round to 2 decimal places

        # Send message with elapsed time
        with chat_container:
            st.chat_message("assistant", avatar="🧑‍💻").markdown(
                f"Votre demande de fiche client pour {prompt} a été traitée en {elapsed_seconds} secondes."
            )
        # Append streaming response message to the chat container
        with chat_container:
            st.chat_message("assistant", avatar="🧑‍💻").write_stream(stream)


        with images_container:
            for sec in section_images:
                st.subheader(f"{sec['section']}")
                for img in sec['images']:
                    st.image(img, width=300, caption=img)

        with src_container:
            for sec in section_urls:
                st.subheader(f"{sec['section']}")
                for url in sec['urls']:
                    st.page_link(page=url, label=url, icon="🔗", use_container_width=True)


        with chat_container:
            pdf_buffer = generate_pdf(content_for_pdf, section_images, section_urls)
            st.download_button(
                    label="Télécharger la fiche client en PDF",
                    data=pdf_buffer,
                    file_name="fiche_client.pdf",
                    mime="application/pdf",
                    icon="✅"
            )
            
logos = [
    "https://sfil.fr/wp-content/uploads/2023/02/Sfil-Logo.png",
    "https://d2q79iu7y748jz.cloudfront.net/s/_squarelogo/256x256/e84f3d078c09d40567c795fb4649f42d",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/42_Logo.svg/langfr-280px-42_Logo.svg.png"
]

async def cycle_logos():
    while True:
        for logo in logos:
            st.logo(image=logo, size="large")
            await asyncio.sleep(5)

# Run the async function in the background
asyncio.run(cycle_logos())