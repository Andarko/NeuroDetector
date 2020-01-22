import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTreeView, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QFileSystemModel, QMenuBar, QMenu, QMainWindow, QPushButton, QAction, qApp
from PyQt5.QtWidgets import QTextEdit, QSizePolicy, QGridLayout, QStyle, QFrame, QErrorMessage, QCheckBox
from PyQt5.QtWidgets import QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QDockWidget
from PyQt5.QtGui import QIcon, QPixmap, QImage
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt, QSize, QEvent, QPoint
from PyQt5.Qt import pyqtSignal, pyqtSlot, QObject
# Класс QQuickView предоставляет возможность отображать QML файлы.
from PyQt5.QtQuick import QQuickView
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine


class Calculator(QObject):
    def __init__(self):
        QObject.__init__(self)

    # Signal sending sum
    # Necessarily give the name of the argument through arguments=['sum']
    # Otherwise it will not be possible to get it up in QML
    sumResult = pyqtSignal(int, arguments=['sum'])

    subResult = pyqtSignal(int, arguments=['sub'])

    # Slot for summing two numbers
    @pyqtSlot(int, int)
    def sum(self, arg1, arg2):
        # Sum two arguments and emit a signal
        self.sumResult.emit(arg1 + arg2)

    # Slot for subtraction of two numbers
    @pyqtSlot(int, int)
    def sub(self, arg1, arg2):
        # Subtract arguments and emit a signal
        self.subResult.emit(arg1 - arg2)


if __name__ == "__main__":
    import sys

    # Create an instance of the application
    app = QGuiApplication(sys.argv)
    # Create QML engine
    engine = QQmlApplicationEngine()
    # Create a calculator object
    calculator = Calculator()
    # And register it in the context of QML
    engine.rootContext().setContextProperty("calculator", calculator)
    # Load the qml file into the engine
    engine.load("main.qml")

    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
