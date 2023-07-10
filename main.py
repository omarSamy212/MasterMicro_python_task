import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from sympy import symbols, lambdify, SympifyError


class FunctionPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setMinimumWidth(400)

        # Create input widgets
        self.input_label = QLabel("Enter function:")
        self.input_lineedit = QLineEdit()
        self.min_label = QLabel("Min value of x:")
        self.min_lineedit = QLineEdit()
        self.max_label = QLabel("Max value of x:")
        self.max_lineedit = QLineEdit()

        # Create plot button and connect it to plot_function method
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_function)

        # Create layout for input widgets
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_lineedit)

        # Create layout for range input widgets
        range_layout = QHBoxLayout()
        range_layout.addWidget(self.min_label)
        range_layout.addWidget(self.min_lineedit)
        range_layout.addWidget(self.max_label)
        range_layout.addWidget(self.max_lineedit)

        # Create main layout and add input and range layouts
        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(range_layout)
        main_layout.addWidget(self.plot_button)

        # Create central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def validate_input(self, function_str, min_value, max_value):
        # Validate function input
        if not function_str:
            QMessageBox.warning(self, "Input Error", "Please enter a function.")
            return False

        try:
            x = symbols('x')
            expr = function_str.replace('^', '**')
            lambdify(x, expr)
        except (SympifyError, TypeError, ValueError, NameError, SyntaxError):
            QMessageBox.warning(self, "Input Error", "Invalid function syntax.")
            return False

        # Validate min value of x input
        try:
            float(min_value)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid minimum value of x.")
            return False

        # Validate max value of x input
        try:
            float(max_value)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid maximum value of x.")
            return False

        # Check if min value is greater than or equal to max value
        if float(min_value) >= float(max_value):
            QMessageBox.warning(self, "Input Error", "Minimum value must be less than maximum value.")
            return False

        return True

    def plot_function(self):
        function_str = self.input_lineedit.text()
        min_value = self.min_lineedit.text()
        max_value = self.max_lineedit.text()

        if self.validate_input(function_str, min_value, max_value):
            # Generate x values for plotting
            x = np.linspace(float(min_value), float(max_value), 1000, dtype=np.float64)

            # Evaluate the function expression
            expr = function_str.replace('^', '**')
            func = lambdify(symbols('x'), expr)

            try:
                # Evaluate y values using the function expression
                y = func(x)

                # Plot the function
                plt.plot(x, y)
                plt.xlabel('x')
                plt.ylabel('f(x)')
                plt.title('Function Plot')
                plt.show()
            except Exception as e:
                QMessageBox.warning(self, "Plotting Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    plotter = FunctionPlotter()
    plotter.show()
    sys.exit(app.exec_())
