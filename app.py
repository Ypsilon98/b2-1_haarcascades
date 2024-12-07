import cv2
from tkinter import Tk, Label, Canvas, Button, filedialog, StringVar, ttk
from PIL import Image, ImageTk
from cameramanager import CameraManager 
from classifiermanager import ClassifierManager

class App:
    def __init__(self, root):
        # Initialisiert die App und GUI-Komponenten.
        self.root = root
        self.root.title("Gesichtserkennung")

        # Manager-Instanzen
        self.camera_manager = CameraManager()
        self.classifier_manager = ClassifierManager()

        # GUI-Komponenten
        self.canvas = Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.info_label = Label(root, text="Gesichtserkennung: Live oder Bild auswählen")
        self.info_label.pack()

        self.mode_var = StringVar(value="live")  # Auswahl zwischen Live- und Datei-Modus
        self.mode_selector = ttk.Combobox(root, textvariable=self.mode_var, state="readonly")
        self.mode_selector["values"] = ["live", "file"]
        self.mode_selector.pack()

        self.btn_load_image = Button(root, text="Bild Laden", command=self.load_image_from_file)
        self.btn_load_image.pack()

        self.btn_start_camera = Button(root, text="Live-Bild Starten", command=self.start_camera)
        self.btn_start_camera.pack()

        self.btn_stop_camera = Button(root, text="Kamera Stoppen", command=self.stop_camera)
        self.btn_stop_camera.pack()

        self.btn_train_classifier = Button(root, text="Klassifizierer Trainieren", command=self.classifier_manager.train_classifier)
        self.btn_train_classifier.pack()

        self.face_count_label = Label(root, text="Erkannte Gesichter: 0")
        self.face_count_label.pack()

        # Variablen
        self.current_frame = None
        self.static_image = None  # Für Bilder aus Datei
        self.update_frame()  # Start initialer Frame-Loop

    def start_camera(self):
        # Startet die Kamera und den Live-Modus.
        camera_index = 0  # Default-Kamera
        try:
            self.camera_manager.start_camera(camera_index)
        except Exception as e:
            self.info_label.config(text=f"Kamera konnte nicht gestartet werden: {str(e)}")

    def stop_camera(self):
        # Stoppt die Kamera.
        self.camera_manager.stop_camera()
        self.static_image = None  # Falls ein Bild angezeigt wurde, wird es zurückgesetzt.

    def load_image_from_file(self):
        # Lädt ein Bild von der Festplatte und zeigt es an.
        file_path = filedialog.askopenfilename(title="Bild auswählen",
                                               filetypes=(("Bilder", "*.jpg;*.png;*.jpeg"), ("Alle Dateien", "*.*")))
        if file_path:
            image = cv2.imread(file_path)
            if image is not None:
                self.static_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def update_frame(self):
        # Aktualisiert den Bildrahmen und zeigt ihn an.
        if self.mode_var.get() == "live" and self.camera_manager.running:
            # Live-Modus
            frame = self.camera_manager.get_frame()
        elif self.mode_var.get() == "file" and self.static_image is not None:
            # Datei-Modus
            frame = self.static_image.copy()
        else:
            frame = None

        if frame is not None:
            # Gesichtserkennung
            faces = self.classifier_manager.detect_faces(frame)

            # Zeichne Rechtecke um Gesichter
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Konvertiere Frame für Tkinter
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, anchor="nw", image=photo)
            self.canvas.image = photo

            # Aktualisiere die Gesichteranzahl
            self.face_count_label.config(text=f"Erkannte Gesichter: {len(faces)}")

        # Nächsten Frame planen
        self.root.after(10, self.update_frame)



