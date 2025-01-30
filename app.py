import sys
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QLabel, QDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal, QObject

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")

        # Label
        self.label = QLabel("Hello!")

        # # Button
        # self.button = QPushButton("Open New Window")
        # self.button.clicked.connect(self.open_new_window)

        self.button = QPushButton("Set Coordinates")  # Changed button text
        self.button.clicked.connect(self.open_coordinates_window) # Connect to new method

        # Layout
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label)
        v_layout.addWidget(self.button)

        central_widget = QWidget()
        central_widget.setLayout(v_layout)
        self.setCentralWidget(central_widget)

        self.new_window = NewWindow()
        self.new_window.back_signal.connect(self.show)

    def open_new_window(self):
        new_window = NewWindow()
        new_window.exec()  # Use exec() to make it a modal dialog
    
    def open_coordinates_window(self):
        try:
            python_path = "D:\\headdatset\\headvenv\\Scripts\\python.exe"
            subprocess.Popen([python_path, "coordinates.py"])  # Run coordinates.py
            self.hide() # Hide main window
            self.new_window.exec()  # Show the dialog (still needed)
            
            # new_window = NewWindow()
            # new_window.exec()

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "coordinates.py not found.") # Error message box
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open coordinates window: {e}") # More general error handling


class NewWindow(QDialog):  # Use QDialog for a simple popup window
    back_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Window")
        label = QLabel("This is a new window!")
        back_button = QPushButton("Back to Main Window")
        back_button.clicked.connect(self.emit_back_signal) # Emit signal on click

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def emit_back_signal(self):
        self.back_signal.emit() # Emit the signal
        self.close() # Close the dialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())