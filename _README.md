# b2-1_haarcascades
B2-1 Gruppenarbeit PRO-KI „Bilderkennung mit Haar-Cascades"
Owner: Yannic Müller
Group B2-1: Yannic Müller, Emelie Nagel, Leon Kaufhold, Philipp Zinder

Git Repository: https://github.com/Ypsilon98/b2-1_haarcascades

Projektaufgabe: Eine Softwareanwendung mit Bild Erkennung unter Verwendung von Haarcascades programmieren

Ziel: Eine einfache Kamera-App, die Haarcascades verwendet, um Gesichter oder andere Objekte zu erkennen. 

Funktionen:
- Live-Kamera mit Echtzeit-Objekterkennung mit vortrainierten Haarcascades
- Hochladen von Bildern und Objekterkennung mit Haarcascades
- Screenshot der Objekterkennung und Speichern der Screenshots
- Auswahl der Objekterkennung (face, smile, eye, upper body, full body, profile face) oder hochladen eines eigenen Klassifizierers mittels .xml Datei
- Darkmode und Vollbild möglich
- Schieberegler für eigene Klassifizierer zur Einstellung von scaleFactor, minNeighbours, minSize

Voraussetzungen:
- Betriebssystem: Windows, macOS, Linux (eingeschränkt)
- Python: Version 3.x

Zu installierende Bibliotheken (inkl. Installationsbefehle):
- OpenCV: pip install opencv-python
- NumPy: pip install numpy
- PySide6: pip install PySide6
- tkinter: pip Install tk Alternativ: sudo apt-get install python3-tk #Linux , brew install python-tk #macOS
 
Start der Anwendung:
python main.py #Windows/macOS
QT_QPA_PLATFORM=xcb python main.py #Linux



