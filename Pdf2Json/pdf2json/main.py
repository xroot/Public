import os
from pdf2json.extractor import extract_text_from_pdf
from pdf2json.parser import parse_rules_from_pdf
from pdf2json.json_schema import generate_json_schema
from pdf2json.utils import save_json_to_file
from pdf2json.config import INPUT_PDFS_PATH, OUTPUT_PATH


def process_pdfs():
    # 1. Récupérer tous les fichiers PDF dans le dossier des données
    pdf_files = [f for f in os.listdir(INPUT_PDFS_PATH) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        # 2. Extraire les données du fichier PDF
        text = extract_text_from_pdf(os.path.join(INPUT_PDFS_PATH, pdf_file))

        # 3. Appliquer les règles de parsing (si elles existent)
        parsed_data = parse_rules_from_pdf(text)

        # 4. Générer le JSON à partir des données extraites
        json_data = generate_json_schema(parsed_data)

        # 5. Sauvegarder le JSON dans le dossier de sortie
        save_json_to_file(json_data, os.path.join(OUTPUT_PATH, f"{pdf_file}.json"))


if __name__ == "__main__":
    process_pdfs()
