import cv2
from tkinter import Label, Canvas, Button, filedialog, StringVar, ttk
from PIL import Image, ImageTk
from cameramanager import CameraManager
from classifiermanager import ClassifierManager
from filemanager import FileManager


class App:
    def __init__(self, root):
        pass

    def refresh_camera_list(self):
        # Aktualisiert die Kameraliste und zeigt verfügbare Kameras an.
        available_cameras = self.camera_manager.detect_cameras()
        if available_cameras:
            camera_names = [f"Kamera {index}" for index in available_cameras]
            self.camera_selector["values"] = camera_names
            self.camera_selector.current(0)
            print(f"Kameras gefunden: {camera_names}")
        else:
            self.camera_selector["values"] = ["Keine Kamera erkannt"]
            self.camera_selector.current(0)
            print("Keine Kameras gefunden.")
            
    def start_camera(self):
        # Startet die Kamera und den Live-Modus.
        print("Versuche, die Kamera zu starten...")
        camera_index = 0  # Default-Kamera
        try:
            self.camera_manager.start_camera(camera_index)
            print(f"Kamera {camera_index} erfolgreich gestartet.")
            self.update_frame() # Startet die Frame-Aktualisierung
        except Exception as e:
            self.info_label.config(text=f"Kamera konnte nicht gestartet werden: {str(e)}")
            print(f"Kamera-Fehler: {str(e)}")

    def stop_camera(self):
        # Stoppt die Kamera.
        print("Kamera wird gestoppt...")
        self.camera_manager.stop_camera()
        self.static_image = None  # Falls ein Bild angezeigt wurde, wird es zurückgesetzt.
        print("Kamera gestoppt.")

    def load_image_from_file(self):
        # Lädt ein Bild von der Festplatte und zeigt es an.
        print("Lade Bild von Datei...")

        file_path = self.file_manager.open_file_dialog(title="Bild auswählen")
        
        if file_path:
            image = cv2.imread(file_path)
            if image is not None:
                self.static_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                print(f"Bild {file_path} erfolgreich geladen.")
                self.update_frame()  # Bild anzeigen
            else:
                print(f"Fehler: Bild {file_path} konnte nicht gelesen werden.")
        else:
            print("Kein Bild ausgewählt.")

    def update_frame(self):
        # Holt ein Frame von der Kamera und zeigt es in der GUI an.
        if self.mode_var.get() == "live":
            ret, frame = self.camera_manager.get_frame()
            if ret:
                frame_height, frame_width = frame.shape[:2]
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()

                # Gesichtserkennung
                faces = self.classifier_manager.detect_faces(frame)
                num_faces = len(faces)

                # Zeichne grüne Rechtecke um erkannte Gesichter
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Berechnung der Skalierung unter Beibehaltung des Seitenverhältnisses
                scale = min(canvas_width / frame_width, canvas_height / frame_height)
                new_width = int(frame_width * scale)
                new_height = int(frame_height * scale)

                # Frame skalieren und konvertieren
                frame_resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
                frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)

                # Canvas zurücksetzen und Bild anzeigen
                self.canvas.delete("all")
                self.canvas.create_image(
                    canvas_width // 2, canvas_height // 2, anchor="center", image=imgtk
                )
                self.canvas.image = imgtk  # Referenz behalten

                # Gesichtszahl aktualisieren, falls sie sich ändert
                if not hasattr(self, "last_face_count") or self.last_face_count != num_faces:
                    self.face_count_label.config(text=f"Erkannte Gesichter: {num_faces}")
                    self.last_face_count = num_faces
            elif ret is False:
                self.canvas.delete("all")

        elif self.mode_var.get() == "file" and self.static_image is not None:
            # Bild vom Dateipfad anzeigen
            img = Image.fromarray(self.static_image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.delete("all")
            self.canvas.create_image(
                self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, 
                anchor="center", image=imgtk
            )
            self.canvas.image = imgtk  # Referenz behalten

        # Nächsten Frame planen
        self.root.after(10, self.update_frame)  # Alle 10 ms ein neuer Frame