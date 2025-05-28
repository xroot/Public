import fitz


def extract_text_from_pdf(pdf_path):
    """
    Extrait le texte d'un fichier PDF.

    Args:
        pdf_path (str): Chemin du fichier PDF.

    Returns:
        str: Texte extrait du PDF.
    """
    global doc
    try:
        # Ouvre le fichier PDF
        doc = fitz.open(pdf_path)

        # Extraction du texte brut
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()

        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte depuis {pdf_path}: {e}")
        return ""
    finally:
        # Ferme le document PDF
        doc.close() if 'doc' in locals() else None  # Assure que le document est fermé


def extract_images_from_pdf(pdf_path):
    """
    Extrait les images d'un fichier PDF.

    Args:
        pdf_path (str): Chemin du fichier PDF.

    Returns:
        list: Liste des images extraites.
    """
    global doc
    try:
        # Ouvre le fichier PDF
        doc = fitz.open(pdf_path)

        images = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                images.append(image_bytes)

        return images
    except Exception as e:
        print(f"Erreur lors de l'extraction des images depuis {pdf_path}: {e}")
        return []
    finally:
        # Ferme le document PDF
        doc.close() if 'doc' in locals() else None  # Assure que le document est fermé


def extract_metadata_from_pdf(pdf_path):
    """
    Extrait les métadonnées d'un fichier PDF.

    Args:
        pdf_path (str): Chemin du fichier PDF.

    Returns:
        dict: Métadonnées extraites.
    """
    global doc
    try:
        # Ouvre le fichier PDF
        doc = fitz.open(pdf_path)

        # Extraction des métadonnées
        metadata = doc.metadata

        return metadata
    except Exception as e:
        print(f"Erreur lors de l'extraction des métadonnées depuis {pdf_path}: {e}")
        return {}
    finally:
        # Ferme le document PDF
        doc.close() if 'doc' in locals() else None  # Assure que le document est fermé


def extract_annotations_from_pdf(pdf_path):
    """
    Extrait les annotations d'un fichier PDF.

    Args:
        pdf_path (str): Chemin du fichier PDF.

    Returns:
        list: Liste des annotations extraites.
    """
    global doc
    try:
        # Ouvre le fichier PDF
        doc = fitz.open(pdf_path)

        annotations = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            annots = page.annots()

            if annots:
                for annot in annots:
                    annotations.append(annot.info)

        return annotations
    except Exception as e:
        print(f"Erreur lors de l'extraction des annotations depuis {pdf_path}: {e}")
        return []
    finally:
        # Ferme le document PDF
        doc.close() if 'doc' in locals() else None  # Assure que le document est fermé


def extract_links_from_pdf(pdf_path):
    """
    Extrait les liens d'un fichier PDF.

    Args:
        pdf_path (str): Chemin du fichier PDF.

    Returns:
        list: Liste des liens extraits.
    """
    global doc
    try:
        # Ouvre le fichier PDF
        doc = fitz.open(pdf_path)

        links = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            link_list = page.get_links()

            for link in link_list:
                links.append(link)

        return links
    except Exception as e:
        print(f"Erreur lors de l'extraction des liens depuis {pdf_path}: {e}")
        return []
    finally:
        # Ferme le document PDF
        doc.close() if 'doc' in locals() else None  # Assure que le document est fermé


def extract_text_with_layout_from_pdf(pdf_path):
    """
    Extrait le texte d'un fichier PDF en tenant compte de la mise en page.

    Args:
        pdf_path (str): Chemin du fichier PDF.

    Returns:
        str: Texte extrait du PDF avec mise en page.
    """
    global doc
    try:
        # Ouvre le fichier PDF
        doc = fitz.open(pdf_path)

        # Extraction du texte avec mise en page
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text")

        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte avec mise en page depuis {pdf_path}: {e}")
        return ""
    finally:
        # Ferme le document PDF
        doc.close() if 'doc' in locals() else None  # Assure que le document est fermé


def extract_text_by_block_from_pdf(pdf_path):
    """
    Extrait le texte d'un fichier PDF par blocs.

    Args:
        pdf_path (str): Chemin du fichier PDF.

    Returns:
        list: Liste des blocs de texte extraits.
    """
    global doc
    try:
        # Ouvre le fichier PDF
        doc = fitz.open(pdf_path)

        # Extraction du texte par blocs
        blocks = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks += page.get_text("blocks")

        return blocks
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte par blocs depuis {pdf_path}: {e}")
        return []
    finally:
        # Ferme le document PDF
        doc.close() if 'doc' in locals() else None  # Assure que le document est fermé


def extract_text_by_words_from_pdf(pdf_path):
    """
    Extrait le texte d'un fichier PDF par mots.

    Args:
        pdf_path (str): Chemin du fichier PDF.

    Returns:
        list: Liste des mots extraits.
    """
    global doc
    try:
        # Ouvre le fichier PDF
        doc = fitz.open(pdf_path)

        # Extraction du texte par mots
        words = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            words += page.get_text("words")

        return words
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte par mots depuis {pdf_path}: {e}")
        return []
    finally:
        # Ferme le document PDF
        doc.close() if 'doc' in locals() else None  # Assure que le document est fermé


def extract_text_by_lines_from_pdf(pdf_path):
    """
    Extrait le texte d'un fichier PDF par lignes.

    Args:
        pdf_path (str): Chemin du fichier PDF.

    Returns:
        list: Liste des lignes extraites.
    """
    global doc
    try:
        # Ouvre le fichier PDF
        doc = fitz.open(pdf_path)

        # Extraction du texte par lignes
        lines = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            lines += page.get_text("lines")

        return lines
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte par lignes depuis {pdf_path}: {e}")
        return []
    finally:
        # Ferme le document PDF
        doc.close() if 'doc' in locals() else None  # Assure que le document est fermé
