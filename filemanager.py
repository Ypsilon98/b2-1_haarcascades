import os
from tkinter import filedialog
import cv2


# FileManager-Klasse zum Verwalten von Dateioperationen.
# Unterstützt die Auswahl von Bild- und XML-Dateien.

class FileManager:

    

    # Initialisiert die Dateitypen-Filter für Bilder und Klassifizierungsdateien.
    def __init__(self):
                
        self.filetypes_pictures = [("Bilder", "*.jpg *.png *.jpeg"), ("Alle Dateien", "*.*")]
        self.filetypes_classifier = [("XML-Dateien", "*.xml"), ("Alle Dateien", "*.*")]



    """
    Öffnet ein Dialogfeld zur Auswahl einer Bilddatei.

    :param title: Titel des Dialogfelds (Standard: "Bild auswählen").
    :return: Pfad zur ausgewählten Datei oder None, falls abgebrochen.
    """
    def open_file_picture(self, title="Bild auswählen"):
        
        return self._open_file(title, self.filetypes_pictures)

    
    """
    Öffnet ein Dialogfeld zur Auswahl einer Klassifizierungsdatei (XML).

    :param title: Titel des Dialogfelds (Standard: "Klassifizierungsdatei auswählen").
    :return: Pfad zur ausgewählten Datei oder None, falls abgebrochen.
    """
    def open_file_classifier(self, title="Klassifizierungsdatei auswählen"):
        
        return self._open_file(title, self.filetypes_classifier)


    """
    Allgemeine Methode zum Öffnen eines Dialogfelds zur Dateiauswahl.

    :param title: Titel des Dialogfelds.
    :param filetypes: Dateitypenfilter für das Dialogfeld.
    :return: Pfad zur ausgewählten Datei oder None, falls abgebrochen.
    """
    def _open_file(self, title, filetypes):
        
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
           
        
        
    # Speichert einen Screenshot des aktuellen Frames mit grünen Rechtecken.
    # :param image: Aktuelles image.
    # :return: True, wenn der Screenshot erfolgreich gespeichert wurde, sonst False.
    def save_screenshot(self, image):

        # Wähle den Dateipfad aus
        file_path = self._open_file("Speicherort für Screenshot auswählen", [("PNG Dateien", "*.png"), ("JPEG Dateien", "*.jpg *.jpeg"), ("Alle Dateien", "*.*")])
        
        if not file_path:
            print("Speichern abgebrochen.")
            return False
        
        if cv2.imwrite(file_path, image):
            print(f"Bild erfolgreich gespeichert: {file_path}")
            return True
        else:
            print(f"Fehler: Bild konnte nicht gespeichert werden.")
            return False