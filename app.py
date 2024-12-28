import cv2
from tkinter import Label, Canvas, Button, filedialog, StringVar, ttk
from PIL import Image, ImageTk
from cameramanager import CameraManager
from classifiermanager import ClassifierManager
from filemanager import FileManager


#
# APP.PY - Graphische Benutzeroberfläche 
#
# Installiere Bibliothek "PySide 6": pip install PySide6
#
# Imports
import sys 
from PySide6.QtWidgets import QApplication, QWidget
#
# Test
app = QApplication(sys.argv)

window = QWidget()
window.show()

app.exec()
#
#


class App:
    def __init__(self, root):
        # Initialisiert die Andwendung und die GUI-Komponenten
        # 
        # 
        # 
        self.root = root
        self.root.title("Gesichtserkennung")

        # Manager-Instanzen
        self.camera_manager = CameraManager()
        self.classifier_manager = ClassifierManager()
        self.file_manager = FileManager()

        pass

    def refresh_camera_list(self):
        # Aktualisiert die Kameraliste und zeigt verfügbare Kameras an.
        pass
            
    def start_camera(self):
        # Startet die Kamera und den Live-Modus.
        pass

    def stop_camera(self):
        # Stoppt die Kamera.
        pass

    def load_image_from_file(self):
        # Lädt ein Bild von der Festplatte und zeigt es an.
        pass

    def update_frame(self):
        # Holt ein Frame von der Kamera und zeigt es in der GUI an.
        pass