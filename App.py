import streamlit as st
import google.generativeai as genai
import PyPDF2

st.title("Resume AI - By Yasaswini")
api_key = st.text_input("Gemini API Key", type="password")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    pdf = st.file_uploader("Resume PDF", type=["pdf"])
    jd = st.text_area("Job Description")
    if st.button("Generate"):
        if pdf and jd:
            reader = PyPDF2.PdfReader(pdf)
            text = ""
            for p in reader.pages:
                text += p.extract_text()
            prompt = f"Resume:{text} Job:{jd} Give score and cover letter in simple english"
            res = model.generate_content(prompt)
            st.write(res.text)
