import time
from typing import Iterator

import requests
import streamlit as st
from schemas import ClientRequest
from langgraph.schema import Checkpoint

def render_checkpoint(checkpoint: Checkpoint):
    nodes = [
        {
            "id": node_name,
            "label": f"{node_name}\n({checkpoint['metadata']['source']})",
            "status": checkpoint["status"]
        }
        for node_name in checkpoint["nodes"]
    ]
    
    edges = [
        {"from": edge[0], "to": edge[1]}
        for edge in checkpoint["edges"]
    ]
    
    return {
        "nodes": nodes,
        "edges": edges,
        "states": checkpoint["channel_values"]
    }



def mock_generate_response(input: ClientRequest):
    # This is a mock implementation for testing the frontend.
    content = "Ceci est un message de test généré pour le hackathon. " * 50
    images = [
        "https://i.ytimg.com/vi/6mOcNbLXhqk/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLASGRqrq-UeirbykA5j6HRCt9GEvg",
        "https://i.ytimg.com/vi/6mOcNbLXhqk/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLASGRqrq-UeirbykA5j6HRCt9GEvg",
        "https://i.ytimg.com/vi/6mOcNbLXhqk/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLASGRqrq-UeirbykA5j6HRCt9GEvg",
        "https://i.ytimg.com/vi/6mOcNbLXhqk/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLASGRqrq-UeirbykA5j6HRCt9GEvg",
    ]
    urls = [
        "https://developer.mozilla.org/es/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL",
        "https://developer.mozilla.org/es/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL",
        "https://developer.mozilla.org/es/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL",
        "https://developer.mozilla.org/es/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL",
        "https://developer.mozilla.org/es/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL",
        "https://developer.mozilla.org/es/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL",
        "https://developer.mozilla.org/es/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL",
        "https://developer.mozilla.org/es/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL",    
    ]

    def stream():
        chunk_size = 2000
        for i in range(0, len(content), chunk_size):
            yield content[i:i+chunk_size]
            time.sleep(0.05)

    return stream(), images, urls

def generate_response(input: ClientRequest):
    try:
        response = requests.post(
            "http://localhost:8000/gen_client_sheet",
            json=input.to_json()
        )
        data = response.json()
        images = data.get("images", [])
        urls = data.get("urls", [])
        content = data.get("content", "")

        def stream():
            chunk_size = 25
            for i in range(0, len(content), chunk_size):
                yield content[i:i+chunk_size]
                time.sleep(0.05)

        return stream(), images, urls
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the backend: {e}")
        return iter([]), [], []


def validate_input(prompt: str) -> bool:
    if not prompt.strip():
        st.warning("Please enter a non-empty message.")
        return False
    if len(prompt) > 100:
        st.warning("Your message is too long. Please limit it to 100 characters.")
        return False
    return True

