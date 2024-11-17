import os
import hashlib
from pprint import pprint

IMG_PATH = "/media/whitepi/foo/Master_HPics"
DB_FILE = "/media/whitepi/foo/imageData.db"


def find_images(IMG_PATH):
    image_list = []
    for root, dirs, files in os.walk(IMG_PATH):
        for file in files:
            if file.lower().endswith(".jpg"):
                image_list.append(os.path.join(root, file))
    return image_list

def image_size(file_name):
    if file_name.lower().endswith(".jpg"):
        return os.path.getsize(file_name)
    else:
        raise ValueError("File does not end with .jpg")

def image_hash(file_name):
    if file_name.lower().endswith(".jpg"):
        hasher = hashlib.sha256()
        with open(file_name, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    else:
        raise ValueError("File does not end with .jpg")

images = find_images(IMG_PATH)
for image in images:
    print(image, image_size(image), image_hash(image))