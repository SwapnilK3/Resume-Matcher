import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv


load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template
task=""" """
input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. 
task:{task}
resume:{text}
description:{jd}

I want the response in one single string where as per the task you need to do in structure of 

"""


## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit1 = st.button("Get JD Maching Percentage ")
submit2 = st.button("Tell Me About the Resume")
submit3 = st.button("How Can I Improvise my Skills")

if submit1:
    if uploaded_file is not None:
        task="Provide the percentage Matching based on Jd"
        input_prompt+='JD matching: "%" and Missing Words to improve your Resume'
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)
        
elif submit2:
    if uploaded_file is not None:
        task="Tell Me About the my Resume and what i lack in my Resume"
        input_prompt+='Missing Points, unwanted points in it has, and other into to improve My Resume'
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)
        
elif submit3:
    if uploaded_file is not None:
        task="How Can I Improvise my Skills to match my Resume"
        input_prompt+='Skills Needed, Resourses for upscalling also provide websites that has the free resources'
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)