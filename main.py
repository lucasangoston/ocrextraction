import os
from dotenv import load_dotenv
from mistralai import Mistral

# Load environment variables from .env file
load_dotenv()

# Get the Mistral API key from the environment
api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("Please set the MISTRAL_API_KEY environment variable.")

# Initialize the Mistral client
client = Mistral(api_key=api_key)

# Path to your test PDF file
pdf_path = "Document.pdf"

# Check if the file exists
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"The file {pdf_path} does not exist. Please provide a valid PDF file.")

# Step 1: Upload the PDF file
print("Uploading PDF file...")
with open(pdf_path, "rb") as pdf_file:
    uploaded_pdf = client.files.upload(
        file={
            "file_name": os.path.basename(pdf_path),
            "content": pdf_file,
        },
        purpose="ocr"
    )

print(f"Uploaded file ID: {uploaded_pdf.id}")

# Step 2: Get a signed URL for the uploaded file
print("Retrieving signed URL...")
signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)
print(f"Signed URL: {signed_url.url}")

# Step 3: Process the file with OCR
print("Processing OCR...")
ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": signed_url.url,
    }
)

# Step 4: Print the OCR results
print("\nOCR Results:")
print(ocr_response)  # Adjust based on the actual response structure
