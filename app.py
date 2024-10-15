import streamlit as st
from dotenv import load_dotenv
import base64
import os
import io
from PIL import Image
import fitz  # PyMuPDF
import google.generativeai as genai
import zipfile

# Load environment variables
load_dotenv()

# Configure the Google generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            # Open the PDF document
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            first_page = pdf_document[0]  # Access the first page
            
            # Create a pixmap (an image representation) of the page
            pix = first_page.get_pixmap()
            img_byte_arr = io.BytesIO()
            img_byte_arr.write(pix.tobytes("jpeg"))  # Convert to JPEG
            
            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr.getvalue()).decode()  # Encode to base64
                }
            ]
            return pdf_parts
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None
    else:
        raise FileNotFoundError("No file uploaded")

def process_zip_file(uploaded_file):
    resumes = []
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall("temp_resumes")  # Extract to a temporary directory
        for file_name in zip_ref.namelist():
            if file_name.endswith('.pdf'):  # Check for PDF files
                with open(f"temp_resumes/{file_name}", "rb") as pdf_file:
                    resumes.append((file_name, pdf_file.read()))
    return resumes

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    pdf_document = fitz.open(stream=pdf_file, filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text += page.get_text() + "\n"
    return text

# Function to create a PDF blob
def create_pdf_blob(pdf_file):
    return pdf_file.read()

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
st.title("Applicant Tracking System")

# Sidebar for uploading resumes
st.sidebar.header("Upload Resumes")
uploaded_zip = st.sidebar.file_uploader("Upload a ZIP file containing resumes...", type=["zip"])

# Job Description input
st.header("Job Description")
input_text = st.text_area("Paste the job description here:")

# Buttons for different actions
col1, col2, col3 = st.columns(3)
with col1:
    submit1 = st.button("Evaluate Resumes")

with col2:
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
You are tasked with evaluating a resume against the provided job description. Based on this comparison, diaplay only the percentage match of 
the resume against the job description and suggest resume is good fit or not in one line. 
"""

# Action handlers for the buttons
if submit1:
    if uploaded_zip is not None:
        resumes = process_zip_file(uploaded_zip)
        for file_name, pdf_content in resumes:
            resume_text = extract_text_from_pdf(io.BytesIO(pdf_content))
            response = get_gemini_response(input_prompt1, [resume_text], input_text)
            st.subheader(f"Evaluation Result for {file_name}")
            st.write(response)
    else:
        st.write("Please upload the ZIP file containing resumes.")

elif submit3:
    st.subheader("Percentage Match are as follow")  
    if uploaded_zip is not None:
        resumes = process_zip_file(uploaded_zip)
        for index, (file_name, pdf_content) in enumerate(resumes, start=1):
            resume_text = extract_text_from_pdf(io.BytesIO(pdf_content))
            response = get_gemini_response(input_prompt3, [resume_text], input_text)
            # Extract just the resume name from the file path
            resume_name = os.path.basename(file_name)
            st.subheader(f"{resume_name}")
            st.write(response)
    else:
        st.write("Please upload the ZIP file containing resumes.")
<<<<<<< HEAD

=======
>>>>>>> 3fcb74b4173933eabd37b14d513c2458a5c43cc0
