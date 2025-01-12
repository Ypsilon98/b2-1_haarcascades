import cv2

class CameraManager:

    # Initialisiert den Kamera-Manager.
    def __init__(self):
        
        self.cap = None
    
    # Erkennt verfügbare Kameras und gibt eine Liste der Indizes zurück.
    # Testet nur die ersten drei Kameras
    def detect_cameras(self):

        available_cameras = []
        for camera_id in range (3):
            self.cap = cv2.VideoCapture(camera_id)
            if self.cap.isOpened():
                available_cameras.append(camera_id)
                self.cap.release()
        return available_cameras
    

    # Startet die Kamera mit dem angegebenen Index.
    def start_camera(self, camera_id =0):

        self.cap = cv2.VideoCapture(camera_id)

        # Testen, ob Kamera geöffnet wurde.
        if self.cap.isOpened():
            print (f"Kamera mit ID {camera_id} wurde erfolgreich geöffnet")
            return self.cap
        else:
            print (f"Fehler: Kamera mit ID {camera_id} konnte nicht geöffnet werden")
            return None
        

    # Stoppt die Kamera und gibt Ressourcen frei.
    def stop_camera(self):
        
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            print("Kamera erfolgreich geschlossen")


    # Liefert einen Frame von der Kamera.
    def get_frame(self):
        
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame, True
            else:
                return None, False
    
