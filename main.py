#from tkinter import Tk
from PySide6.QtWidgets import QApplication
from app import App

if __name__ == "__main__":
    
    app = QApplication([])
    window = App()
    window.show()   # GUI Anzeigen # Show the window maximized
    app.exec()  # Hauptschleife starten
    #root = Tk()
    #app = TestApp(root)
    #root.mainloop()