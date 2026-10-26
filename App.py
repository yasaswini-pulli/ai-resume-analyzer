import streamlit as st
import google.generativeai as genai
import PyPDF2
import time

st.set_page_config(page_title="Resume AI - By Yasaswini")
st.title("Resume AI - By Yasaswini")

api_key = st.text_input("Enter your Gemini API Key", type="password")
if not api_key:
    st.stop()

genai.configure(api_key=api_key)

# FIX - Quota ekkuva unna model
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Resume PDF", type="pdf")
job_desc = st.text_area("Job Description", height=200)

if st.button("Generate"):
    if not uploaded_file or not job_desc:
        st.warning("Resume & Job Description pettali")
    else:
        with st.spinner("Analyzing... 10 sec wait chey"):
            reader = PyPDF2.PdfReader(uploaded_file)
            text = "".join([p.extract_text() or "" for p in reader.pages])
            prompt = f"Resume: {text}\n\nJob Desc: {job_desc}\n\nGive Match %, Missing Skills, Improvements, Cover Letter"
            try:
                time.sleep(2)
                res = model.generate_content(prompt)
                st.success("Done!")
                st.markdown(res.text)
            except Exception as e:
                st.error("API limit ayipoyindi. 1 minute aagi malli Generate nokku. Inka kotha Gmail tho key teesko - 100% work avuddi")
                st.write(str(e))
