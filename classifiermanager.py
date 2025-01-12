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



    # Trainiert einen benutzerdefinierten Haar-Cascade Klassifizierer.
    def train_classifier(self):
        
        # Beispiel-Logik für das Training eines Klassifizierers:
        # Du kannst hier den Prozess implementieren, um z. B. Positiv- und Negativbilder zu verarbeiten.
        file_path = filedialog.askdirectory(title="Wähle Trainingsdatensatz-Ordner")
        if file_path:
            # Füge hier Code für das Training mit OpenCV hinzu (z. B. mit cv2.trainCascadeClassifier).
            print(f"Klassifizierer mit Daten aus {file_path} trainieren...")
        else:
            print("Kein Ordner ausgewählt!")



    # Erkennt Gesichter in einem gegebenen Frame.
    def detect_faces(self, frame):
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(30, 30))
        return faces

