import cv2
import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk

# Klasse: Kamera-Handler
class CameraHandler:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Kamera konnte nicht geöffnet werden")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Kein Kamerabild verfügbar")
        return frame

    def release(self):
        self.cap.release()

# Klasse: Gesichtserkennung
class FaceDetection:
    def __init__(self, cascade_file="haarcascade_frontalface_default.xml"):
        self.face_cascade = cv2.CascadeClassifier(cascade_file)
        if self.face_cascade.empty():
            raise RuntimeError(f"Haar-Cascade-Datei {cascade_file} konnte nicht geladen werden")

    def detect(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return frame

# Klasse: GUI-Anwendung
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesichtserkennung mit Haar-Cascades")

        self.camera = CameraHandler()
        self.detector = FaceDetection()

        # GUI-Komponenten
        self.video_label = Label(root)
        self.video_label.pack()

        self.start_button = Button(root, text="Start", command=self.start_video)
        self.start_button.pack()

        self.stop_button = Button(root, text="Stop", command=self.stop_video)
        self.stop_button.pack()

        self.running = False

    def start_video(self):
        self.running = True
        self.update_frame()

    def stop_video(self):
        self.running = False

    def update_frame(self):
        if not self.running:
            return

        frame = self.camera.get_frame()
        frame = self.detector.detect(frame)

        # Konvertiere das Bild für Tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        self.root.after(10, self.update_frame)

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        self.running = False
        self.camera.release()
        self.root.destroy()

# Hauptprogramm
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.run()