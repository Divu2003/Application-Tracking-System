import streamlit as st
from dotenv import load_dotenv
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Google generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Specify the path to Poppler's binaries
poppler_path = r'C:\Users\sakshi\Projects\ATS Tracker Sytem\poppler-24.02.0\Library\bin'  # Replace with the actual path to Poppler's bin directory

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            # Convert the PDF to image using the specified Poppler path
            images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)
            first_page = images[0]

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
        except pdf2image.exceptions.PDFInfoNotInstalledError:
            st.error("Poppler is not installed or not in the PATH. Please install Poppler to proceed.")
            return None
    else:
        raise FileNotFoundError("No file uploaded")

# Inject CSS to add background image from URL and style elements
def add_bg_from_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
        }}
        .stTextArea {{
            border: 2px solid #4CAF50;
            border-radius: 5px;
            padding: 10px;
        }}
        .stButton > button {{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 5px;
            cursor: pointer;
        }}
        .stFileUploader {{
            border: 2px solid #2196F3;
            border-radius: 5px;
            padding: 10px;
        }}
        .css-1d391kg {{
            border: 2px solid #FF5722;
            border-radius: 5px;
            padding: 10px;
        }}
        .css-1y4p8pa {{
            border: 2px solid #FF9800;
            border-radius: 5px;
            padding: 10px;
        }}
        .stSidebar {{
            border: 2px solid #3F51B5;
            border-radius: 5px;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.8);
        }}
        .css-1aumxhk {{
            border: 2px solid #3F51B5;
            border-radius: 5px;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.8);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function with the URL to your image
background_image_url = "https://e1.pxfuel.com/desktop-wallpaper/271/821/desktop-wallpaper-cv-backgrounds-cv.jpg"
add_bg_from_url(background_image_url)

# Streamlit App
# st.set_page_config(page_title="ATS Resume Expert", layout="wide")
st.title("ATS Tracking System")

# Sidebar for uploading resume
st.sidebar.header("Upload Resume")
uploaded_file = st.sidebar.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.success("PDF Uploaded Successfully")

# Job Description input
st.header("Job Description")
input_text = st.text_area("Paste the job description here:")

# Buttons for different actions
col1, col2, col3 = st.columns(3)
with col1:
    submit1 = st.button("Evaluate Resume")

with col2:
    #submit2 = st.button("How Can I Improvise my Skills")
    pass

with col3:
    submit3 = st.button("Percentage Match")

# Prompts for AI model
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please evaluate whether the candidate's profile aligns with the requirements outlined in the job description. Highlight the strengths 
and weaknesses of the applicant in relation to the specified job requirements. Provide your professional evaluation on whether the resume 
is a good fit for the role or not. Additionally, offer suggestions for improvement for the recruiter based on the resume content.

Please accurately identify and sum the total work experience from the resume. Work experience can be stated in years or months 
and may appear in various date formats.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
You are tasked with evaluating a resume against the provided job description. Based on this comparison, give the percentage match of 
the resume against the job description. The output should be in percentage.

Additionally, categorize the resume by listing only the missing keywords or skills from the resume that are required for the job. 
Do not mention keywords that are already present in the resume as missing. Provide your final thoughts on the overall suitability of 
the resume for the role.
"""

# Action handlers for the buttons
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("Evaluation Result")
            st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("Percentage Match Result")
            st.write(response)
    else:
        st.write("Please upload the resume")
