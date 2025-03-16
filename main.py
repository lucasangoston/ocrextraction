import os
import logging
from dotenv import load_dotenv
from mistralai import Mistral

from prompt_generation import generate_student_answer_prompt
from mistral_client import upload_pdf, get_signed_url, process_ocr, get_correction_response
from pdf_export import export_correction_to_pdf

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    load_dotenv()
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        logging.error("La variable d'environnement MISTRAL_API_KEY n'est pas définie.")
        raise ValueError("Veuillez définir la variable d'environnement MISTRAL_API_KEY.")

    model = "mistral-large-latest"
    client = Mistral(api_key=api_key)

    pdf_path = "files/4eme.pdf"
    if not os.path.exists(pdf_path):
        logging.error(f"Le fichier {pdf_path} n'existe pas. Veuillez fournir un fichier PDF valide.")
        raise FileNotFoundError(f"Le fichier {pdf_path} n'existe pas.")

    try:
        uploaded_pdf = upload_pdf(client, pdf_path)
        signed_url_obj = get_signed_url(client, uploaded_pdf.id)
        ocr_text = process_ocr(client, signed_url_obj.url)
    except Exception as e:
        logging.exception("Erreur lors du traitement du PDF")
        raise e

    # Génération du prompt pour obtenir la réponse d'un élève
    student_prompt = generate_student_answer_prompt(ocr_text)
    logging.info("Prompt généré :")
    logging.info(student_prompt)

    try:
        student_response = get_correction_response(client, model, student_prompt)
    except Exception as e:
        logging.exception("Erreur lors de l'obtention de la réponse")
        raise e

    # Export de la réponse en PDF dans le dossier "correction"
    os.makedirs("correction", exist_ok=True)
    output_pdf_path = os.path.join("correction", "reponse_eleve.pdf")
    export_correction_to_pdf(student_response, output_pdf_path)

    logging.info("Processus terminé avec succès.")

if __name__ == "__main__":
    main()