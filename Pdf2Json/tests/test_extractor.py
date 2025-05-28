import os
from pdf2json.extractor import extract_text_from_pdf

# Obtenir le chemin absolu du dossier "tests/pdf"
pdf_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf")

# Vérifie si le dossier existe
if not os.path.exists(pdf_directory):
    print(f"Le dossier {pdf_directory} n'existe pas !")
else:
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

    # Test de l'extraction du texte pour chaque fichier PDF dans le dossier
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        print(f"Extraction du texte de |{pdf_file}| en cours...")

        # Extraction du texte depuis le fichier PDF
        extracted_text = extract_text_from_pdf(pdf_path)

        print(f"Texte extrait de |{pdf_file}| :")
        print(extracted_text)
        print("-" * 50)  # Séparateur pour chaque fichier
