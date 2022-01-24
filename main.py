from mainWindow import Ui_PortScanner
from PyQt6 import QtWidgets
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_PortScanner()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())


