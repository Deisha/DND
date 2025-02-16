import os
import pdfplumber
import pytesseract
import requests
import streamlit as st
from PIL import Image

# Set API Key
os.environ["GROQ_API_KEY"] = "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"
GROQ_CLOUD_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_CLOUD_API_KEY:
    st.error("Groq Cloud API key not found. Please set the GROQ_API_KEY environment variable.")
    st.stop()

# Streamlit UI Configuration
st.set_page_config(page_title="StartupMate", page_icon="💡", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #F3E5F5;
        color: #4A148C;
    }
    .stApp {
        background-color: #F3E5F5;
    }
    .css-1aumxhk {
        background-color: #F3E5F5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display Logo
logo_path = "logofinal.png"  # Ensure this is in the same directory
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=200)

st.title("💡 StartupMate - Your AI Co-Founder")
st.subheader("Helping solo founders navigate their startup journey with AI-powered insights.")

# Pre-defined PDF Files
pdf_files = ["jumpstart.pdf", "harvard.pdf","start1.pdf"]  # Place these in the same directory

def extract_text_from_pdf(pdf_path):
    """Extracts text from PDF, including OCR for image-based content."""
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
                else:
                    image = page.to_image().original
                    ocr_text = pytesseract.image_to_string(image)
                    full_text += ocr_text + "\n"
    except Exception as e:
        st.error(f"Error processing {pdf_path}: {e}")
    return full_text

# Extract Text from Predefined PDFs
all_text = ""
for pdf in pdf_files:
    if os.path.exists(pdf):
        all_text += extract_text_from_pdf(pdf) + "\n"
    else:
        st.error(f"File {pdf} not found. Please ensure it's in the same directory.")

# AI Interaction
st.write("### Ask AI About Your Startup")
user_input = st.text_area("Question:")

def get_ai_response(conversation_history):
    """Fetches AI response from API."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {GROQ_CLOUD_API_KEY}"}
    data = {"model": "llama3-8b-8192", "messages": conversation_history, "max_tokens": 4000}
    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        return response.json()["choices"][0]["message"]["content"]
    return f"Error: {response.status_code} - {response.text}"

if st.button("Enter") and user_input:
    conversation = [{"role": "system", "content": "You are an AI assistant for startup founders."},
                    {"role": "user", "content": user_input}]
    response = get_ai_response(conversation)
    st.success("**AI Response:**")
    st.write(response)
