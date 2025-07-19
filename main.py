import streamlit as st
from dotenv import load_dotenv

import io
import os
import PyPDF2


load_dotenv()

st.title("AI Resume Roaster")
st.badge("Chaitanya Sonawane")

uploaded_file= st.file_uploader("Upload your resume her (PDF & txt)" , type=['pdf', 'txt'])
st.text_input("Enter the job role that you are targeting")

analyze= st.button("Analyze Resume")
# print(analyze) --> T/F


def extract_text_from_pdf(file_bytes):
    reader= PyPDF2.PdfReader(file_bytes)

    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text(uploaded_file):
    file_type= uploaded_file.type

    if file_type == "application/pdf":
        with io.BytesIO(uploaded_file.read()) as file_bytes:
            return extract_text_from_pdf(file_bytes)
    elif file_type == "text/plain":
        return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    pass