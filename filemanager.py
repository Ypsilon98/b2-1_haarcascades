import os
from tkinter import filedialog
import cv2

class FileManager:

    #　Initialisiert den FileManager. Ist hier implementiert aufgrund Erweiterungen in der Zukunft.
    def __init__(self):
        self.ft_pictures = ("Bilder", "*.jpg *.png *.jpeg"), ("Alle Dateien", "*.*")
        self.ft_classifier = ("XML-Dateien", "*.xml"), ("Alle Dateien", "*.*")
  
    # Öffnet ein Dialogfeld, um eine Datei auszuwählen.
    # Gibt zurück den Pfad zur ausgewählten Datei oder None, falls abgebrochen.
    # Standardmäßig werden nur Bilddateien angezeigt.
    def open_file_picture(self, title="Datei auswählen", filetypes = None):
        
        file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if file_path:
            print(f"Datei ausgewählt: {file_path}")
            return file_path
        else:
            print("Keine Datei ausgewählt.")
            return None
        

    
    
    
    #　Lädt ein Bild von einem angegebenen Dateipfad.
    #　Das geladene Bild als NumPy-Array oder None, falls fehlgeschlagen.
    def load_image(self, file_path):

        if not os.path.exists(file_path):
            print(f"Fehler: Datei {file_path} nicht gefunden.")
            return None

        image = cv2.imread(file_path)
        if image is None:
            print(f"Fehler: Datei {file_path} konnte nicht geladen werden.")
        else:
            print(f"Bild erfolgreich geladen: {file_path}")
        return image
