import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream
from ui.main_window import MainWindow

def load_styles(app):
    """Загружает стили из файла"""
    try:
        style_file = QFile("styles/styles.qss")
        if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(style_file)
            app.setStyleSheet(stream.readAll())
            style_file.close()
            print("Стили загружены успешно")
        else:
            print("Не удалось открыть файл стилей")
    except Exception as e:
        print(f"Не удалось загрузить стили: {e}")

def setup_directories():
    """Создает необходимые папки если их нет"""
    directories = ['data', 'styles', 'images']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Создана папка: {directory}")

def main():
    setup_directories()
    
    app = QApplication(sys.argv)
    
    if os.path.exists("styles/styles.qss"):
        load_styles(app)
    else:
        print("Файл стилей не найден, используется стандартный стиль")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()