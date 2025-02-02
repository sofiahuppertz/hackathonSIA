import os
from io import BytesIO

import requests
from fpdf import FPDF


def generate_pdf(content: str, section_images, section_urls):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    font_path = "DejaVuSans.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError("DejaVuSans.ttf not found. Please download and place it in the working directory.")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.set_text_color(0, 0, 0)
    
    # Write the text content
    pdf.multi_cell(0, 10, content)

    # Add a section for images
    for sec in section_images:
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Images for {sec['section']}", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        for img_url in sec['images']:
            try:
                response = requests.get(img_url)
                if response.status_code == 200:
                    img_data = BytesIO(response.content)
                    # Insert image with a fixed width; adjust as needed
                    pdf.image(img_data, w=100)
                    pdf.ln(10)
            except Exception as e:
                pdf.cell(0, 10, f"Error loading image: {img_url}", ln=True)

    # Add a section for URLs
    for sec in section_urls:
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Links for {sec['section']}", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        for url in sec['urls']:
            pdf.write(10, url, link=url)
            pdf.ln(10)

    # Get PDF output as BytesIO
    pdf_bytes = pdf.output(dest="S")
    pdf_buffer = BytesIO(pdf_bytes)
    pdf_buffer.seek(0)
    return pdf_buffer