import os


class Face:
    def __init__(self, name, image_path):
        self.name = name
        self.image_path = image_path

    @staticmethod
    def from_folder(folder_path):
        faces = []
        for name in os.listdir(folder_path):
            user_folder = os.path.join(folder_path, name)
            if os.path.isdir(user_folder):
                for img in os.listdir(user_folder):
                    faces.append(Face(name, os.path.join(user_folder, img)))
        return faces
