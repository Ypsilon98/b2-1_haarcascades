from PySide6.QtWidgets import QApplication 
from app import App
from filemanager import FileManager

if __name__ == "__main__":
    
    app = QApplication([]) 
    window = App() 
    window.show() # Fenster (GUI) anzeigen 
    app.exec()  # Hauptschleife starten