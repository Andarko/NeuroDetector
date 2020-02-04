

# Окно для работы с наборами изображений
from PyQt5.QtWidgets import QMainWindow, QLabel, QListWidget, QMenu, QAction, QWidget, QHBoxLayout, QVBoxLayout, \
    QSizePolicy, QFileDialog, QInputDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt
import os
import glob


class ImageSetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.imLabel = QLabel()
        self.objectListWidget = QListWidget()
        self.menuPathListWidget = QMenu(self)
        self.imagesListWidget = QListWidget()
        self.menuPathListWidget = QMenu(self)
        self.pathListWidget = QListWidget()
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

        labelPathListWidget = QLabel("Пути с файлами")
        leftLayout.addWidget(labelPathListWidget)
        self.pathListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pathListWidget.customContextMenuRequested.connect(self.show_context_menu)

        actionPathAddFile = self.menuPathListWidget.addAction('Add new file/files...')
        actionPathAddFile.setShortcut("insert")
        actionPathAddFile.triggered.connect(self.action_path_add_file_click)

        actionPathAddFolder = self.menuPathListWidget.addAction('Add new folder...')
        actionPathAddFolder.setShortcut("shift + insert")
        actionPathAddFolder.triggered.connect(self.action_path_add_folder_click)

        actionPathAddMask = self.menuPathListWidget.addAction('Add new mask...')
        actionPathAddMask.setShortcut("ctrl + insert")
        actionPathAddMask.triggered.connect(self.action_path_add_mask_click)

        self.menuPathListWidget.addSeparator()
        actionPathRemove = self.menuPathListWidget.addAction('Remove')
        actionPathRemove.setShortcut("delete")
        actionPathRemove.triggered.connect(lambda: self.pathListWidget.takeItem(self.pathListWidget.currentRow()))

        leftLayout.addWidget(self.pathListWidget)
        # for i in range(10):
        #     self.pathListWidget.addItem('Set #{}'.format(i))
        self.pathListWidget.addItem('/home/krasnov/IRZProjects/NeuroWeb/Object-Detection-Quidditch-master/images')

        labelImagesListWidget = QLabel("Файлы")
        leftLayout.addWidget(labelImagesListWidget)
        leftLayout.addWidget(self.imagesListWidget)
        for i in range(10):
            self.imagesListWidget.addItem('File #{}'.format(i))

        labelObjectListWidget = QLabel("Объекты")
        leftLayout.addWidget(labelObjectListWidget)
        leftLayout.addWidget(self.objectListWidget)
        self.objectListWidget.addItem('Автомобиль')
        self.objectListWidget.addItem('Человек')
        self.objectListWidget.addItem('Птица')

        self.imLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imLabel.setStyleSheet("border: 1px solid red")
        centralLayout.addWidget(self.imLabel)

        self.resize(800, 600)
        self.move(300, 300)
        self.setMinimumSize(800, 600)

    def show_context_menu(self, point):
        self.menuPathListWidget.exec(self.mapToGlobal(point))

    def action_path_add_file_click(self):
        openDialog = QFileDialog()
        file = openDialog.getOpenFileName(self
                                          , "Выберите файлы изображения"
                                          , "/"
                                          , "All files (*.*);;JPEG (*.jpg, *.jpeg)"
                                          , "JPEG (*.jpg, *.jpeg)")
        if file[0]:
            self.pathListWidget.addItem(file[0])

    def action_path_add_folder_click(self):
        openDialog = QFileDialog()
        directory = openDialog.getExistingDirectory(self, "Выберите папку с файлами", "/")
        if directory and os.path.isdir(directory):
            if not glob.glob(os.path.join(directory, "*.jpg")) \
               and not glob.glob(os.path.join(directory, "**", "*.jpg"), recursive=True):
                mBox = QMessageBox()
                dlgResult = mBox.question(self
                                          , "Диалог подтверждения"
                                          , "В указанной папке не обнаружено файлов изображений. Все равно добавить ее?"
                                          , QMessageBox.Yes | QMessageBox.No
                                          , QMessageBox.No)
                if dlgResult == QMessageBox.No:
                    return
            self.pathListWidget.addItem(directory)
            # for file in glob.glob(os.path.join(directory, "**", "*.jpg"), recursive=True):
            #     self.pathListWidget.addItem(file)

    def action_path_add_mask_click(self):
        openDialog = QFileDialog()
        directory = openDialog.getExistingDirectory(self, "Выберите папку с файлами", "/")

        if directory and os.path.isdir(directory):
            mBox = QMessageBox()
            if not glob.glob(os.path.join(directory, "*.jpg")) \
                    and not glob.glob(os.path.join(directory, "**", "*.jpg"), recursive=True):
                dlgResult = mBox.question(self
                                          , "Диалог подтверждения"
                                          , "В указанной папке не обнаружено файлов изображений. Все равно добавить ее?"
                                          , QMessageBox.Yes | QMessageBox.No
                                          , QMessageBox.No)
                if dlgResult == QMessageBox.No:
                    return
            inputDialog = QInputDialog()
            mask = os.path.join(directory, "*.jpg")

            while True:
                mask, ok = inputDialog.getText(self
                                               , 'Введите маску для файлов директории'
                                               , 'Enter your name:'
                                               , QLineEdit.Normal
                                               , mask)

                if ok and not glob.glob(mask, recursive=True):
                    dlgResult = mBox.question(self
                                              , "Диалог подтверждения"
                                              , "По указанной маске не обнаружено файлов изображений. "
                                              + "Все равно добавить маску?"
                                              , QMessageBox.Yes | QMessageBox.No
                                              , QMessageBox.No)
                    if dlgResult == QMessageBox.No:
                        continue
                    self.pathListWidget.addItem(mask)
                    break
                else:
                    break
