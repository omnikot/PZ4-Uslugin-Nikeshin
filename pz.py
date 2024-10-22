# main.py
# GitHub: https://github.com/your_username/your_repository

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import os


class FileScanner(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()

        self.dir_input = QtWidgets.QLineEdit(self)
        self.scan_button = QtWidgets.QPushButton("Сканировать", self)
        self.file_list = QtWidgets.QListWidget(self)

        self.layout.addWidget(QtWidgets.QLabel("Введите путь к папке:"))
        self.layout.addWidget(self.dir_input)
        self.layout.addWidget(self.scan_button)
        self.layout.addWidget(self.file_list)

        self.scan_button.clicked.connect(self.scan_directory)
        self.setLayout(self.layout)

    def scan_directory(self):
        folder = self.dir_input.text()
        if os.path.isdir(folder):
            self.file_list.clear()
            for filename in os.listdir(folder):
                self.file_list.addItem(filename)
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Папка не найдена!")


class FileEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()

        self.text_edit = QtWidgets.QTextEdit(self)
        self.open_button = QtWidgets.QPushButton("Открыть файл", self)
        self.save_button = QtWidgets.QPushButton("Сохранить файл", self)

        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.save_button)

        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_file)
        self.setLayout(self.layout)

    def open_file(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть текстовый файл", "",
                                                            "Text Files (*.txt);;All Files (*)", options=options)
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                self.text_edit.setText(f.read())

    def save_file(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить текстовый файл", "",
                                                            "Text Files (*.txt);;All Files (*)", options=options)
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.text_edit.toPlainText())


class FormSaver(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QFormLayout()

        self.inputs = {f"Поле {i}": QtWidgets.QLineEdit(self) for i in range(1, 6)}
        for label, input_field in self.inputs.items():
            self.layout.addRow(label, input_field)

        self.save_button = QtWidgets.QPushButton("Сохранить данные", self)
        self.layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_data)
        self.setLayout(self.layout)

    def save_data(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить данные", "",
                                                            "Text Files (*.txt);;All Files (*)", options=options)
        if filename:
            with open(filename, 'a', encoding='utf-8') as f:
                data = [(label, input_field.text()) for label, input_field in self.inputs.items()]
                f.write(', '.join([f"{key} ~ {value}" for key, value in data]) + '\n')


class ListReader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()

        self.list_view = QtWidgets.QListWidget(self)
        self.load_button = QtWidgets.QPushButton("Загрузить файл", self)

        self.layout.addWidget(self.list_view)
        self.layout.addWidget(self.load_button)

        self.load_button.clicked.connect(self.load_data)
        self.setLayout(self.layout)

    def load_data(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть файл с данными", "",
                                                            "Text Files (*.txt);;All Files (*)", options=options)
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    self.list_view.addItem(line.strip())


class MyApp(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(FileScanner(), "Сканирование файлов")
        self.addTab(FileEditor(), "Редактирование файла")
        self.addTab(FormSaver(), "Сохранение данных")
        self.addTab(ListReader(), "Чтение данных")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.setWindowTitle("Приложение на PyQt")
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())
