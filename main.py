import sys
from typing import List

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
from dataclasses import dataclass, field
import os.path


# Размеры изображения для аннотаций
@dataclass
class SizeImage:
    width: int = 0
    height: int = 0
    depth: int = 3


@dataclass
class BoundBox:
    xmin: int = 0
    ymin: int = 0
    xmax: int = 0
    ymax: int = 0


# Объект на изображении
@dataclass
class ObjectInImage:
    name: str = ""
    pose: str = ""
    truncated: int = 0
    Difficult: int = 0
    bndbox: BoundBox = BoundBox()


# Класс "Картинка с аннотацией"
@dataclass
class SingleImage:
    path: str
    filename: str = ""
    folder: str = ""
    size: SizeImage = SizeImage()
    objectFromImage: List[ObjectInImage] = field(default_factory=list, repr=False)
    segmented: int = 0

    def __post_init__(self):
        if self.path:
            os.path.splitext(self.path)


# Класс "Набор картинок"
@dataclass
class ImageSet:
    # Путь к файлу с описанием набора картинок
    filePath: str = ""
    imgPaths: List[str] = field(default_factory=list, repr=False)


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
        # fileMenuAOpen.triggered.connect(self.openFile)
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
        imgSetMenuAEdit.triggered.connect(self.imgSetEditFormOpen)
        imgSetMenuAOpen = imgSetMenu.addAction("&Выбрать набор...")
        imgSetMenuAOpen.setStatusTip("Выбрать набор картинок для обучения")
        # imgSetMenuAOpen.triggered.connect(self.imgSetOpen)
        menuBar.addMenu(imgSetMenu)

        self.setWindowTitle('NeuroDetector')
        # Центральные элементы, включая изображение
        mainLayout = QHBoxLayout(self)
        mainWidget = QWidget(self)
        centralLayout = QVBoxLayout()
        mainWidget.setLayout(centralLayout)
        self.setCentralWidget(mainWidget)

        self.statusBar().setStatusTip("Ready")

        self.resize(1280, 720)
        self.move(300, 300)
        self.setMinimumSize(800, 600)
        neuroNetwork = RecognizingNN()
        neuroNetwork.imageSet.imgPaths.append("/etc/")
        self.show()
        self.imgSetEditForm = ImageSetWindow()

    def imgSetEditFormOpen(self):
        self.imgSetEditForm.show()


# Окно для работы с наборами изображений
class ImageSetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Основное меню
        menuBar = self.menuBar()
        # Меню "Файл"
        fileMenu = menuBar.addMenu("&Файл")
        fileMenuANew = QAction("&Новый", self)
        fileMenuANew.setShortcut("Ctrl+N")
        fileMenuANew.setStatusTip("Новый набор картинок")

        fileMenu.addAction(fileMenuANew)
        fileMenu.addSeparator()
        fileMenuAOpen = QAction("&Открыть...", self)
        fileMenuAOpen.setShortcut("Ctrl+O")
        fileMenuAOpen.setStatusTip("Открыть существующий набор картинок")
        # fileMenuAOpen.triggered.connect(self.openFile)
        fileMenu.addAction(fileMenuAOpen)
        fileMenu.addSeparator()
        fileMenuASave = fileMenu.addAction("&Сохранить")
        fileMenuASave.setShortcut("Ctrl+S")
        fileMenuASave.setStatusTip("Сохранить изменения")
        # fileMenuASave.triggered.connect(self.saveFile)
        fileMenuASaveAss = fileMenu.addAction("Сохранить как...")
        fileMenuASaveAss.setShortcut("Ctrl+Shift+S")
        fileMenuASaveAss.setStatusTip("Сохранить текущий набор картинок в другом файле...")
        # fileMenuASaveAss.triggered.connect(self.saveFileAss)
        fileMenuASaveAss = fileMenu.addAction("Сохранить копию...")
        fileMenuASaveAss.setStatusTip("Сохранить текущий набор в отдельный файл...")
        # fileMenuASaveAss.triggered.connect(self.saveFileAss)
        fileMenu.addSeparator()
        fileMenuAExit = QAction("&Выйти", self)
        fileMenuAExit.setShortcut("Ctrl+Q")
        fileMenuAExit.setStatusTip("Закрыть приложение")
        fileMenuAExit.triggered.connect(self.close)
        fileMenu.addAction(fileMenuAExit)
        menuBar.addMenu(fileMenu)

        self.setWindowTitle('Редактор наборов изображений')
        # Центральные элементы, включая изображение
        mainWidget = QWidget(self)
        centralLayout = QHBoxLayout()
        mainWidget.setLayout(centralLayout)
        self.setCentralWidget(mainWidget)

        leftLayout = QVBoxLayout()
        centralLayout.addLayout(leftLayout)

        labelPathesListWidget = QLabel("Пути с файлами")
        leftLayout.addWidget(labelPathesListWidget)
        self.pathesListWidget = QListWidget()
        self.pathesListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pathesListWidget.customContextMenuRequested.connect(self.show_context_menu)

        self.menu = QMenu(self)
        action = self.menu.addAction('Say: "Hello!"')
        action.triggered.connect(lambda: QMessageBox.information(self, 'Info', 'Hello!'))

        leftLayout.addWidget(self.pathesListWidget)
        for i in range(10):
            self.pathesListWidget.addItem('Set #{}'.format(i))

        labelImagesListWidget = QLabel("Файлы")
        leftLayout.addWidget(labelImagesListWidget)
        self.imagesListWidget = QListWidget()
        leftLayout.addWidget(self.imagesListWidget)
        for i in range(10):
            self.imagesListWidget.addItem('File #{}'.format(i))

        labelObjectsListWidget = QLabel("Объекты")
        leftLayout.addWidget(labelObjectsListWidget)
        self.objectsListWidget = QListWidget()
        leftLayout.addWidget(self.objectsListWidget)
        self.objectsListWidget.addItem('Автомобиль')
        self.objectsListWidget.addItem('Человек')
        self.objectsListWidget.addItem('Птица')


        self.imLabel = QLabel()
        self.imLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imLabel.setStyleSheet("border: 1px solid red")
        centralLayout.addWidget(self.imLabel)

        self.resize(800, 600)
        self.move(300, 300)
        self.setMinimumSize(800, 600)

    def show_context_menu(self, point):
        self.menu.exec(self.mapToGlobal(point))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
