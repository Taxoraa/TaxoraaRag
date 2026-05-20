import os
import time
from dotenv import load_dotenv
from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def upload_pdf(pdf_path: str):
    """
    Upload PDF once and wait until Gemini finishes processing it.
    """

    uploaded_file = client.files.upload(file=pdf_path)

    while uploaded_file.state and uploaded_file.state.name == "PROCESSING":
        print("Waiting for PDF processing...")
        time.sleep(2)
        uploaded_file = client.files.get(name=uploaded_file.name)

    if uploaded_file.state and uploaded_file.state.name == "FAILED":
        raise Exception("PDF processing failed.")

    return uploaded_file


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=20)
)
def generate_response(uploaded_file, prompt: str):
    """
    Retry ONLY generation, not upload.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            uploaded_file,
            prompt
        ]
    )

    return response.text


def analyze_pdf(pdf_path: str, prompt: str):
    uploaded_file = upload_pdf(pdf_path)
    return generate_response(uploaded_file, prompt)