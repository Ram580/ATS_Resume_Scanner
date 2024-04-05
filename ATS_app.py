
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from  PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        # Handle specific exceptions here (e.g., ConnectionError, ValueError, etc.)
        return f"Error occurred: {str(e)}"

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")   

## Streamlit APP

st.set_page_config(page_title="ATS Resume Expert")
st.header("JobFit Resume ATS")
input_JD = st.text_area("Job Description: ", key='input')
uploaded_file = st.file_uploader("Upload your Resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded successfully")
    
submit1 = st.button("Tell me about the Resume")

submit2 = st.button("How can I improvise my skills")

submit3 = st.button("Percentage match")

submit4 = st.button("Missing keywords compared to Job description")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager with wide range of exposure to several prominent Technology fields like
 Data Science, AI Engineering, Full stack webdevelopment, Devops etc.,
 you will be provided with a summary of resume and a job descrption.
 your task is to review the provided resume against the provided job description of any one of the job role from the above mentioned technologies. 
 Please make share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
 Analyse the qualifications, experience, education and other relevant details of the CV.
 explain why or whynot the candidate met the fits in the position
 
"""
input_prompt2 = """
 You are an experienced Technical Human Resource Manager with wide range of exposure to several prominent Technology fields like
 Data Science, AI Engineering, Full stack webdevelopment, Devops etc.,
 you will be provided with a summary of resume and a job descrption.
 your task is to scrutinize the provided resume in the light of the provided job description of any one  of the job role from the above mentioned technologies. 
 Please make share your professional evaluation on whether the candidate's profile aligns with the role. 
 Analyse if the skills and experties of the candidate aligns well with the requirements and responsibilities of the position 
 in job description provided.
 Analyse the degree of experties required to perform the tasks in the job efficiently and effectively and 
 check if the candidate posses that degree of experties.
 Explain how well does the candidate possess the requisite knowledge and skill set?
 Explain the Areas in which the candidate can improve 
 provide suggestions on the areas where the candidate needs to work further.
"""
input_prompt3 = """
 You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding several prominent Technology fields like
 Data Science, AI Engineering, Full stack webdevelopment, Devops etc., and Deep and amazing ATS functionality, 
 your task is to evaluate the resume against the provided job description of any one of the job role from the above mentioned technologies.
 give the percentage of match if the resume matches
 the job description. First the output should come as percentage and then provide the percentage of match with the important feilds 
 like education, experience, technical skills , soft skills etc.
"""

input_prompt4 = """
 You are an experienced Technical Human Resource Manager with wide range of exposure to several prominent Technology fields like
 Data Science, AI Engineering, Full stack webdevelopment, Devops etc.,
 you will be provided with a summary of resume and a job descrption.
 your task is to scrutinize the provided resume in the light of the provided job description of any one of the job role from the above mentioned technologies. 
 Please make share your professional evaluation on whether the candidate's profile aligns with the role. 
 Analyse if the skills and experties of the candidate aligns well with the requirements and responsibilities of the position 
 in job description provided.
 provide the feedback on what are all the important Technical, soft skills and qualities that are missing in the resume.
"""
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_JD)
        st.subheader('The response is ')
        st.write(response)
    else:
        st.write("please upload the resume PDF and then click submit")
        
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_JD)
        st.subheader('The response is ')
        st.write(response)
    else:
        st.write("please upload the resume PDF and then click submit")
        
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_JD)
        st.subheader('The response is ')
        st.write(response)
    else:
        st.write("please upload the resume PDF and then click submit")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_JD)
        st.subheader('The response is ')
        st.write(response)
    else:
        st.write("please upload the resume PDF and then click submit")