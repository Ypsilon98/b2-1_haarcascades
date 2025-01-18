import cv2
import os
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QComboBox, QStatusBar, QMessageBox
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy 
from PySide6.QtGui import QPixmap, QImage , QPainter, QColor, QAction
from PySide6.QtCore import QTimer, Qt, QRect
import numpy as np
from cameramanager import CameraManager
from classifiermanager import ClassifierManager
from filemanager import FileManager

# Hauptklasse App für GUI
class App(QMainWindow):
    """
    Hauptklasse für die GUI-Anwendung.

    Attribute:  camera_manager (CameraManager): Instanz des CameraManager.
                classifier_manager (ClassifierManager): Instanz des ClassifierManager.
                file_manager (FileManager): Instanz des FileManager.
                
                central_widget (QWidget): Zentrales Widget der Anwendung.
                menu_bar (QMenuBar): Menüleiste der Anwendung.
                image_display (QLabel): Anzeigebereich für Bilder/Kamera.
                animation_label (QLabel): Label für die Beispielanimation.
                camera_selector (QComboBox): Dropdown-Menü für Kameraauswahl.
                mode_selector (QComboBox): Dropdown-Menü für Modusauswahl.
                
                btn_refresh_cameras (QPushButton): Button zum Aktualisieren der Kameras.
                btn_load_image (QPushButton): Button zum Laden von Bildern.
                btn_start_camera (QPushButton): Button zum Starten/Stoppen der Kamera.
                classifier_selector (QComboBox): Dropdown-Menü für Klassifizierer.
                btn_choose_classifier (QPushButton): Button zum Laden von Klassifizierern.
                btn_train_classifier (QPushButton): Button zum Trainieren von Klassifizierern.
                btn_screenshot (QPushButton): Button zum Erstellen von Screenshots.

                num_objects (int): Anzahl der erkannten Gesichter.
                object_count_label (QLabel): Label für die Anzahl der erkannten Objekte.

                timer (QTimer): Timer für die Aktualisierung der Frames.
                animation_timer (QTimer): Timer für die Beispielanimation.

                current_frame (np.ndarray): Aktuelles Frame von der Kamera.
                static_image (np.ndarray): Statisches Bild aus Datei.

     Methoden:  __init__, animation, draw_haar_filter,toggle_fullscreen,toggle_nightmode, show_help,
                show_about, load_stylesheet, change_mode, refresh_camera_list, start_camera, stop_camera,
                start_stop_camera, load_image_from_file, update_frame, 
    """
    def __init__(self):
        # Initialisiert die GUI und die Manager-Instanzen.
        super().__init__()
        
        # Manager Instanzen
        self.camera_manager = CameraManager()
        self.classifier_manager = ClassifierManager()
        self.file_manager = FileManager()

        self.setWindowTitle("Objekterkennung mit Haarcascades")   # Fenstertitel
        self.setGeometry(100, 100, 1000, 700)  # Default Fenstergröße festlegen

        # Versuche Stylesheet zu laden
        try:    
            self.load_stylesheet("style_sheet.css")
            self.load_stylesheet("b2-1_haarcascades/style_sheet.css")
            self.i2 = cv2.imread("face_animation.jpg")
            self.i1 = cv2.imread("b2-1_haarcascades/face_animation.jpg")

        # Fehlerbehandlung beim Laden des Stylesheets
        except: 
            print("Fehler beim Laden des Stylesheets, stelle sicher das du im richtigen Verzeichnis ../b2-1_haarcascades/main.py startest")
        
        # Sicherstellen, dass App nicht abstürzt, wenn Bild nicht geladen werden kann
        if type(self.i1) != type(None):     
            self.image = QImage(self.i1.data, self.i1.shape[1], self.i1.shape[0], QImage.Format.Format_RGB888)
        elif type(self.i2) != type(None):    
            self.image = QImage(self.i2.data, self.i2.shape[1], self.i2.shape[0], QImage.Format.Format_RGB888)
        else: 
            self.image = QImage(250,250)
        
        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create the menu bar
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("Ansicht")
        self.fullscreen_action = QAction("Vollbild",self)
        self.fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(self.fullscreen_action)

        self.is_nightmode = False # Nachtmodus deaktiviert
        self.nightmode_action = QAction("Nachtmodus",self)
        self.nightmode_action.triggered.connect(self.toggle_nightmode)
        view_menu.addAction(self.nightmode_action)


        help_menu = menu_bar.addMenu("Info")
        help_action = QAction("Kurzanleitung",self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        about_action = QAction("Über", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        end_action = QAction("Beenden", self)
        end_action.triggered.connect(self.close)
        help_menu.addAction(end_action)

        # Main Layout
        debug_layout = QVBoxLayout(self.central_widget)
        main_layout = QHBoxLayout()
        debug_layout.addLayout(main_layout)
        self.status = QStatusBar()
        debug_layout.addWidget(self.status)
        
        # Kamera- und Bildanzeigebereich
        self.image_display = QLabel("Anzeigebereich für Bilder/Kamera")
        #self.image_display.setStyleSheet("background-color: #dcdcdc; border: 1px solid black;")
        self.image_display.setProperty("status", "display")
        self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_display.setMinimumSize(300,300)
        main_layout.addWidget(self.image_display)

        # Control Panel Layout
        control_panel = QVBoxLayout()

        # Info Label - Beispielanimation Haar Cascades
        self.animation_label = QLabel()
        self.pixmap = QPixmap(self.image)
        self.pixmap = self.pixmap.scaled(250, 250)
        self.x = 0
        self.y = 0
        self.random_int = np.random.randint(0, 5)
        self.animation_label.setPixmap(self.pixmap)
        self.animation_label.setMinimumWidth(250)
        self.animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_panel.addWidget(self.animation_label)

        # Kamera Dropdown Layout
        camera_layout = QHBoxLayout()
        self.camera_selector = QComboBox()
        self.camera_selector.addItem("Keine Kamera erkannt")
        camera_layout.addWidget(QLabel("Kamera:"))
        camera_layout.addWidget(self.camera_selector)

        self.btn_refresh_cameras = QPushButton("Kameras Aktualisieren")
        self.btn_refresh_cameras.clicked.connect(self.refresh_camera_list)
        control_panel.addWidget(self.btn_refresh_cameras)
        control_panel.addLayout(camera_layout)

        # Modus Auswahl Layout
        mode_layout = QHBoxLayout()
        self.mode_selector = QComboBox()
        self.mode_selector.setEnabled(True)
        self.mode_selector.addItems(["live", "file"])
        self.mode_selector.currentTextChanged.connect(self.change_mode)
        mode_layout.addWidget(QLabel("Modus:"))
        mode_layout.addWidget(self.mode_selector)
        #mode_layout.addWidget(QLabel(""))
        control_panel.addLayout(mode_layout)

        # Buttons Layout
        buttons_layout = QVBoxLayout()

        # Bild laden
        self.btn_load_image = QPushButton("Bild Laden")
        self.btn_load_image.setCheckable(True)
        self.btn_load_image.setEnabled(False)
        self.btn_load_image.clicked.connect(self.load_reset_file)
        buttons_layout.addWidget(self.btn_load_image)

        self.btn_start_camera = QPushButton("Live-Kamera Starten")
        self.btn_start_camera.setCheckable(True)
        self.btn_start_camera.setEnabled(False)
        self.btn_start_camera.clicked.connect(self.start_stop_camera)
        buttons_layout.addWidget(self.btn_start_camera)
        
    
        classifier_layout = QHBoxLayout()
        self.classifier_selector = QComboBox()
        self.classifier_selector.setEnabled(True)
        self.classifier_selector.addItems(["face", "eye", "smile", "upperbody", "fullbody", "profileface", "Eigener Klassifizierer"])
        self.classifier_selector.setCurrentText("face")
        self.classifier_selector.currentTextChanged.connect(self.change_classifier)
        classifier_layout.addWidget(QLabel("Klassifizierer:"))
        classifier_layout.addWidget(self.classifier_selector)
        buttons_layout.addLayout(classifier_layout)

        self.btn_choose_classifier = QPushButton("Eigener Klassifizierer Laden")
        self.btn_choose_classifier.setEnabled(False)
        self.btn_choose_classifier.clicked.connect(self.classifier_manager.load_custom_classifier)
        buttons_layout.addWidget(self.btn_choose_classifier)
        #control_panel.addLayout(buttons_layout)

        self.btn_train_classifier = QPushButton("Klassifizierer Trainieren")
        self.btn_train_classifier.setEnabled(False)
        #self.btn_train_classifier.clicked.connect(self.classifier_manager.train_classifier)
        buttons_layout.addWidget(self.btn_train_classifier)

        self.btn_screenshot = QPushButton("Screenshot")
        self.btn_screenshot.setEnabled(False)
        buttons_layout.addWidget(self.btn_screenshot)
        control_panel.addLayout(buttons_layout)

        # Erkannte Objekte Label
        objects_layout = QHBoxLayout()
        self.num_objects = 0 # Anzahl der erkannten Objekte
        self.object_count_label = QLabel("")
        self.object_count_label.setText(f"<a style=\"text-decoration:none;\" href=\"http://www.easteregg.com\"> {self.num_objects} </a>")
        self.object_count_label.setOpenExternalLinks(True)
        self.object_count_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.object_count_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.object_count_label.setStyleSheet("font-weight: bold;")
        objects_layout.addWidget(QLabel("Erkannte Objekte: "))
        objects_layout.addWidget(self.object_count_label)
        control_panel.addLayout(objects_layout)

        main_layout.addLayout(control_panel)

        # Timer für die Aktualisierung der Frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Timer für Beispielanimation
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animation)
        self.animation_timer.start(50)  # Animationsgeschwindigkeit in ms

        # Variablen
        self.current_frame = None
        self.static_image = None

        # Kameraliste bei Programmstart aktualisieren
        self.btn_refresh_cameras.click()
        self.change_mode(self.mode_selector.currentText())

    # Animiert die Haar Cascade Features
    def animation(self):
        
        if self.x + 60 >= 250:
            self.x = 0
            self.y += 60
            self.random_int = np.random.randint(0, 5)

        if self.y + 60 >= 250:
            self.x = 0
            self.y = 0
            
        self.x += 10
        self.draw_haar_filter()
        pass

    # Zeichnet Haar Cascade Features
    def draw_haar_filter(self):

        overlay_pixmap = self.pixmap.copy()
        painter = QPainter(overlay_pixmap)
        x, y = self.x, self.y

        if self.random_int == 0:
            painter.fillRect(QRect(x,      y, 20, 60), QColor("white"))
            painter.fillRect(QRect(x + 20, y, 20, 60), QColor("black"))
            painter.fillRect(QRect(x + 40, y, 20, 60), QColor("white"))
        elif self.random_int == 1:
            painter.fillRect(QRect(x, y,      60, 20), QColor("white"))
            painter.fillRect(QRect(x, y + 20, 60, 20), QColor("black"))
            painter.fillRect(QRect(x, y + 40, 60, 20), QColor("white"))
        elif self.random_int == 2:
            painter.fillRect(QRect(x     , y     , 30, 30), QColor("white"))
            painter.fillRect(QRect(x + 30, y     , 30, 30), QColor("black"))
            painter.fillRect(QRect(x     , y + 30, 30, 30), QColor("white"))
            painter.fillRect(QRect(x + 30, y + 30, 30, 30), QColor("black"))
        elif self.random_int == 3:
            painter.fillRect(QRect(x     , y     , 30, 30), QColor("white"))
            painter.fillRect(QRect(x + 30, y     , 30, 30), QColor("white"))
            painter.fillRect(QRect(x     , y + 30, 30, 30), QColor("black"))
            painter.fillRect(QRect(x + 30, y + 30, 30, 30), QColor("black"))
        elif self.random_int == 4:
            painter.fillRect(QRect(x     , y     , 30, 30), QColor("white"))
            painter.fillRect(QRect(x + 30, y     , 30, 30), QColor("black"))
            painter.fillRect(QRect(x     , y + 30, 30, 30), QColor("black"))
            painter.fillRect(QRect(x + 30, y + 30, 30, 30), QColor("white"))
        else:
            painter.fillRect(QRect(x     , y     , 30, 30), QColor("black"))
            painter.fillRect(QRect(x + 30, y     , 30, 30), QColor("white"))
            painter.fillRect(QRect(x     , y + 30, 30, 30), QColor("white"))
            painter.fillRect(QRect(x + 30, y + 30, 30, 30), QColor("black"))

        painter.end()
        self.animation_label.setPixmap(overlay_pixmap)

    # Schaltet zwischen Vollbildmodus und Fenstermodus um.
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_action.setText("Vollbild")
        else:
            self.showFullScreen()
            self.fullscreen_action.setText("Fenstermodus")
        pass
    
    # Schaltet zwischen Nachtmodus und Tagmodus (stylesheets) um.
    def toggle_nightmode(self):
        # Versuche Stylesheet zu laden
        if self.is_nightmode:
            try:    
                self.load_stylesheet("style_sheet.css")
                self.load_stylesheet("b2-1_haarcascades/style_sheet.css")
            # Fehlerbehandlung beim Laden des Stylesheets
            except: 
                print("Fehler beim Laden des Stylesheets, stelle sicher das du im richtigen Verzeichnis ../b2-1_haarcascades/main.py startest")
            self.nightmode_action.setText("Nachtmodus")
        else:
            try:    
                self.load_stylesheet("night_mode.css")
                self.load_stylesheet("b2-1_haarcascades/night_mode.css")
            # Fehlerbehandlung beim Laden des Stylesheets
            except: 
                print("Fehler beim Laden des Stylesheets, stelle sicher das du im richtigen Verzeichnis ../b2-1_haarcascades/main.py startest")
            self.nightmode_action.setText("Tagmodus")
        # Update the night mode state
        self.is_nightmode = not self.is_nightmode   
        pass
    
    def show_help(self):
        QMessageBox.about(self, "Kurzanleitung",  "Kamera und Modus auswählen und auf Live-Kamera Starten klicken.\n\nAlternativ Modus auf 'file' setzen und Bild Laden.\n\nObjekte werden automatisch erkannt, markiert und gezählt.\n\nVortrainierte als auch eigene Klassifizierer können geladen werden.\n\nDazu einfach den entsprechenden Button klicken und die XML-Datei auswählen.\n\nViel Spaß!")

    def show_about(self):
        QMessageBox.about(self, "Über", "Anwendung zur Objekterkennung mit Haarcascades\n\nProgrammiert von der Projektgruppe B2-1 im Master AKI an der FH SWF Iserlohn\n\nYannick\nEmilie\nLeon\nPhilipp\n\nJanuar 2025")

    # Lädt ein Stylesheet aus einer Datei.
    # Parameters: filename (str): Dateiname des Stylesheets.
    def load_stylesheet(self, filename):

        try:
            with open(filename, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Error: Stylesheet file '{filename}' not found.")

    # Ändert den Modus basierend auf der Auswahl im Dropdown-Menü.
    def change_mode(self, text):
        
        if text == "live":
            self.btn_start_camera.setEnabled(True)
            self.btn_start_camera.setProperty("status","start")
            self.btn_start_camera.style().unpolish(self.btn_start_camera) 
            self.btn_start_camera.style().polish(self.btn_start_camera)    
            self.btn_load_image.setEnabled(False)
            self.btn_load_image.setProperty("status","unavailable")
            self.btn_load_image.style().unpolish(self.btn_load_image)
            self.btn_load_image.style().polish(self.btn_load_image)
            self.reset_image()
        elif text == "file":
            self.btn_start_camera.setEnabled(False)
            self.btn_start_camera.setProperty("status", "unavailable")
            self.btn_start_camera.style().unpolish(self.btn_start_camera)
            self.btn_start_camera.style().polish(self.btn_start_camera)
            self.btn_load_image.setEnabled(True)
            self.btn_load_image.setProperty("status","start")
            self.btn_load_image.style().unpolish(self.btn_load_image)
            self.btn_load_image.style().polish(self.btn_load_image)
        else:
            self.btn_start_camera.setEnabled(False)
            self.btn_load_image.setEnabled(False)
        pass
    
    def change_classifier(self, text):
        self.btn_choose_classifier.setEnabled(False)
        if text == "face":
            self.classifier_manager.load_classifier("face")
        elif text == "eye":
            self.classifier_manager.load_classifier("eye")
        elif text == "smile":
            self.classifier_manager.load_classifier("smile")
        elif text == "upperbody":
            self.classifier_manager.load_classifier("upperbody")
        elif text == "fullbody":
            self.classifier_manager.load_classifier("fullbody")
        elif text == "profileface":
            self.classifier_manager.load_classifier("profileface")
        elif text == "Eigener Klassifizierer":
            self.btn_choose_classifier.setEnabled(True)
        else:
            self.classifier_manager.load_classifier("face")
        pass

    # Aktualisiert die Liste der verfügbaren Kameras.
    def refresh_camera_list(self):
        
        available_cameras = self.camera_manager.detect_cameras()
        self.camera_selector.clear()
        if available_cameras:
            camera_names = [f"Kamera {index}" for index in available_cameras]
            self.camera_selector.addItems(camera_names)
            self.status.showMessage(f"Kameras gefunden: {camera_names}")
            self.btn_start_camera.setEnabled(True)
            self.btn_start_camera.setProperty("status","start")
            self.btn_start_camera.style().unpolish(self.btn_start_camera)  # Reset style
            self.btn_start_camera.style().polish(self.btn_start_camera)    # Reapply style
        else:
            self.camera_selector.addItem("Keine Kamera erkannt")
            self.status.showMessage("Keine Kameras gefunden.")
            self.btn_start_camera.setEnabled(False) # Bug: setEnable ändert Button-Style nicht automatisch"
            self.btn_start_camera.setProperty("status", "unavailable")
            self.btn_start_camera.style().unpolish(self.btn_start_camera)
            self.btn_start_camera.style().polish(self.btn_start_camera)
            
        pass

    # Startet die Kamera.   
    def start_camera(self):
        
        camera_index = self.camera_selector.currentIndex()  # Kamera-Index auswählen
        try:
            self.btn_refresh_cameras.setEnabled(False)
            self.camera_selector.setEnabled(False)
            self.mode_selector.setEnabled(False)
            self.classifier_selector.setEnabled(False)
            self.btn_start_camera.setProperty("status","stop")
            self.btn_start_camera.style().unpolish(self.btn_start_camera)  # Reset style
            self.btn_start_camera.style().polish(self.btn_start_camera)    # Reapply style
            self.btn_start_camera.setText("Live-Kamera Stoppen")
            self.camera_manager.start_camera(camera_index)
            print(f"Kamera {camera_index} erfolgreich gestartet.")
            self.status.showMessage(f"Kamera {camera_index} erfolgreich gestartet.")
            self.timer.start(10)  # Update alle 10 ms
        except Exception as e:
            self.animation_label.setText(f"Kamera konnte nicht gestartet werden: {str(e)}")
            self.status.showMessage(f"Kamera-Fehler: {str(e)}")
        pass
    
    # Stoppt die Kamera.
    def stop_camera(self):

        self.btn_refresh_cameras.setEnabled(True)
        self.btn_start_camera.setProperty("status","start")
        self.btn_start_camera.style().unpolish(self.btn_start_camera)  # Reset style
        self.btn_start_camera.style().polish(self.btn_start_camera)    # Reapply style
        self.btn_start_camera.setText("Live-Kamera Starten")
        self.camera_selector.setEnabled(True)
        self.classifier_selector.setEnabled(True)
        self.mode_selector.setEnabled(True)
        self.status.showMessage("Kamera wird gestoppt...")
        self.camera_manager.stop_camera()
        self.timer.stop()
        self.num_objects = 0 # Anzahl der erkannten Objekte auf 0 zurücksetzen
        self.object_count_label.setText(f"<a style=\"text-decoration:none;\" href=\"http://www.easteregg.com\"> {self.num_objects} </a>")

        self.image_display.clear()  # Clear the pixmap from the label
        self.image_display.setText("Anzeigebereich für Bilder/Kamera")  # Optionale Standardnachricht
        self.status.showMessage("Kamera gestoppt.")
        pass


    # Startet oder stoppt die Kamera, je nach Status des Buttons.
    def start_stop_camera(self,checked):

        #self.btn_start_camera.isChecked():
        if checked:                 
            self.start_camera()
            print("Kamera gestartet")
        else:
            self.stop_camera()
            print("Kamera gestartet")
        pass

    
    # Lädt ein Bild aus einer Datei.
    def load_image_from_file(self):
       
        file_path = self.file_manager.open_file_picture()
        if file_path:
            self.static_image = self.file_manager.load_image(file_path)
            self.static_image = cv2.cvtColor(self.static_image, cv2.COLOR_BGR2RGB) # OpenCV (standard) BGR, Umwandlung in RGB
            self.btn_start_camera.setEnabled(False)
            self.timer.start(50)

    # Setzt das Bild zurück.
    def reset_image(self):
        self.static_image = None
        self.timer.start(50)

        

    # Lädt ein Bild aus einer Datei und setzt den Button zurück.
    def load_reset_file(self, checked):

        if checked:
            self.load_image_from_file()
            print("Bild laden...")
        else:
            self.reset_image()
            print("Bild zurücksetzen...")
        pass

    # Holt ein Frame von der Kamera und zeigt es in der GUI an. 
    def update_frame(self):
        if self.mode_selector.currentText() == "live":
            frame, ret = self.camera_manager.get_frame()
            if not ret: # Wenn Kamera keine Frames mehr liefert/disconnected, stoppe Kamera und aktualisiere Kamera-Liste
                self.stop_camera()
                self.refresh_camera_list()
                self.btn_start_camera.setChecked(False)
                return  
        
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # OpenCV (standard) BGR, Umwandlung in RGB

            # Objekterkennung
            objects = self.classifier_manager.detect_faces(frame)
            self.num_objects = len(objects) # Anzahl der erkannten Objekte
            self.object_count_label.setText(f"<a style=\"text-decoration:none;\" href=\"http://www.easteregg.com\"> {self.num_objects} </a>")
                
            # Zeichne grüne Rechtecke um erkannte Gesichter
            for (x, y, w, h) in objects:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Zeichne grünes Rechteck um Objekt

            height, width, channel = frame.shape # Größe des Frames
            aspect_ratio = height/width # Seitenverhältnis
            bytes_per_line = 3 * width  # 3 Kanäle pro Pixel (RGB)

            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888) # Erstelle QImage aus Frame 
            pixmap = QPixmap.fromImage(q_image) # Erstelle Pixmap aus QImage

            # Logik für das Skalieren des Bildes
            i_h = self.image_display.height() # Höhe des QLabel(image_display)
            w_asp = int(i_h * (width/height)) # Berechne Breite des Bildes basierend auf Höhe und Seitenverhältnis
            if(w_asp <= self.image_display.width()): 
                i_w = w_asp 
            else:
                i_w = self.image_display.width()
                i_h = int(i_w * aspect_ratio)
            scaled_pixmap = pixmap.scaled(i_w,i_h) 
            self.image_display.setPixmap(scaled_pixmap) # Setze Pixmap in QLabel(image_display)

        elif self.mode_selector.currentText() == "file":
            
            frame = self.static_image
            # Objekterkennung
            objects = self.classifier_manager.detect_faces(frame)
            self.num_objects = len(objects) # Anzahl der erkannten Objekte
            self.object_count_label.setText(f"<a style=\"text-decoration:none;\" href=\"http://www.easteregg.com\"> {self.num_objects} </a>")
                
            # Zeichne grüne Rechtecke um erkannte Gesichter
            for (x, y, w, h) in objects:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Zeichne grünes Rechteck um Objekt

            height, width, channel = frame.shape # Größe des Frames
            aspect_ratio = height/width # Seitenverhältnis
            bytes_per_line = 3 * width  # 3 Kanäle pro Pixel (RGB)

            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888) # Erstelle QImage aus Frame 
            pixmap = QPixmap.fromImage(q_image) # Erstelle Pixmap aus QImage

            # Logik für das Skalieren des Bildes
            i_h = self.image_display.height() # Höhe des QLabel(image_display)
            w_asp = int(i_h * (width/height)) # Berechne Breite des Bildes basierend auf Höhe und Seitenverhältnis
            if(w_asp <= self.image_display.width()): 
                i_w = w_asp 
            else:
                i_w = self.image_display.width()
                i_h = int(i_w * aspect_ratio)
            scaled_pixmap = pixmap.scaled(i_w,i_h) 
            self.image_display.setPixmap(scaled_pixmap) # Setze Pixmap in QLabel(image_display)         
        pass