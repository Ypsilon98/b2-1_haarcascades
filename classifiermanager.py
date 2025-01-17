import cv2
from filemanager import FileManager

class ClassifierManager:

    # Initialisiert den Klassifizierer-Manager.
    def __init__(self):
        
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.file_manager = FileManager()


    # Lädt eine Haar-Cascade XML-Datei zum Erkennen von Gesichtern.
    def load_classifier(self):
        
        file_path = self.file_manager.open_file_dialog(title="Wähle Haar-Cascade XML-Datei", filetypes=(("XML-Dateien", "*.xml"), ("Alle Dateien", "*.*")))
        if file_path:
            self.face_cascade = cv2.CascadeClassifier(file_path)
        else:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        return file_path.split("/")[-1] if file_path else "Keine Datei ausgewählt!"


    # Trainiert einen benutzerdefinierten Haar-Cascade Klassifizierer.
    def train_classifier(self):
        
        pass


    # Erkennt Gesichter in einem gegebenen Frame.
    def detect_faces(self, frame):
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(30, 30))
        return faces

