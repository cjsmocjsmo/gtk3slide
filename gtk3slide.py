import gi
import os
import sqlite3
import hashlib
import argparse
from gi.repository import Gtk, GdkPixbuf, GLib

gi.require_version('Gtk', '3.0')

class PhotoViewer(Gtk.Window):
    def __init__(self, db_file):
        super().__init__(title="Photo Viewer")

        self.image = Gtk.Image()
        self.set_default_size(800, 600)
        self.add(self.image)

        self.db_file = db_file
        self.current_photo = 1

        # Open the window in fullscreen mode
        self.fullscreen()

        # Show the first image
        self.show_photo(self.current_photo)

    def get_photo_path(self, idx):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT image_path FROM imageData WHERE idx = ?', (idx,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def show_photo(self, idx):
        photo_path = self.get_photo_path(idx)
        if not photo_path:
            print("No photo found for idx:", idx)
            return

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(photo_path)

        # Create a new pixbuf with a black background
        width, height = pixbuf.get_width(), pixbuf.get_height()
        new_pixbuf = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, False, 8, width, height)
        new_pixbuf.fill(0x000000)  # Fill with black color
        pixbuf.copy_area(0, 0, width, height, new_pixbuf, 0, 0)

        # Set the pixbuf to the image widget
        self.image.set_from_pixbuf(new_pixbuf)

    def show_next_photo(self):
        self.current_photo += 1
        self.show_photo(self.current_photo)

        # Schedule the next photo change
        GLib.timeout_add(11000, self.show_next_photo)  # 11 seconds for the animation to finish

def setup(db_file, img_path):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # if not os.path.exists(db_file):
    create_tables(cursor)
    conn.commit()
    insert_data(cursor, img_path)
    conn.commit()
    conn.close()
    # else:
    #     cursor.execute('SELECT MAX(idx) FROM imageData')
    #     max_idx = cursor.fetchone()[0]
    #     conn.close()
    #     print(f"Database already exists\nThere are {max_idx} entries in the db")

def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS imageData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT NOT NULL,
        idx INTEGER NOT NULL,
        size INTEGER NOT NULL,
        hash TEXT NOT NULL
    )
    ''')

def insert_data(cursor, img_path):
    images = find_images(img_path)
    idx = 0
    for image in images:
        idx += 1
        print(idx)
        size = image_size(image)
        hash_value = image_hash(image)
        cursor.execute('''
        INSERT INTO imageData (image_path, idx, size, hash) VALUES (?, ?, ?, ?)
        ''', (image, idx, size, hash_value))

def find_images(directory):
    image_list = []
    for root, dirs, files in os.walk(directory):
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

def create_db_file(dbfile):
    if not os.path.exists(dbfile):
        with open(dbfile, 'a'):
            os.utime(dbfile, None)  # Update the file's access and modification times

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Photo Viewer")
    parser.add_argument('-i', '--images', required=True, help="Path to the images directory")
    parser.add_argument('-d', '--database', required=True, help="Path to the database file")
    args = parser.parse_args()

    IMG_PATH = args.images
    DB_FILE = args.database

    create_db_file(DB_FILE)

    if not os.path.exists(DB_FILE):
        create_db_file(DB_FILE)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        create_tables(cursor)
        conn.commit()
        setup(DB_FILE, IMG_PATH)
        conn.commit()
        conn.close()
    
    max_idx = 0
    if os.path.exists(DB_FILE):
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(idx) FROM imageData')
            max_idx = cursor.fetchone()[0]
            conn.close()
            print(f"Database already exists\nThere are {max_idx} entries in the db")
            create_tables(cursor)
            conn.commit()
            setup(DB_FILE, IMG_PATH)
            conn.commit()
            conn.close()
        except sqlite3.OperationalError:
            print(f"The database file exists\nHOWEVER IT IS EMPTY\nRunning setup")
            create_tables(cursor)
            conn.commit()
            setup(DB_FILE, IMG_PATH)
            conn.commit()
            conn.close()

    window = PhotoViewer(DB_FILE)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    window.show_next_photo()
    Gtk.main()