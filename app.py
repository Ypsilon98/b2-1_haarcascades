import cv2
#from tkinter import Label, Canvas, Button, filedialog, StringVar, ttk
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QSizePolicy
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer, Qt
import numpy as np
from PIL import Image, ImageTk
from cameramanager import CameraManager
from classifiermanager import ClassifierManager
from filemanager import FileManager

# Hauptklasse App für GUI
class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gesichtserkennung")

        # Manager Instanzen
        self.camera_manager = CameraManager()
        #self.classifier_manager = ClassifierManager()
        #self.file_manager = FileManager()
        # Set the minimum window size (width, height)
        self.setMinimumSize(300, 300)  # Minimum size is 800x600 pixels
        self.setGeometry(100, 100, 1000, 700)  # Default window size

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        main_layout = QVBoxLayout(self.central_widget)

        # Image/Camera Display Area
        self.image_display = QLabel("Live/Loaded Image Display Area")
        self.image_display.setStyleSheet("background-color: #dcdcdc; border: 1px solid black;")
        self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.image_display)

        # Control Panel Layout
        control_panel = QVBoxLayout()

        # Info Label
        self.info_label = QLabel("Gesichtserkennung: Live oder Bild auswählen")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_panel.addWidget(self.info_label)

        # Camera Selector Layout
        camera_layout = QHBoxLayout()
        self.camera_selector = QComboBox()
        self.camera_selector.addItem("Keine Kamera erkannt")
        camera_layout.addWidget(QLabel("Kamera:"))
        camera_layout.addWidget(self.camera_selector)

        self.btn_refresh_cameras = QPushButton("Kameras Aktualisieren")
        self.btn_refresh_cameras.clicked.connect(self.refresh_camera_list)
        camera_layout.addWidget(self.btn_refresh_cameras)
        control_panel.addLayout(camera_layout)

        # Mode Selector
        mode_layout = QHBoxLayout()
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["live", "file"])
        mode_layout.addWidget(QLabel("Modus:"))
        mode_layout.addWidget(self.mode_selector)
        control_panel.addLayout(mode_layout)

        # Buttons Layout
        buttons_layout = QGridLayout()
        # Bild laden
        self.btn_load_image = QPushButton("Bild Laden")
        #self.btn_load_image.clicked.connect(self.load_image_from_file)
        buttons_layout.addWidget(self.btn_load_image, 0, 0)

        self.btn_start_camera = QPushButton("Live-Bild Starten")
        self.btn_start_camera.clicked.connect(self.start_camera)
        buttons_layout.addWidget(self.btn_start_camera, 0, 1)

        # Kamera Stoppen
        self.btn_stop_camera = QPushButton("Kamera Stoppen")
        self.btn_stop_camera.clicked.connect(self.stop_camera)
        buttons_layout.addWidget(self.btn_stop_camera, 1, 0)

        self.btn_train_classifier = QPushButton("Klassifizierer Trainieren")
        #self.btn_train_classifier.clicked.connect(self.classifier_manager.train_classifier)
        buttons_layout.addWidget(self.btn_train_classifier, 1, 1)
        control_panel.addLayout(buttons_layout)

        # Face Count Label
        self.face_count_label = QLabel("Erkannte Gesichter: 0")
        self.face_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        control_panel.addWidget(self.face_count_label)

        # Add Control Panel to Main Layout
        main_layout.addLayout(control_panel)

        # Stretch Factors
        main_layout.setStretch(0, 5)  # Image display gets the most space
        main_layout.setStretch(1, 2)  # Control panel takes less space

        # Timer for Updating Frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Variables
        self.current_frame = None
        self.static_image = None

        # Automatically refresh camera list when the GUI starts
        self.btn_refresh_cameras.click()

    def refresh_camera_list(self):
        # Aktualisiert die Kameraliste und zeigt verfügbare Kameras an.
        available_cameras = self.camera_manager.detect_cameras()
        self.camera_selector.clear()
        if available_cameras:
            camera_names = [f"Kamera {index}" for index in available_cameras]
            self.camera_selector.addItems(camera_names)
            print(f"Kameras gefunden: {camera_names}")
        else:
            self.camera_selector.addItem("Keine Kamera erkannt")
            print("Keine Kameras gefunden.")
        pass
            
    def start_camera(self):
        # Startet die Kamera und den Live-Modus.
        print("Versuche, die Kamera zu starten...")
        camera_index = 0  # Default-Kamera
        try:
            self.camera_manager.start_camera(camera_index)
            print(f"Kamera {camera_index} erfolgreich gestartet.")
            self.timer.start(10)  # Update every 10 ms
        except Exception as e:
            self.info_label.setText(f"Kamera konnte nicht gestartet werden: {str(e)}")
            print(f"Kamera-Fehler: {str(e)}")
        pass

    def stop_camera(self):
        # Stoppt die Kamera.
        print("Kamera wird gestoppt...")
        self.camera_manager.stop_camera()
        self.timer.stop()
        self.image_display.clear()  # Clear the pixmap from the label
        self.image_display.setText("Live/Loaded Image Display Area")  # Optionally set a default message
        print("Kamera gestoppt.")
        pass

    def load_image_from_file(self):
        # Lädt ein Bild von der Festplatte und zeigt es an.
        pass

    def update_frame(self):
        # Holt ein Frame von der Kamera und zeigt es in der GUI an.
         # Get frame from the camera if we're in live mode
        if self.mode_selector.currentText() == "live":
            frame, ret = self.camera_manager.get_frame()
            if not ret:
                return  # If no frame, do nothing

        # Convert the frame from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to QImage
        height, width, channel = frame.shape

        aspect_ratio = width / height


        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        # Assuming q_image is your QImage object
        pixmap = QPixmap.fromImage(q_image)

        i_h = self.image_display.height()

        # Get the size of the image display widget
        h = (i_h // 100) * 100 
        w = int(h * aspect_ratio)

        # Scale the pixmap to fit the display size
        scaled_pixmap = pixmap.scaled(w,h)

        # Set the scaled pixmap to the image display
        self.image_display.setPixmap(scaled_pixmap)
        pass