import cv2

class CameraManager:
    def __init__(self):
        # Initialisiert den Kamera-Manager.
        self.cap = None
    

    def detect_cameras(self):
        # Erkennt verfügbare Kameras und gibt eine Liste der Indizes zurück.
        # Testet nur die ersten drei Kameras
        available_cameras = []
        for camera_id in range (3):
            self.cap = cv2.VideoCapture(camera_id)
            if self.cap.isOpened():
                available_cameras.append(camera_id)
                self.cap.release()
        return available_cameras

    def start_camera(self, camera_id =0):
        # Startet die Kamera mit dem angegebenen Index.
        self.cap = cv2.VideoCapture(camera_id)
        #Testen, ob Kamera geöffnet wurde.
        if self.cap.isOpened():
            print (f"Kamera mit ID {camera_id} wurde erfolgreich geöffnet")
            return self.cap
        else:
            print (f"Fehler: Kamera mit ID {camera_id} konnte nicht geöffnet werden")
            return None
        


    def stop_camera(self):
        # Stoppt die Kamera und gibt Ressourcen frei.
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            print("Kamera erfolgreich geschlossen")


    def get_frame(self):
        # Liefert einen Frame von der Kamera.
        if self.cap is not None and self.cap.isOpended():
            ret, frame = self.cap.read()
            if ret:
                return frame, True
            else:
                return None, False
    
