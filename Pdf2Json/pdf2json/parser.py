import re


def parse_rules_from_pdf(text):
    """
    Applique les règles de parsing définies dans un texte.

    Args:
        text (str): Le texte extrait d'un fichier PDF.

    Returns:
        dict: Dictionnaire contenant les données extraites suivant les règles définies.
    """
    rules = {}

    # Exemple : Rechercher une adresse e-mail dans le texte
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)

    if emails:
        rules['emails'] = emails

    # Tu peux ajouter d'autres règles de parsing ici

    return rules
