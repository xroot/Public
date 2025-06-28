import os

import cv2

FACES_FOLDER = "data/faces"


def ensure_faces_folder():
    os.makedirs(FACES_FOLDER, exist_ok=True)


def save_face_image(name, image):
    ensure_faces_folder()
    person_folder = os.path.join(FACES_FOLDER, name)
    os.makedirs(person_folder, exist_ok=True)
    idx = len(os.listdir(person_folder)) + 1
    filename = os.path.join(person_folder, f"{name}_{idx}.png")
    cv2.imwrite(filename, image)
    return filename


def list_faces():
    ensure_faces_folder()
    faces = {}
    for name in os.listdir(FACES_FOLDER):
        folder = os.path.join(FACES_FOLDER, name)
        if os.path.isdir(folder):
            faces[name] = [os.path.join(folder, img) for img in os.listdir(folder)]
    return faces
