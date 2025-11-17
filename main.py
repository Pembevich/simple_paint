import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream
from ui.main_window import MainWindow

def load_styles():
    """Загружает стили из файла"""
    try:
        style_file = QFile("styles/styles.qss")
        if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(style_file)
            app.setStyleSheet(stream.readAll())
            style_file.close()
    except Exception as e:
        print(f"Не удалось загрузить стили: {e}")

def main():
    app = QApplication(sys.argv)
    
    # Загружаем стили (если файл существует)
    if os.path.exists("styles/styles.qss"):
        load_styles()
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()