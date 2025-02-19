import streamlit as st
import requests
import json
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()  # load all our environment variables

# Use your OpenRouter API key (which works for Deepseek as well)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def get_deepseek_response(input_text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {
                "role": "user",
                "content": input_text
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    if 'choices' in response_json and response_json['choices']:
        return response_json['choices'][0]['message']['content']
    else:
        return f"Error in response: {response_json.get('error', 'Unexpected response format')}"

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page_obj = reader.pages[page]
        text += str(page_obj.extract_text())
    return text

# Prompt Template
task = """ """
input_prompt = """
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst,
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide
best assistance for improving the resumes. 
task:{task}
resume:{text}
description:{jd}

I want the response in one single string where as per the task you need to do in structure of 
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

submit1 = st.button("Get JD Maching Percentage")
submit2 = st.button("Tell Me About the Resume")
submit3 = st.button("How Can I Improvise my Skills")

if submit1:
    if uploaded_file is not None:
        task = "Provide the percentage Matching based on JD"
        full_prompt = input_prompt + 'JD matching: "%" and Missing Words to improve your Resume'
        text = input_pdf_text(uploaded_file)
        # Format the prompt with current context values
        formatted_prompt = full_prompt.format(task=task, text=text, jd=jd)
        response = get_deepseek_response(formatted_prompt)
        formatted_response = f"### Deepseek Response\n\n{response.replace(chr(10), '<br>')}"
        st.markdown(formatted_response, unsafe_allow_html=True)

elif submit2:
    if uploaded_file is not None:
        task = "Tell Me About my Resume and what I lack in my Resume"
        full_prompt = input_prompt + 'Missing Points, unwanted points in it has, and other info to improve My Resume'
        text = input_pdf_text(uploaded_file)
        formatted_prompt = full_prompt.format(task=task, text=text, jd=jd)
        response = get_deepseek_response(formatted_prompt)
        formatted_response = f"### Deepseek Response\n\n{response.replace(chr(10), '<br>')}"
        st.markdown(formatted_response, unsafe_allow_html=True)

elif submit3:
    if uploaded_file is not None:
        task = "How Can I Improvise my Skills to match my Resume"
        full_prompt = input_prompt + 'Skills Needed, Resources for upscaling and also provide websites that have free resources'
        text = input_pdf_text(uploaded_file)
        formatted_prompt = full_prompt.format(task=task, text=text, jd=jd)
        response = get_deepseek_response(formatted_prompt)
        formatted_response = f"### Deepseek Response\n\n{response.replace(chr(10), '<br>')}"
        st.markdown(formatted_response, unsafe_allow_html=True)
