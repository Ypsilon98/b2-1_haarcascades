from tkinter import filedialog

import os
from tkinter import filedialog
import cv2

class FileManager:
    def __init__(self):
        #Initialisiert den FileManager. Ist hier implementiert aufgrund Erweiterungen in der Zukunft.
        pass

    def open_file_dialog(self, title="Datei auswählen", filetypes=(
            ("Bilder", "*.jpg;*.png;*.jpeg"),
            ("Alle Dateien", "*.*")
    )):
        #Öffnet ein Dialogfeld, um eine Datei auszuwählen.
        #Gibt zurück den Pfad zur ausgewählten Datei oder None, falls abgebrochen.
        
        file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if file_path:
            print(f"Datei ausgewählt: {file_path}")
            return file_path
        else:
            print("Keine Datei ausgewählt.")
            return None

    def load_image(self, file_path):
        #Lädt ein Bild von einem angegebenen Dateipfad.
        #Das geladene Bild als NumPy-Array oder None, falls fehlgeschlagen.
       
        if not os.path.exists(file_path):
            print(f"Fehler: Datei {file_path} nicht gefunden.")
            return None

        image = cv2.imread(file_path)
        if image is None:
            print(f"Fehler: Datei {file_path} konnte nicht geladen werden.")
        else:
            print(f"Bild erfolgreich geladen: {file_path}")
        return image

    def save_file_dialog(self, title="Speichere Datei", defaultextension=".jpg", filetypes=(
        ("JPEG-Bild", "*.jpg"),
        ("PNG-Bild", "*.png"),
        ("Alle Dateien", "*.*")
    )):
        
       #Öffnet ein Dialogfeld, um eine Datei zu speichern.
       #Parameters:
           # title (str): Der Titel des Dialogfelds.
           # defaultextension (str): Die Standard-Dateierweiterung.
           # filetypes (tuple): Die zulässigen Dateitypen.

           # str: Gibt zurück den Pfad zur gespeicherten Datei oder None, falls abgebrochen.
        
        file_path = filedialog.asksaveasfilename(
            title=title, defaultextension=defaultextension, filetypes=filetypes
        )
        if file_path:
            print(f"Datei wird gespeichert unter: {file_path}")
            return file_path
        else:
            print("Speichern abgebrochen.")
            return None


file_manager = FileManager()
file_manager.open_file_dialog()
