import os
import time
import logging
from mistralai import Mistral
from mistralai.models.sdkerror import SDKError

logger = logging.getLogger(__name__)

def upload_pdf(client: Mistral, pdf_path: str):
    logger.info("Uploading PDF...")
    with open(pdf_path, "rb") as pdf_file:
        uploaded_pdf = client.files.upload(
            file={
                "file_name": os.path.basename(pdf_path),
                "content": pdf_file,
            },
            purpose="ocr"
        )
    logger.info(f"File uploaded with ID: {uploaded_pdf.id}")
    return uploaded_pdf

def get_signed_url(client: Mistral, file_id: str):
    logger.info("Retrieving signed URL...")
    signed_url = client.files.get_signed_url(file_id=file_id)
    logger.info(f"Signed URL: {signed_url.url}")
    return signed_url

def process_ocr(client: Mistral, document_url: str) -> str:
    logger.info("Starting OCR...")
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": document_url,
        }
    )
    logger.info("OCR finished")
    return ocr_response

def get_correction_response(client: Mistral, model: str, prompt: str, max_attempts: int = 3) -> str:
    attempt = 0
    chat_response = None
    while attempt < max_attempts:
        try:
            logger.info(f"Sending prompt to Mistral (attempt {attempt + 1})...")
            chat_response = client.chat.complete(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            break
        except SDKError as e:
            if e.status_code == 429:
                logger.warning("Rate limit exceeded. Waiting before retry...")
                time.sleep(3)
            else:
                logger.exception("Error while getting the response")
                raise
            attempt += 1

    if chat_response is None:
        logger.error("Max attempts reached. API call failed")
        raise Exception("Rate limit exceeded even after retries")

    response_text = chat_response.choices[0].message.content
    logger.info("Response received")
    logger.info(response_text)
    return response_text