import sys
import subprocess
import threading
import json # For sending data
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QLabel, QDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal, QObject

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")

        self.new_window = NewWindow()
        self.new_window.back_signal.connect(self.show)
        self.new_window.coordinates_received.connect(self.handle_coordinates)

        # Central Widget and Layout
        central_widget = QWidget()  # Create a central widget
        main_layout = QVBoxLayout()  # Create a layout for the central widget

        self.label = QLabel("Hello!")
        self.button = QPushButton("Set Coordinates")
        self.button.clicked.connect(self.open_coordinates_window)

        main_layout.addWidget(self.label)
        main_layout.addWidget(self.button)

        self.coordinates_label = QLabel("Coordinates will be displayed here") # Label for coordinates
        main_layout.addWidget(self.coordinates_label)

        central_widget.setLayout(main_layout)  # Set the layout on the central widget
        self.setCentralWidget(central_widget)
        
    def handle_coordinates(self, coordinates): # This function will be called when signal is emited
        print("Coordinates received in MainWindow:", coordinates)
        
        if hasattr(self, 'coordinates_label'):  # Check if the label exists
            self.coordinates_label.setText(str(coordinates))

    # def open_new_window(self):
    #     new_window = NewWindow()
    #     new_window.exec()  # Use exec() to make it a modal dialog
    
    def open_coordinates_window(self):
        try:
            python_path = "D:\\headdatset\\headvenv\\Scripts\\python.exe"
            process = subprocess.Popen([python_path, "coordinates.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)  # Run coordinates.py
            self.hide() # Hide main window
            self.new_window.exec()  # Show the dialog (still needed)
            
            # new_window = NewWindow()
            # new_window.exec()
            def read_output(pipe, target):
                for line in iter(pipe.readline, ''):
                    target(line.strip())
                pipe.close()

            def process_stdout(line):
                try:
                    # Attempt to parse as JSON. If it fails, it's not the coordinates output.
                    data = json.loads(line) # Coordinates are sent as JSON
                    if isinstance(data, list) and len(data) == 4 and all(isinstance(point, list) and len(point) == 2 for point in data): # Check if it is in the correct format
                        print("Received coordinates:", data)
                        self.new_window.coordinates_received.emit(data) # Emit the signal with the coordinates
                    else:
                        print(isinstance(data, list))
                        print(len(data))
                        all(isinstance(point, list) and len(point) == 2 for point in data)
                        
                        print("else coordinates.py (stdout):", line) # Print other output
                        self.new_window.output_label.setText(line) # Example: put the output in the dialog label
                except json.JSONDecodeError:
                    print("coordinates.py (stdout):", line) # If not JSON, just print it
                    self.new_window.output_label.setText(line) # Example: put the output in the dialog label

            def process_stderr(line):
                print("coordinates.py (stderr):", line)

            stdout_thread = threading.Thread(target=read_output, args=(process.stdout, process_stdout))
            stderr_thread = threading.Thread(target=read_output, args=(process.stderr, process_stderr))
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            stdout_thread.start()
            stderr_thread.start()

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "coordinates.py not found.") # Error message box
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open coordinates window: {e}") # More general error handling


class NewWindow(QDialog):  # Use QDialog for a simple popup window
    back_signal = pyqtSignal()
    coordinates_received = pyqtSignal(list) 

    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Window")
        label = QLabel("This is a new window!")
        back_button = QPushButton("Back to Main Window")
        back_button.clicked.connect(self.emit_back_signal) # Emit signal on click
        
        layout = QVBoxLayout()
        self.output_label = QLabel("Output from coordinates.py will appear here.")
        layout.addWidget(self.output_label)
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