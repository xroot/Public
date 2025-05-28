import json


def save_json_to_file(data, filepath):
    """
    Sauvegarde les données au format JSON dans un fichier.

    Args:
        data (dict): Les données à sauvegarder.
        filepath (str): Le chemin du fichier où enregistrer les données JSON.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier JSON à {filepath}: {e}")
        return False
    finally:
        f.close() if 'f' in locals() else None  # Assure que le fichier est fermé
        # Ferme le fichier si ouvert
    return True
