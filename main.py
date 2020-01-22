import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTreeView, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QFileSystemModel, QMenuBar, QMenu, QMainWindow, QPushButton, QAction, qApp
from PyQt5.QtWidgets import QTextEdit, QSizePolicy, QGridLayout, QStyle, QFrame, QErrorMessage, QCheckBox
from PyQt5.QtWidgets import QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QDockWidget
from PyQt5.QtGui import QIcon, QPixmap, QImage
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt, QSize, QEvent, QPoint
from PyQt5.Qt import pyqtSignal

# Главное окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()



    def initUI(self):
        self.setWindowTitle('Micros')
        # Основное меню
        menuBar = self.menuBar()
        # Меню "Файл"
        fileMenu = menuBar.addMenu("&Файл")
        fileMenuANew = QAction("&Новый", self)
        fileMenuANew.setShortcut("Ctrl+N")
        fileMenuANew.setStatusTip("Новое сканирование")
        # fileMenuANew.triggered.connect(self.close)
        fileMenu.addAction(fileMenuANew)
        fileMenu.addSeparator()
        fileMenuAOpen = QAction("&Открыть", self)
        fileMenuAOpen.setShortcut("Ctrl+O")
        fileMenuAOpen.setStatusTip("Открыть существующее изображение")
        # fileMenuAOpen.triggered.connect(self.openFile)
        fileMenu.addAction(fileMenuAOpen)
        fileMenu.addSeparator()
        fileMenuASave = fileMenu.addAction("&Сохранить")
        fileMenuASave.setShortcut("Ctrl+S")
        fileMenuASave.setStatusTip("Сохранить изменения")
        # fileMenuASave.triggered.connect(self.saveFile)
        fileMenuASaveAss = fileMenu.addAction("Сохранить как...")
        fileMenuASaveAss.setShortcut("Ctrl+Shift+S")
        fileMenuASaveAss.setStatusTip("Сохранить текущее изображение в другом файле...")
        # fileMenuASaveAss.triggered.connect(self.saveFileAss)
        fileMenu.addSeparator()
        fileMenuAExit = QAction("&Выйти", self)
        fileMenuAExit.setShortcut("Ctrl+Q")
        fileMenuAExit.setStatusTip("Закрыть приложение")
        # fileMenuAExit.triggered.connect(self.close)
        fileMenu.addAction(fileMenuAExit)
        menuBar.addMenu(fileMenu)
        # Меню "Вид"
        viewMenu = menuBar.addMenu("&Вид")
        self.viewMenuMainPanel = QAction("Основная &панель", self)
        self.viewMenuMainPanel.setShortcut("Ctrl+T")
        self.viewMenuMainPanel.setStatusTip("Отображать основную панель")
        # self.viewMenuMainPanel.triggered.connect(self.viewMenuMainPanel_Click)
        self.viewMenuMainPanel.setCheckable(True)
        self.viewMenuMainPanel.setChecked(True)
        viewMenu.addAction(self.viewMenuMainPanel)
        menuBar.addMenu(viewMenu)
        # Меню "Настройки"
        servicesMenu = menuBar.addMenu("&Сервис")
        self.servicesMenuAllInMemory = QAction("&Буферизировать изображение", self)
        self.servicesMenuAllInMemory.setShortcut("Ctrl+M")
        self.servicesMenuAllInMemory.setStatusTip(
            "Разместить все части изображения в памяти, что увеличит скорость навигации по нему")
        # self.servicesMenuAllInMemory.triggered.connect(self.servicesMenuAllInMemory_Click)
        self.servicesMenuAllInMemory.setCheckable(True)
        self.servicesMenuAllInMemory.setChecked(False)
        servicesMenu.addAction(self.servicesMenuAllInMemory)
        servicesMenu.addSeparator()
        self.servicesMenuSettings = QAction("Настройки", self)
        self.servicesMenuSettings.setStatusTip("Изменить основные настройки программы")
        # self.servicesMenuSettings.triggered.connect(self.servicesMenuSettings_Click)
        servicesMenu.addAction(self.servicesMenuSettings)
        menuBar.addMenu(servicesMenu)

        # Центральные элементы, включая изображение
        mainLayout = QHBoxLayout(self)
        mainWidget = QWidget(self)
        # mainWidget.setLayout(mainLayout)
        centralLayout = QVBoxLayout()
        mainWidget.setLayout(centralLayout)
        self.imLabel = QLabel()

        self.imLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imLabel.setStyleSheet("border: 1px solid red")
        self.imLabel.installEventFilter(self)

        centralLayout.addWidget(self.imLabel)

        minimapLayout = QGridLayout()
        self.imLabel.setLayout(minimapLayout)

        self.minimapLabel = QLabel()
        self.minimapLabel.installEventFilter(self)

        minimapLayout.setRowStretch(0, 1)
        minimapLayout.setColumnStretch(0, 1)
        minimapLayout.addWidget(self.minimapLabel, 1, 1)

        messageEdit = QTextEdit(self)
        messageEdit.setEnabled(False)

        messageEdit.setText("Hello, world!")

        messageEdit.setFixedHeight(100)
        messageEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        centralLayout.addWidget(messageEdit)

        # Правые элементы
        self.rightDocWidget = QDockWidget("Dock Widget", self)
        self.rightDocWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        rightLayout = QVBoxLayout(self)

        btn31 = QPushButton("MegaImg", self)
        # btn31.clicked.connect(self.btn31_Click)
        btn32 = QPushButton("Prepare", self)
        # btn32.clicked.connect(self.prepareScans)
        btn33 = QPushButton("View", self)
        rightLayout.addWidget(btn31)
        rightLayout.addWidget(btn32)
        rightLayout.addWidget(btn33)

        minimapCheckBox = QCheckBox("Мини-изображение", self)
        # minimapCheckBox.stateChanged.connect(self.minimapCheckBox_Changed)
        minimapCheckBox.setCheckState(Qt.Checked)
        rightLayout.addWidget(minimapCheckBox)

        rightLayout.addSpacing(50)

        labScale = QLabel("Увеличение")
        self.scaleEdit = QDoubleSpinBox()
        self.scaleEdit.setMinimum(0.001)
        self.scaleEdit.setMaximum(10.0)
        self.scaleEdit.setValue(1.0)
        self.scaleEdit.setSingleStep(0.01)
        self.scaleEdit.setDecimals(3)
        # self.scaleEdit.valueChanged.connect(self.scaleEdit_Change)
        rightLayout.addWidget(labScale)
        rightLayout.addWidget(self.scaleEdit)

        rightLayout.addStretch(0)

        rightDockWidgetContents = QWidget()
        rightDockWidgetContents.setLayout(rightLayout)
        self.rightDocWidget.setWidget(rightDockWidgetContents)
        self.rightDocWidget.installEventFilter(self)

        self.setCentralWidget(mainWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.rightDocWidget)

        self.statusBar().setStatusTip("Ready")

        self.resize(1280, 720)
        self.move(300, 300)
        self.setMinimumSize(800, 600)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
