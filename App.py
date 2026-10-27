import streamlit as st
import google.generativeai as genai
import PyPDF2
import time

st.set_page_config(page_title="Resume AI - By Yasaswini")
st.title("Resume AI - By Yasaswini")

api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)


model = genai.GenerativeModel('models/gemini-3.5-flash-lite')
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

# Add this new function in your app.py

def rewrite_resume_for_ats(resume_text, jd_text):
    prompt = f"""
    You are an expert ATS Resume Writer for Qualcomm/TCS.

    TASK: Rewrite the user's resume to increase ATS match from 52% to 85%+ WITHOUT LYING.

    RULES:
    1. DO NOT add fake skills like "Expert in C++" if user doesn't know.
    2. Instead, BRIDGE existing skills: 
       Example: If JD asks C++ and user knows Embedded C -> Write "Proficient in C/C++ concepts through Embedded C projects"
       Example: If JD asks OOPs and user knows C -> Write "Applied OOPs concepts using Python in Resume AI project"
    3. Keep all original projects, just add JD keywords naturally.
    4. Output should be in proper Resume Format.

    USER RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {jd_text}

    OUTPUT FORMAT:
    Give me a NEW Improved Resume text only.
    """
    # call your LLM here - response = openai.chat.completions.create(...)
    # return response
    return prompt
                


