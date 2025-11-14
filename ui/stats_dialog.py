from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QTabWidget, QWidget)
from PyQt6.QtCore import Qt
from utils.database import DatabaseManager

class StatsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseManager()
        self.setWindowTitle("Статистика рисования")
        self.setFixedSize(500, 400)
        self.setup_ui()
        self.load_stats()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Вкладки
        self.tabs = QTabWidget()
        
        # Вкладка общей статистики
        self.general_tab = QWidget()
        self.setup_general_tab()
        self.tabs.addTab(self.general_tab, "Общая статистика")
        
        # Вкладка истории действий
        self.history_tab = QWidget()
        self.setup_history_tab()
        self.tabs.addTab(self.history_tab, "История действий")

        layout.addWidget(self.tabs)

        # Кнопка закрытия
        button_layout = QHBoxLayout()
        self.close_btn = QPushButton("Закрыть")
        self.close_btn.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def setup_general_tab(self):
        layout = QVBoxLayout()
        
        # Статистика по инструментам
        self.tools_label = QLabel("Статистика по инструментам:")
        self.tools_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.tools_label)
        
        self.tools_stats = QLabel("Загрузка...")
        layout.addWidget(self.tools_stats)

        # Статистика по цветам
        self.colors_label = QLabel("Статистика по цветам:")
        self.colors_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.colors_label)
        
        self.colors_stats = QLabel("Загрузка...")
        layout.addWidget(self.colors_stats)

        # Общая информация
        self.info_label = QLabel("Общая информация:")
        self.info_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.info_label)
        
        self.info_stats = QLabel("Загрузка...")
        layout.addWidget(self.info_stats)

        layout.addStretch()
        self.general_tab.setLayout(layout)

    def setup_history_tab(self):
        layout = QVBoxLayout()
        
        # Таблица истории
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Время", "Инструмент", "Цвет", "Размер"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.history_table)
        self.history_tab.setLayout(layout)

    def load_stats(self):
        """Загружает статистику из базы данных"""
        try:
            # Статистика по инструментам
            tools_stats = self.db_manager.get_tools_stats(self.get_current_session_id())
            tools_text = ""
            for tool, count in tools_stats:
                tools_text += f"{tool}: {count} раз\n"
            self.tools_stats.setText(tools_text if tools_text else "Нет данных")

            # Статистика по цветам
            colors_stats = self.db_manager.get_colors_stats(self.get_current_session_id())
            colors_text = ""
            for color, count in colors_stats:
                colors_text += f"{color}: {count} раз\n"
            self.colors_stats.setText(colors_text if colors_text else "Нет данных")

            # Общая информация
            session_info = self.db_manager.get_session_info(self.get_current_session_id())
            if session_info:
                start_time, actions_count = session_info
                info_text = f"Начало сессии: {start_time}\nВсего действий: {actions_count}"
                self.info_stats.setText(info_text)

            # История действий
            self.load_history()

        except Exception as e:
            print(f"Ошибка загрузки статистики: {e}")

    def load_history(self):
        """Загружает историю действий в таблицу"""
        try:
            history = self.db_manager.get_actions_history(self.get_current_session_id())
            self.history_table.setRowCount(len(history))
            
            for row, action in enumerate(history):
                time, tool, color, size = action
                self.history_table.setItem(row, 0, QTableWidgetItem(time))
                self.history_table.setItem(row, 1, QTableWidgetItem(tool))
                self.history_table.setItem(row, 2, QTableWidgetItem(color))
                self.history_table.setItem(row, 3, QTableWidgetItem(str(size)))
                
        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")

    def get_current_session_id(self):
        """Получает ID текущей сессии из родительского окна"""
        parent = self.parent()
        if hasattr(parent, 'current_session_id'):
            return parent.current_session_id
        return None