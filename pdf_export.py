import logging
from fpdf import FPDF

logger = logging.getLogger(__name__)


def export_correction_to_pdf(correction_text: str, output_path: str) -> None:
    logger.info(f"Export de la correction en PDF vers {output_path}...")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, correction_text)
    pdf.output(output_path)
    logger.info("Export PDF terminé.")