from typing import List

from pydantic import BaseModel


class PDFData(BaseModel):
    emails: List[str] = []
    invoices: List[str] = []  # Si tu veux ajouter d'autres catégories de données


def generate_json_schema(data):
    """
    Génère un objet JSON à partir des données extraites et le valide.

    Args:
        data (dict): Données extraites et structurées.

    Returns:
        dict: Données au format JSON validées.
    """
    try:
        pdf_data = PDFData(**data)
        return pdf_data.dict()  # Retourne les données sous forme de dict JSON valide
    except Exception as e:
        print(f"Erreur lors de la génération du JSON : {e}")
        doc.close() if 'doc' in locals() else None  # Assure que le document est fermé
        return {}
        # Ferme le document PDF
    finally:
        # Ferme le document PDF
        doc.close() if 'doc' in locals() else None  # Assure que le document est fermé
