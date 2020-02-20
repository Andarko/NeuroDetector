import sys


from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTreeView, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QFileSystemModel, QMenuBar, QMenu, QMainWindow, QPushButton, QAction, qApp
from PyQt5.QtWidgets import QTextEdit, QSizePolicy, QGridLayout, QStyle, QFrame, QErrorMessage, QCheckBox
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtWidgets import QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QDockWidget
from PyQt5.QtGui import QIcon, QPixmap, QImage
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt, QSize, QEvent, QPoint, QUrl
from PyQt5.Qt import pyqtSignal, pyqtSlot, QObject
# Класс QQuickView предоставляет возможность отображать QML файлы.
from PyQt5.QtQuick import QQuickView
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import sys
from dataclasses import dataclass
import os.path

from image_set_editor import ImageSetWindow
from image_set_editor import ImageSet


# Класс типа нейронной сети
@dataclass
class TypeOfNetwork:
    name: str = ""
    settingsFolder: str = ""


# Класс "Распознающая нейросеть
@dataclass
class RecognizingNN:
    imageSet: ImageSet = ImageSet()
    filePath: str = ""
    educated: bool = False
    typeOfNetwork: TypeOfNetwork = TypeOfNetwork()


# Главное окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.imgSetEditForm = ImageSetWindow()
        self.init_ui()

    def init_ui(self):
        # Основное меню
        menuBar = self.menuBar()

        # Меню "Файл"
        fileMenu = menuBar.addMenu("&Файл")
        fileMenuANew = QAction("&Новый", self)
        fileMenuANew.setShortcut("Ctrl+N")
        fileMenuANew.setStatusTip("Новая нейросеть")
        fileMenu.addAction(fileMenuANew)
        fileMenu.addSeparator()
        fileMenuAOpen = QAction("&Открыть...", self)
        fileMenuAOpen.setShortcut("Ctrl+O")
        fileMenuAOpen.setStatusTip("Открыть существующую нейросеть")
        fileMenuAOpen.triggered.connect(self.open_file)
        fileMenu.addAction(fileMenuAOpen)
        fileMenu.addSeparator()
        fileMenuASave = fileMenu.addAction("&Сохранить")
        fileMenuASave.setShortcut("Ctrl+S")
        fileMenuASave.setStatusTip("Сохранить изменения")
        # fileMenuASave.triggered.connect(self.saveFile)
        fileMenuASaveAss = fileMenu.addAction("Сохранить как...")
        fileMenuASaveAss.setShortcut("Ctrl+Shift+S")
        fileMenuASaveAss.setStatusTip("Сохранить текущую нейросеть в другом файле...")
        # fileMenuASaveAss.triggered.connect(self.saveFileAss)
        fileMenu.addSeparator()
        fileMenuAExit = QAction("&Выйти", self)
        fileMenuAExit.setShortcut("Ctrl+Q")
        fileMenuAExit.setStatusTip("Закрыть приложение")
        fileMenuAExit.triggered.connect(self.close)
        fileMenu.addAction(fileMenuAExit)
        menuBar.addMenu(fileMenu)

        # Меню "Набор картинок"
        imgSetMenu = menuBar.addMenu("Набор &картинок")
        imgSetMenuAEdit = imgSetMenu.addAction("Смотреть/&Редактировать...")
        imgSetMenuAEdit.setStatusTip("Просмотр и редактирование наборов картинок")
        imgSetMenuAEdit.triggered.connect(self.img_set_edit_form_open)
        imgSetMenuAOpen = imgSetMenu.addAction("&Выбрать набор...")
        imgSetMenuAOpen.setStatusTip("Выбрать набор картинок для обучения")
        # imgSetMenuAOpen.triggered.connect(self.imgSetOpen)
        menuBar.addMenu(imgSetMenu)

        self.setWindowTitle('NeuroDetector v0.0.0')
        # Центральные элементы, включая изображение
        mainWidget = QWidget(self)
        centralLayout = QVBoxLayout()
        mainWidget.setLayout(centralLayout)
        self.setCentralWidget(mainWidget)

        self.statusBar().setStatusTip("Ready")

        self.resize(1280, 720)
        self.move(300, 300)
        self.setMinimumSize(800, 600)
        # neuroNetwork = RecognizingNN()
        # neuroNetwork.imageSet.imgPaths.append("/etc/")
        self.show()

    def img_set_edit_form_open(self):
        self.imgSetEditForm.show()

    def open_file(self):
        openDialog = QFileDialog()
        a = openDialog.getOpenFileName(self,
                                       "Выберите файл изображения",
                                       "",
                                       "All files (*.*);;Microscope scans (*.misc)",
                                       "Microscope scans (*.misc)",
                                       options=openDialog.options() | QFileDialog.DontUseNativeDialog)
        for b in a:
            print(b)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
