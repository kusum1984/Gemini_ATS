import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai 
import dotenv as load_dotenv
import json

load_dotenv.load_dotenv() ##load all the our environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
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

# Prompt Template

input_prompt="""
Hey act like a skilled or very experienced ATS(Application Tracking System) with a deep understanding
of tech feild,software engineering,data science,data analyst and big data engineer.Your task is to 
evaluate the resume based on the given job description.You must consider the job market is very competitive
and you shoud provide best assistance for improving the resume.Assign the percentage matching based on JD
and the missing keywords with high accuracy.
resume:{text}
description:{jd}
I want the response in one single string having the structure
{{"JD match":"%","MissingKeywords:[]","Profile Summary":""}}
""" 

##streamlit app
st.title("Smart ATS")
st.text("Improve your resume ATS")
jd=st.text_area("Paste the job Description")
uploaded_files=st.file_uploader("Upload your resume",type="pdf",help="Please upload the pdf")

submit=st.button("Submit")

if submit:
    if uploaded_files is not None:
        text=input_pdf_text(uploaded_files)
        response=get_gemini_response(input_prompt)
        st.subheader(response)
