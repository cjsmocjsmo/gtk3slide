# import gi
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk, GdkPixbuf, GLib

# import os

# class PhotoViewer(Gtk.Window):
#     def __init__(self):
#         super().__init__(title="Photo Viewer")

#         self.image = Gtk.Image()
#         self.set_default_size(800, 600)
#         self.add(self.image)

#         self.photos_dir = "/media/pipi/ATree/Master_HPics"  # Replace with your directory
#         self.photos = os.listdir(self.photos_dir)

#         self.current_photo = 0
        
#         # self.fullscreen()

#     def show_next_photo(self):
#         photo_path = os.path.join(self.photos_dir, self.photos[self.current_photo])
#         pixbuf = GdkPixbuf.Pixbuf.new_from_file(photo_path)

#         # Create a new pixbuf with a black background
#         width, height = pixbuf.get_width(), pixbuf.get_height()
#         new_pixbuf = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, False, 8, width, height)
#         new_pixbuf.fill(0x000000)  # Fill with black color
#         pixbuf.copy_area(0, 0, width, height, new_pixbuf, 0, 0)

#         # Set the pixbuf to the image widget
#         self.image.set_from_pixbuf(new_pixbuf)

#         # Schedule the next photo change
#         GLib.timeout_add(11000, self.show_next_photo)  # 11 seconds for the animation to finish

#         self.current_photo = (self.current_photo + 1) % len(self.photos)

# if __name__ == "__main__":
#     window = PhotoViewer()
#     window.connect("delete-event", Gtk.main_quit)
#     window.show_all()
#     window.show_next_photo()
#     Gtk.main()

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk

import os

class PhotoViewer(Gtk.Window):
    def __init__(self):
        super().__init__(title="Photo Viewer")

        self.set_default_size(1596, 1200)
        self.fullscreen()

        # Create a CSS provider and set the background color to black
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
        window {
            background-color: black;
        }
        """)

        # Apply the CSS to the window
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.image = Gtk.Image()
        self.add(self.image)

        self.photos_dir = "/media/whitepi/foo/Master_HPics"  # Replace with your directory
        self.photos = os.listdir(self.photos_dir)

        self.current_photo = 0

    def show_next_photo(self):
        photo_path = os.path.join(self.photos_dir, self.photos[self.current_photo])
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(photo_path)

        # Create a new pixbuf with a black background
        width, height = pixbuf.get_width(), pixbuf.get_height()
        new_pixbuf = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, False, 8, width, height)
        new_pixbuf.fill(0x000000)  # Fill with black color
        pixbuf.copy_area(0, 0, width, height, new_pixbuf, 0, 0)

        # Set the pixbuf to the image widget
        self.image.set_from_pixbuf(new_pixbuf)

        # Schedule the next photo change
        GLib.timeout_add(11000, self.show_next_photo)  # 11 seconds for the animation to finish

        self.current_photo = (self.current_photo + 1) % len(self.photos)

if __name__ == "__main__":
    window = PhotoViewer()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    window.show_next_photo()
    Gtk.main()