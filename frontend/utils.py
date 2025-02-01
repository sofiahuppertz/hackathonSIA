import time
from typing import Iterator

import requests
import streamlit as st
from schemas import ClientRequest

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
            chunk_size = 1024
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

