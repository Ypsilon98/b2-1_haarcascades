import cv2

class CameraManager:
    def __init__(self):
        """Initialisiert den Kamera-Manager."""
        self.cap = None
        self.running = False

    def detect_cameras(self):
        """Erkennt verfügbare Kameras und gibt eine Liste der Indizes zurück."""
        cameras = []
        for i in range(5):  # Check the first 5 indexes
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(i)
                cap.release()
        return cameras

    def start_camera(self, camera_index=0):
        """Startet die Kamera mit dem angegebenen Index."""
        self.cap = cv2.VideoCapture(camera_index)
        self.running = self.cap.isOpened()
        if not self.running:
            raise Exception(f"Kamera {camera_index} konnte nicht gestartet werden.")


    def stop_camera(self):
        """Stoppt die Kamera und gibt Ressourcen frei."""
        if self.cap:
            self.cap.release()
        self.cap = None
        self.running = False

    def get_frame(self):
        """Liefert einen Frame von der Kamera."""
        if self.running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None
