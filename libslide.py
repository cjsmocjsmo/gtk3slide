import os
import hashlib
import sqlite3
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

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS imageData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT NOT NULL,
    count TEXT NOT NULL,
    hash TEXT NOT NULL
)
''')

images = find_images(IMG_PATH)
count = 0
for image in images:
    count += 1
    size = image_size(image)
    hash = image_hash(image)
    print(image)
    print(count)
    print(size)
    print(hash)