import os
import logging
from dotenv import load_dotenv
from mistralai import Mistral

from src.mistral_client import upload_pdf, get_signed_url, process_ocr, get_correction_response
from src.prompt_generation import generate_evaluation_correction_prompt
from src.pdf_export import export_correction_to_pdf

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    load_dotenv()
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        logging.error("MISTRAL_API_KEY is missing")
        raise ValueError("Please set MISTRAL_API_KEY in your environment")

    client = Mistral(api_key=api_key)
    model = "mistral-large-latest"

    student_pdf_path = os.path.join("files", "reponse_eleve.pdf")
    corrige_pdf_path = os.path.join("files", "Corrigé.4eme.pdf")

    if not os.path.exists(student_pdf_path):
        logging.error(f"{student_pdf_path} not found.")
        raise FileNotFoundError(f"{student_pdf_path} does not exist")

    if not os.path.exists(corrige_pdf_path):
        logging.error(f"{corrige_pdf_path} not found.")
        raise FileNotFoundError(f"{corrige_pdf_path} does not exist")

    try:
        uploaded_student_pdf = upload_pdf(client, student_pdf_path)
        signed_url_student = get_signed_url(client, uploaded_student_pdf.id)
        student_text = process_ocr(client, signed_url_student.url)

        uploaded_corrige_pdf = upload_pdf(client, corrige_pdf_path)
        signed_url_corrige = get_signed_url(client, uploaded_corrige_pdf.id)
        corrige_text = process_ocr(client, signed_url_corrige.url)

        prompt = generate_evaluation_correction_prompt(student_text, corrige_text)
        correction_response = get_correction_response(client, model, prompt)

        os.makedirs("correction", exist_ok=True)
        output_pdf_path = os.path.join("correction", "evaluation_correction.pdf")
        export_correction_to_pdf(correction_response, output_pdf_path)

        logging.info("Process completed successfully.")
    except Exception as e:
        logging.exception("An error occurred during processing")
        raise e

if __name__ == "__main__":
    main()