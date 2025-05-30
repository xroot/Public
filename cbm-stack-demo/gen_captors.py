import json
import random
from datetime import datetime, timedelta, timezone

import numpy as np

capteur = 101  # Nombre total de capteurs +1 (car range exclut la borne supérieure)


def generate_sensor_data(sensor_id, timestamp):
    """
    Génère des données simulées pour un capteur donné.

    Args:
        sensor_id (str): Identifiant unique du capteur, ex "vib_001".
        timestamp (datetime): Horodatage de la mesure.

    Returns:
        dict: Dictionnaire contenant les données du capteur avec
              acceleration, fréquence, timestamp, sampling rate.
    """
    np.random.seed(int(sensor_id[-3:]))  # Seed pour reproductibilité selon id
    acceleration = np.random.logistic(0, 0.05, 100).round(4).tolist()
    frequency = np.linspace(50, 1000, 20).round(2).tolist()

    return {
        "sensor_id": sensor_id,
        "timestamp": timestamp.isoformat() + "Z",
        "sampling_rate_hz": 1000,
        "data": {
            "acceleration": acceleration,
            "frequency": frequency
        }
    }


def generate_all_sensors():
    """
    Génère une liste de données pour tous les capteurs définis dans `capteur`.
    Chaque capteur aura un timestamp unique avec un incrément aléatoire
    entre 0.5 et 2 secondes par rapport au capteur précédent.

    Returns:
        list: Liste des dictionnaires de données capteurs.
    """
    all_sensors = []
    datetime.now(timezone.utc)
    timestamp = 1571595618.0
    base_time = datetime.fromtimestamp(timestamp, timezone.utc)
    current_time = base_time

    for i in range(1, capteur):
        # Incrément aléatoire de temps entre 0.5 et 2 secondes
        delta = timedelta(seconds=random.uniform(0.5, 2.0))
        current_time += delta

        sensor_id = f"vib_{i:03d}"
        sensor_data = generate_sensor_data(sensor_id, current_time)
        all_sensors.append(sensor_data)

    return all_sensors


if __name__ == "__main__":
    data = {
        "vib": generate_all_sensors()
    }
    with open("sensor_data/sensors_vibration.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Fichier sensor_data/sensors_vibration.json créé avec {capteur - 1} capteurs dans la clé 'vib'.")
    print("Données générées avec succès.")
    print(f"Timestamp de la première mesure : {data['vib'][0]['timestamp']}")
    print(f"Timestamp de la dernière mesure : {data['vib'][-1]['timestamp']}")
    print(f"Nombre total de capteurs : {len(data['vib'])}")
    print("Exécution terminée.")

# Génération de données capteurs pour un fichier JSON
# pour l'analyse de vibrations.
# Ce script génère des données de capteurs de vibrations simulées
# et les enregistre dans un fichier JSON.
# Il crée des données pour 100 capteurs avec des timestamps uniques.
