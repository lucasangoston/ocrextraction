import os
import time
import logging
from mistralai import Mistral
from mistralai.models.sdkerror import SDKError

logger = logging.getLogger(__name__)


def upload_pdf(client: Mistral, pdf_path: str):
    logger.info("Téléchargement du fichier PDF...")
    with open(pdf_path, "rb") as pdf_file:
        uploaded_pdf = client.files.upload(
            file={
                "file_name": os.path.basename(pdf_path),
                "content": pdf_file,
            },
            purpose="ocr"
        )
    logger.info(f"Fichier téléchargé avec succès. ID du fichier : {uploaded_pdf.id}")
    return uploaded_pdf


def get_signed_url(client: Mistral, file_id: str):
    logger.info("Récupération de l'URL signée...")
    signed_url = client.files.get_signed_url(file_id=file_id)
    logger.info(f"URL signée récupérée : {signed_url.url}")
    return signed_url


def process_ocr(client: Mistral, document_url: str) -> str:
    logger.info("Traitement OCR en cours...")
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": document_url,
        }
    )
    logger.info("Traitement OCR terminé.")
    # Ici, il est possible d'extraire et de nettoyer le texte en fonction de la structure de la réponse.
    ocr_text = ocr_response
    return ocr_text


def get_correction_response(client: Mistral, model: str, prompt: str, max_attempts: int = 3) -> str:
    attempt = 0
    chat_response = None
    while attempt < max_attempts:
        try:
            logger.info("Envoi du prompt à Mistral pour obtenir la réponse (tentative %d)...", attempt + 1)
            chat_response = client.chat.complete(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            break
        except SDKError as e:
            if e.status_code == 429:
                logger.warning("Rate limit exceeded. Attente avant de réessayer...")
                time.sleep(3)
            else:
                logger.exception("Erreur lors de l'obtention de la réponse")
                raise
            attempt += 1

    if chat_response is None:
        logger.error("Nombre maximal de tentatives atteint. Échec de l'appel API pour la réponse.")
        raise Exception("Rate limit exceeded even after retries")

    response_text = chat_response.choices[0].message.content
    logger.info("Réponse reçue :")
    logger.info(response_text)
    return response_text