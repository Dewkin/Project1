import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
import formulas

class CalculatorModel:
    def calculate(self, expression: str) -> str:
        """ Process the calculation based on the given expression. """
        try:
            text = expression.split()
            values = [float(val) for val in text if val not in ['+', '-', '*', '/']]
            if '+' in text:
                result = formulas.add(values)
            elif '-' in text:
                result = formulas.subtract(values)
            elif '*' in text:
                result = formulas.multiply(values)
            elif '/' in text:
                result = formulas.divide(values)
            else:
                result = 'Error'

            return str(int(result)) if result.is_integer() else f"{result:.2f}"
        except ValueError:
            return 'Invalid input'
        except Exception as e:
            return str(e)

class CalculatorView(QMainWindow):
    """ View for the Calculator GUI. """

    buttonClickedSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculator')
        self.setGeometry(100, 100, 300, 350)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setSpacing(0)

        self.input_line = QLineEdit(self)
        self.input_line.setReadOnly(True)
        self.grid_layout.addWidget(self.input_line, 0, 0, 1, 5)

        button_style = "background-color: #d3d3d3; min-height: 40px;"
        self.createButton('Clear', self.grid_layout, 1, 0, button_style)
        self.createButton('Del', self.grid_layout, 1, 1, button_style)

        numbers = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '0']
        positions = [(i, j) for i in range(2, 5) for j in range(3)] + [(5, 1)]
        for position, number in zip(positions, numbers):
            self.createButton(number, self.grid_layout, *position, button_style)

        self.createButton('+/-', self.grid_layout, 5, 0, button_style)
        self.createButton('.', self.grid_layout, 5, 2, button_style)

        operators = ['/', '*', '-', '+']
        for i, operator in enumerate(operators):
            self.createButton(operator, self.grid_layout, 1 + i, 4, button_style)

        self.createButton('=', self.grid_layout, 5, 4, button_style)

    def createButton(self, text, layout, row, col, style):
        button = QPushButton(text)
        button.setStyleSheet(style)
        button.clicked.connect(self.buttonClicked)
        layout.addWidget(button, row, col)

    def buttonClicked(self):
        button = self.sender()
        self.buttonClickedSignal.emit(button.text())

    def setDisplayText(self, text):
        self.input_line.setText(text)

    def getDisplayText(self):
        return self.input_line.text()

class CalculatorController:
    """ For managing interactions between Model and View. """

    def __init__(self):
        self.view = CalculatorView()
        self.model = CalculatorModel()
        self.view.buttonClickedSignal.connect(self.handleButtonClicked)

    def show(self):
        self.view.show()

    def handleButtonClicked(self, buttonText):
        if buttonText == 'Clear':
            self.view.setDisplayText('')
        elif buttonText == 'Del':
            current_text = self.view.getDisplayText()
            self.view.setDisplayText(current_text[:-1])
        elif buttonText == '+/-':
            self.toggleSign()
        elif buttonText == '=':
            result = self.model.calculate(self.view.getDisplayText())
            self.view.setDisplayText(result)
        else:
            current_text = self.view.getDisplayText()
            new_text = current_text + ' ' + buttonText + ' ' if buttonText in ['+', '-', '*', '/'] else current_text + buttonText
            self.view.setDisplayText(new_text)

    def toggleSign(self):
        current_text = self.view.getDisplayText().strip()
        if current_text:
            if current_text[-1].isdigit():
                parts = current_text.split(' ')
                last_number = parts[-1]
                if last_number.startswith('-'):
                    parts[-1] = last_number[1:]
                else:
                    parts[-1] = '-' + last_number
                self.view.setDisplayText(' '.join(parts))
            else:
                self.view.setDisplayText(current_text + ' -')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = CalculatorController()
    controller.show()
    sys.exit(app.exec())
