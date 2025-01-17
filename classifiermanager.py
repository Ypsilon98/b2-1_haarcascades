import cv2
from filemanager import FileManager

class ClassifierManager:

    # Initialisiert den Klassifizierer-Manager.
    def __init__(self):
        
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.file_manager = FileManager()

        # Dictionary für native OpenCV-Klassifizierer
        self.classifiers = {
            "face": "haarcascade_frontalface_default.xml",
            "eye": "haarcascade_eye.xml",
            "smile": "haarcascade_smile.xml",
            "upperbody": "haarcascade_upperbody.xml",
            "fullbody": "haarcascade_fullbody.xml",
            "profileface": "haarcascade_profileface.xml"
        }


    # Lädt eine Haar-Cascade XML-Datei zum Erkennen von Gesichtern.
    def load_custom_classifier(self):
        
        file_path = self.file_manager.open_file_classifier()
        if file_path:
            self.face_cascade = cv2.CascadeClassifier(file_path)
        else:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        return file_path.split("/")[-1] if file_path else "Keine Datei ausgewählt!"
    

    """
    Lädt einen nativen OpenCV-Klassifizierer basierend auf einer angegebenen ID.

    :param classifier_id: ID des gewünschten Klassifizierers (z. B. "face", "eye", "smile").
    :return: Name des geladenen Klassifizierers oder eine Fehlermeldung.
    """    
    def load_classifier(self, classifier_id):
        
        if classifier_id not in self.classifiers:
            print(f"Ungültige ID: '{classifier_id}'")
            return "Ungültige ID!"

        # Den Dateipfad für den gewünschten Klassifizierer erstellen
        classifier_path = cv2.data.haarcascades + self.classifiers[classifier_id]
        print(f"Lade Klassifizierer '{self.classifiers[classifier_id]}'...")

        # Versuchen, den Klassifizierer zu laden
        self.face_cascade = cv2.CascadeClassifier(classifier_path)
        if self.face_cascade.empty():
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            print(f"Laden des Klassifizierers '{self.classifiers[classifier_id]}' fehlgeschlagen")
            return "Laden fehlgeschlagen! Standard wird zurückgesetzt"

        print(f"Klassifizierer '{self.classifiers[classifier_id]}' erfolgreich geladen.")
        return self.classifiers[classifier_id]




    # Trainiert einen benutzerdefinierten Haar-Cascade Klassifizierer.
    def train_classifier(self):
        pass


    # Erkennt Gesichter in einem gegebenen Frame.
    def detect_faces(self, frame):
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(30, 30))
        return faces

