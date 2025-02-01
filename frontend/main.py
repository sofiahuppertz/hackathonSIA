import asyncio
import time

import requests
import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from schemas import ClientRequest
from utils import generate_response, validate_input


def get_title(url):
    try:
        response = requests.get(url, timeout=5)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')
            if title_tag and title_tag.string:
                return title_tag.string.strip()
    except Exception:
        pass
    return "this page"

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
        stream, images, urls = generate_response(input_obj)

        # Append streaming response message to the chat container
        with chat_container:
            st.chat_message("assistant", avatar="🧑‍💻").write_stream(stream)

        # Display images in the "Images" tab
        with images_container:
            for img, url in zip(images, urls):
                st.image(img, use_container_width=True, caption=url)

        # Display search iframes in the "Recherche" tab
        with src_container:
            for url in urls:
                try:
                    response = requests.head(url, timeout=5)
                    x_frame = response.headers.get("X-Frame-Options", "").lower()
                except Exception:
                    x_frame = ""
                if x_frame in ["deny", "sameorigin"]:
                    page_title = get_title(url)
                    st.page_link(page=url, label=f"{page_title}", icon="🔗", use_container_width=True)
                else:

                    iframe_html = (
                        f'<iframe src="{url}?embed=true" '
                        'style="height: 450px; width: 100%;" frameborder="0"></iframe>'
                    )
                    components.html(iframe_html, height=450)
                    
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