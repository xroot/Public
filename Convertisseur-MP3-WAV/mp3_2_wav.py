import os

# Ajouter FFmpeg et FFprobe au PATH à l'exécution
ffmpeg_path = "C:/ffmpeg/bin"
os.environ["PATH"] += os.pathsep + ffmpeg_path

import pydub.utils

print("FFmpeg trouvé après correction :", pydub.utils.which("ffmpeg"))
print("FFprobe trouvé après correction :", pydub.utils.which("ffprobe"))

# Définir les chemins manuellement
ffmpeg_path = "C:/ffmpeg/bin/ffmpeg.exe"
ffprobe_path = "C:/ffmpeg/bin/ffprobe.exe"

# Vérification des fichiers
if not os.path.exists(ffmpeg_path):
    print(f"⚠️ Erreur : FFmpeg introuvable à {ffmpeg_path}")
    exit(1)
if not os.path.exists(ffprobe_path):
    print(f"⚠️ Erreur : FFprobe introuvable à {ffprobe_path}")
    exit(1)

# Affectation des chemins à pydub
pydub.AudioSegment.converter = ffmpeg_path
pydub.utils.which("ffmpeg")
pydub.utils.which("ffprobe")

from pydub import AudioSegment

mp3_path = "resources/alarms/alarm-01.mp3"
wav_path = "resources/alarms/alarm-01.wav"

# Vérifier que le fichier MP3 existe avant conversion
if not os.path.exists(mp3_path):
    print(f"⚠️ Erreur : Fichier MP3 introuvable à {mp3_path}")
    exit(1)

audio = AudioSegment.from_mp3(mp3_path)
audio.export(wav_path, format="wav")

print("✅ Conversion réussie !")
