from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе SimplePaint")
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel("SimplePaint")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Описание
        desc_label = QLabel(
            "Простой графический редактор\n\n"
            "Разработано в рамках учебного проекта\n\n"
            "Возможности:\n"
            "• Рисование кистью\n"
            "• Геометрические фигуры\n"
            "• Ластик для исправлений\n"
            "• Сохранение в PNG, JPEG, BMP\n"
            "• Загрузка изображений\n"
            "• Сохранение настроек"
        )
        desc_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(desc_label)

        # Версия
        version_label = QLabel("Версия 1.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        # Кнопка OK
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)
        self.setLayout(layout)
