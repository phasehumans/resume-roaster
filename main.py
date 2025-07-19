import streamlit as st
from dotenv import load_dotenv

import io
import os
import PyPDF2
import google.generativeai as genai
import time

load_dotenv()

st.title("Resume Roaster")
# st.badge("ai resume roaster")
st.badge("ai resume roaster", icon=":material/star:", color="green")

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
genai.configure(api_key= GEMINI_API_KEY)


uploaded_file= st.file_uploader("Upload your resume here (.pdf or .txt)" , type=['pdf', 'txt'])
# job_role= st.text_input("Enter the job role that you are targeting")

options = ["Web Developer", "App Developer", "Data Scientist", "AI Engineer", "UI Designer"]
job_role = st.pills("Job Roles: ", options, selection_mode="multi")
st.markdown(f"Your selected options: {job_role}.")

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
    try:
        file_content= extract_text(uploaded_file)

        if not file_content.strip():
            st.error("file does not have any content")
            st.stop()

        prompt= f"""

You are a brutally honest, no non-sense HR expert who's been reviewing resume for decades
Roast this resume like you are on a comedy stage but still give some useful insights feedback.

Don't hold back- be sarcastic, witty and critical where need.

What would make this resume actually land a job in {job_role} for a good company.

here is the resume, go wild:

{file_content}

Make it sting and make sure to keep it in 150 words. Answer everything in Hinglish

"""

        model= genai.GenerativeModel("models/gemini-1.5-flash")
        response= model.generate_content(prompt)

        # st.markdown("## Analysis Result")
        # st.markdown(response.text)

        placeholder = st.empty()
        placeholder.progress(0, "Wait for it...")
        time.sleep(1)
        placeholder.progress(50, "Wait for it...")
        time.sleep(1)
        placeholder.progress(100, "Wait for it...")
        time.sleep(1)

        placeholder.markdown(response.text)

    except Exception as e:
        st.error(f"An error occured")


