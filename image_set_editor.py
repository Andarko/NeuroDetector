import xml.etree.ElementTree as xmlET
from dataclasses import dataclass

from lxml import etree
from PyQt5.QtWidgets import QMainWindow, QLabel, QListWidget, QMenu, QAction, QWidget, QHBoxLayout, QVBoxLayout, \
    QSizePolicy, QFileDialog, QInputDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt
import os
import glob


# Окно для работы с наборами изображений
class ImageSetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.imLabel = QLabel()
        # Список источников
        self.pathListWidget = QListWidget()
        self.menuPathListWidget = QMenu()
        self.actionPathSubFolder = QAction()
        self.actionPathEdit = QAction()
        self.actionPathRemove = QAction()
        # Список картинок
        self.labelImagesListWidget = QLabel()
        self.imagesListWidget = QListWidget()
        # Список объектов
        self.objectListWidget = QListWidget()
        # Путь к текущему открытому файлу
        self.fileName = ""
        self.init_ui()

    def init_ui(self):
        """Основное меню"""
        menuBar = self.menuBar()
        """Меню Файл"""
        fileMenu = menuBar.addMenu("&Файл")
        fileMenuANew = QAction("&Новый", self)
        fileMenuANew.setShortcut("Ctrl+N")
        fileMenuANew.setStatusTip("Новый набор картинок")

        fileMenu.addAction(fileMenuANew)
        fileMenu.addSeparator()
        fileMenuAOpen = QAction("&Открыть...", self)
        fileMenuAOpen.setShortcut("Ctrl+O")
        fileMenuAOpen.setStatusTip("Открыть существующий набор картинок")
        fileMenuAOpen.triggered.connect(self.open_file)
        fileMenu.addAction(fileMenuAOpen)

        fileMenu.addSeparator()
        fileMenuASave = fileMenu.addAction("&Сохранить")
        fileMenuASave.setShortcut("Ctrl+S")
        fileMenuASave.setStatusTip("Сохранить изменения")
        fileMenuASave.triggered.connect(self.save_file)

        fileMenuASaveAss = fileMenu.addAction("Сохранить как...")
        fileMenuASaveAss.setShortcut("Ctrl+Shift+S")
        fileMenuASaveAss.setStatusTip("Сохранить текущий набор картинок в другом файле...")
        fileMenuASaveAss.triggered.connect(self.save_file_ass)

        fileMenuASaveCopy = fileMenu.addAction("Сохранить копию...")
        fileMenuASaveCopy.setStatusTip("Скопировать текущий набор в отдельный файл...")
        fileMenuASaveCopy.triggered.connect(self.save_file_copy)

        fileMenu.addSeparator()
        fileMenuAExit = QAction("&Выйти", self)
        fileMenuAExit.setShortcut("Ctrl+Q")
        fileMenuAExit.setStatusTip("Закрыть приложение")
        fileMenuAExit.triggered.connect(self.close)
        fileMenu.addAction(fileMenuAExit)
        menuBar.addMenu(fileMenu)

        self.setWindowTitle('Редактор наборов изображений')

        """Центральные элементы, включая изображение"""
        mainWidget = QWidget(self)
        centralLayout = QHBoxLayout()
        mainWidget.setLayout(centralLayout)
        self.setCentralWidget(mainWidget)

        leftLayout = QVBoxLayout()
        centralLayout.addLayout(leftLayout)

        labelPathListWidget = QLabel("Источники")
        leftLayout.addWidget(labelPathListWidget)
        self.pathListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pathListWidget.customContextMenuRequested.connect(self.show_context_menu_path)
        self.pathListWidget.itemSelectionChanged.connect(self.path_list_widget_item_selected)

        """Контекстное меню"""
        actionPathAddFile = self.menuPathListWidget.addAction('Добавить файл/файлы...')
        actionPathAddFile.setShortcut("insert")
        actionPathAddFile.triggered.connect(self.action_path_add_file_click)

        actionPathAddFolder = self.menuPathListWidget.addAction('Добавить папку...')
        actionPathAddFolder.setShortcut("shift+insert")
        actionPathAddFolder.triggered.connect(self.action_path_add_folder_click)

        actionPathAddMask = self.menuPathListWidget.addAction('Добавить маску...')
        actionPathAddMask.setShortcut("ctrl+insert")
        actionPathAddMask.triggered.connect(self.action_path_add_mask_click)

        self.menuPathListWidget.addSeparator()
        self.actionPathEdit.setText("Изменить...")
        self.menuPathListWidget.addAction(self.actionPathEdit)
        self.actionPathEdit.triggered.connect(self.action_path_edit_click)

        self.actionPathSubFolder.setText("Включать подпапки")
        self.actionPathSubFolder.setCheckable(True)
        self.actionPathSubFolder.setChecked(False)
        self.menuPathListWidget.addAction(self.actionPathSubFolder)
        self.actionPathSubFolder.triggered.connect(self.action_path_sub_folder_click)

        self.menuPathListWidget.addSeparator()
        self.actionPathRemove.setText("Удалить")
        self.actionPathRemove.setShortcut("delete")
        self.menuPathListWidget.addAction(self.actionPathRemove)
        self.actionPathRemove.triggered.connect(lambda: self.pathListWidget.takeItem(self.pathListWidget.currentRow()))

        leftLayout.addWidget(self.pathListWidget)
        # for i in range(10):
        #     self.pathListWidget.addItem('Set #{}'.format(i))
        # self.pathListWidget.addItem('/home/krasnov/IRZProjects/NeuroWeb/Object-Detection-Quidditch-master/images')

        # labelImagesListWidget = QLabel("Файлы")
        self.labelImagesListWidget.setText("0 файлов")
        leftLayout.addWidget(self.labelImagesListWidget)
        leftLayout.addWidget(self.imagesListWidget)
        # for i in range(10):
        #     self.imagesListWidget.addItem('File #{}'.format(i))

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

    def open_file(self):
        fileDialog = QFileDialog()
        file = QFileDialog.getOpenFileName(fileDialog,
                                           "Выберите место сохранения файла",
                                           "",
                                           "All files (*.*);;Наборы изображений (*.ims)",
                                           "Наборы изображений (*.ims)",
                                           options=fileDialog.options() | QFileDialog.DontUseNativeDialog)
        if not file[0]:
            return

        # Загружаем данные тз нашего файла в xml формате
        with open(file[0]) as fobj:
            xml = fobj.read()
        root = etree.fromstring(xml)
        self.pathListWidget.clear()
        for pathsElement in root.getchildren():
            if pathsElement.tag == "Paths":
                for pathElement in pathsElement.getchildren():
                    self.pathListWidget.addItem(pathElement.text)
        self.fileName = file[0]

    def save_file(self, save_dlg=True):
        if self.pathListWidget.count() == 0:
            return
        if save_dlg or not self.fileName:
            fileDialog = QFileDialog()
            file = QFileDialog.getSaveFileName(fileDialog,
                                               "Выберите место сохранения файла",
                                               "",
                                               "All files (*.*);;Наборы изображений (*.ims)",
                                               "Наборы изображений (*.ims)",
                                               options=fileDialog.options() | QFileDialog.DontUseNativeDialog)
            if file[0]:
                ext = os.path.splitext(file[0])
                if ext[1] == ".ims":
                    self.fileName = file[0]
                else:
                    self.fileName = ext[0] + ".ims"
                if os.path.exists(self.fileName):
                    messageBox = QMessageBox()
                    dlgResult = QMessageBox.question(messageBox,
                                                     "Confirm Dialog",
                                                     "Файл уже существует. Хотите его перезаписать?" +
                                                     "Это удалит данные в нем",
                                                     QMessageBox.Yes | QMessageBox.No,
                                                     QMessageBox.No)
                    if dlgResult == QMessageBox.No:
                        return

            else:
                return

        # Записываем данные в наш файл в xml формате
        if self.fileName:
            root = xmlET.Element("ImageSet")
            pathsElement = xmlET.Element("Paths")
            root.append(pathsElement)

            for i in range(self.pathListWidget.count()):
                pathElement = xmlET.SubElement(pathsElement, "Path")
                pathElement.text = self.pathListWidget.item(i).text()

            tree = xmlET.ElementTree(root)
            with open(self.fileName, "w"):
                tree.write(self.fileName)

    def save_file_ass(self):
        self.save_file(True)
        return

    def save_file_copy(self):
        currentFileName = self.fileName
        self.save_file(True)
        self.fileName = currentFileName
        return

    # Отображение
    def show_context_menu_path(self, point):
        if self.pathListWidget.currentItem():
            self.actionPathEdit.setEnabled(True)
            self.actionPathRemove.setEnabled(True)
            path = self.pathListWidget.currentItem().text()
            withSubFolders = False
            if str.endswith(path, "**"):
                path = path[0:-2]
                withSubFolders = True

            if os.path.exists(path) and os.path.isdir(path):
                self.actionPathSubFolder.setEnabled(True)
                self.actionPathSubFolder.setChecked(withSubFolders)
            else:
                self.actionPathSubFolder.setEnabled(False)
                self.actionPathSubFolder.setChecked(False)
        else:
            self.actionPathSubFolder.setEnabled(False)
            self.actionPathSubFolder.setChecked(False)
            self.actionPathEdit.setEnabled(False)
            self.actionPathRemove.setEnabled(False)
        self.menuPathListWidget.exec(self.mapToGlobal(point))

    def get_files_images(self, init_dir="", multi_select=True):
        openDialog = QFileDialog()
        getFile = openDialog.getOpenFileNames
        if not multi_select:
            getFile = openDialog.getOpenFileName
        files = getFile(self,
                        "Выберите файлы изображения",
                        init_dir,
                        "JPEG (*.jpg);;All files (*)",
                        "JPEG (*.jpg)",
                        options=openDialog.options() | QFileDialog.DontUseNativeDialog)
        return files[0]

    def action_path_add_file_click(self):
        for file in self.get_files_images("", True):
            if file:
                self.pathListWidget.addItem(file)

    def get_folder_images(self, init_dir=""):
        openDialog = QFileDialog()
        directory = openDialog.getExistingDirectory(self,
                                                    "Выберите папку с файлами",
                                                    init_dir,
                                                    options=openDialog.options() | QFileDialog.DontUseNativeDialog)
        if directory and os.path.isdir(directory):
            if not glob.glob(os.path.join(directory, "*.jpg")) \
                    and not glob.glob(os.path.join(directory, "**", "*.jpg"), recursive=True):
                mBox = QMessageBox()
                dlgResult = mBox.question(self,
                                          "Диалог подтверждения",
                                          "В указанной папке не обнаружено файлов изображений. Все равно добавить ее?",
                                          QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.No)
                if dlgResult == QMessageBox.No:
                    return ""
        return directory

    def action_path_add_folder_click(self):
        directory = self.get_folder_images()
        if directory:
            self.pathListWidget.addItem(directory)

    def get_mask_images(self, init_path):
        inputDialog = QInputDialog()
        if not str.endswith(init_path, "*.jpg"):
            init_path = os.path.join(init_path, "*.jpg")

        while True:
            mask, ok = inputDialog.getText(self,
                                           'Введите маску для файлов директории',
                                           'Enter your name:',
                                           QLineEdit.Normal,
                                           init_path)

            if ok:
                if not glob.glob(mask, recursive=True):
                    dlgText = "По указанной маске не обнаружено файлов изображений. Все равно добавить маску?"
                    mBox = QMessageBox()
                    dlgResult = mBox.question(self,
                                              "Диалог подтверждения",
                                              dlgText,
                                              QMessageBox.Yes | QMessageBox.No,
                                              QMessageBox.No)
                    if dlgResult == QMessageBox.No:
                        continue
                return mask
            else:
                return ""

    def action_path_add_mask_click(self):
        directory = self.get_folder_images()
        if directory:
            mask = self.get_mask_images(directory)
            if mask:
                self.pathListWidget.addItem(mask)

    def action_path_edit_click(self):
        if self.pathListWidget.currentItem():
            path = self.pathListWidget.currentItem().text()
            withSubFolders = False
            if str.endswith(path, "**"):
                path = path[0:-2]
                withSubFolders = True
            newStr = ""
            if os.path.exists(path):
                # Папка
                if os.path.isdir(path):
                    newStr = self.get_folder_images(path)
                    if withSubFolders:
                        newStr += "**"
                # Файл
                else:
                    newStr = self.get_files_images(path, False)
            # Маска
            else:
                newStr = self.get_mask_images(path)
            if newStr:
                self.pathListWidget.currentItem().setText(newStr)
                self.path_list_widget_item_selected()

    def action_path_sub_folder_click(self):
        if self.pathListWidget.currentItem():
            if self.actionPathSubFolder.isChecked():
                if not str.endswith(self.pathListWidget.currentItem().text(), "**"):
                    self.pathListWidget.currentItem().setText(self.pathListWidget.currentItem().text() + "**")
            elif str.endswith(self.pathListWidget.currentItem().text(), "**"):
                self.pathListWidget.currentItem().setText(self.pathListWidget.currentItem().text()[0:-2])
            self.path_list_widget_item_selected()

    def path_list_widget_item_selected(self):
        self.imagesListWidget.clear()
        if self.pathListWidget.currentItem():
            path = self.pathListWidget.currentItem().text()
            withSubFolders = False
            if str.endswith(path, "**"):
                path = path[0:-2]
                withSubFolders = True
            if os.path.split(path)[1] and not str.endswith(os.path.split(path)[1], ".jpg"):
                path = os.path.join(path, "*.jpg")
            files = glob.glob(path, recursive=True)
            if withSubFolders:
                files += glob.glob(os.path.join(os.path.split(path)[0], "**", "*.jpg"), recursive=True)
            files.sort()
            for file in files:
                self.imagesListWidget.addItem(file)
        endWord = get_end_of_word(self.imagesListWidget.count(), ("", "а", "ов"))
        self.labelImagesListWidget.setText(f"{self.imagesListWidget.count()} файл{endWord}")


def get_end_of_word(count, ends):
    mod = count % 100
    if 5 <= mod <= 20:
        return ends[2]
    else:
        mod = (count - 1) % 10
        if mod == 0:
            return ends[0]
        elif mod < 4:
            return ends[1]
        else:
            return ends[2]
