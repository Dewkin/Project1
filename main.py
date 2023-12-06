import sys
from PyQt6.QtWidgets import QApplication
from gui import CalculatorController

# Main entry point for the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = CalculatorController()
    controller.show()
    sys.exit(app.exec())
