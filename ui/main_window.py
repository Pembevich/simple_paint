from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, 
                             QSlider, QMenuBar, QStatusBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPainter, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SimplePaint")
        self.setGeometry(100, 100, 800, 600)
        
        self.current_color = QColor(0, 0, 0)  # Черный по умолчанию
        self.brush_size = 5
        self.current_tool = "brush"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Левая панель инструментов
        tools_layout = QVBoxLayout()
        
        # Кнопки инструментов
        self.brush_btn = QPushButton("Кисть")
        self.line_btn = QPushButton("Линия")
        self.rect_btn = QPushButton("Прямоугольник")
        self.ellipse_btn = QPushButton("Эллипс")
        self.eraser_btn = QPushButton("Ластик")
        
        tools_layout.addWidget(self.brush_btn)
        tools_layout.addWidget(self.line_btn)
        tools_layout.addWidget(self.rect_btn)
        tools_layout.addWidget(self.ellipse_btn)
        tools_layout.addWidget(self.eraser_btn)
        tools_layout.addStretch()
        
        # Правая часть (холст и настройки)
        right_layout = QVBoxLayout()
        
        # Панель настроек
        settings_layout = QHBoxLayout()
        settings_layout.addWidget(QLabel("Цвет:"))
        
        # Кнопки цветов
        self.red_btn = QPushButton()
        self.red_btn.setStyleSheet("background-color: red;")
        self.red_btn.setFixedSize(30, 30)
        
        self.blue_btn = QPushButton()
        self.blue_btn.setStyleSheet("background-color: blue;")
        self.blue_btn.setFixedSize(30, 30)
        
        self.green_btn = QPushButton()
        self.green_btn.setStyleSheet("background-color: green;")
        self.green_btn.setFixedSize(30, 30)
        
        self.black_btn = QPushButton()
        self.black_btn.setStyleSheet("background-color: black;")
        self.black_btn.setFixedSize(30, 30)
        
        settings_layout.addWidget(self.red_btn)
        settings_layout.addWidget(self.blue_btn)
        settings_layout.addWidget(self.green_btn)
        settings_layout.addWidget(self.black_btn)
        settings_layout.addStretch()
        
        # Слайдер размера кисти
        settings_layout.addWidget(QLabel("Размер:"))
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setRange(1, 50)
        self.size_slider.setValue(5)
        settings_layout.addWidget(self.size_slider)
        
        self.size_label = QLabel("5px")
        settings_layout.addWidget(self.size_label)
        
        right_layout.addLayout(settings_layout)
        
        # Холст (пока просто виджет)
        self.canvas = QWidget()
        self.canvas.setStyleSheet("background-color: white; border: 1px solid gray;")
        right_layout.addWidget(self.canvas)
        
        # Собираем основное окно
        main_layout.addLayout(tools_layout)
        main_layout.addLayout(right_layout)
        
        # Строка состояния
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status()
        
        # Создаем меню
        self.create_menu()
        
        # Подключаем сигналы
        self.connect_signals()
    
    def create_menu(self):
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("Файл")
        
        new_action = QAction("Новый", self)
        open_action = QAction("Открыть", self)
        save_action = QAction("Сохранить", self)
        exit_action = QAction("Выход", self)
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # Меню Правка
        edit_menu = menubar.addMenu("Правка")
        clear_action = QAction("Очистить", self)
        edit_menu.addAction(clear_action)
        
        # Меню Справка
        help_menu = menubar.addMenu("Справка")
        about_action = QAction("О программе", self)
        help_menu.addAction(about_action)
    
    def connect_signals(self):
        # Инструменты
        self.brush_btn.clicked.connect(lambda: self.set_tool("brush"))
        self.line_btn.clicked.connect(lambda: self.set_tool("line"))
        self.rect_btn.clicked.connect(lambda: self.set_tool("rectangle"))
        self.ellipse_btn.clicked.connect(lambda: self.set_tool("ellipse"))
        self.eraser_btn.clicked.connect(lambda: self.set_tool("eraser"))
        
        # Цвета
        self.red_btn.clicked.connect(lambda: self.set_color(QColor(255, 0, 0)))
        self.blue_btn.clicked.connect(lambda: self.set_color(QColor(0, 0, 255)))
        self.green_btn.clicked.connect(lambda: self.set_color(QColor(0, 255, 0)))
        self.black_btn.clicked.connect(lambda: self.set_color(QColor(0, 0, 0)))
        
        # Размер кисти
        self.size_slider.valueChanged.connect(self.set_brush_size)
    
    def set_tool(self, tool):
        self.current_tool = tool
        self.update_status()
        print(f"Выбран инструмент: {tool}")  # Для отладки
    
    def set_color(self, color):
        self.current_color = color
        self.update_status()
        print(f"Выбран цвет: {color.getRgb()}")  # Для отладки
    
    def set_brush_size(self, size):
        self.brush_size = size
        self.size_label.setText(f"{size}px")
        self.update_status()
    
    def update_status(self):
        color_name = self.get_color_name()
        self.status_bar.showMessage(f"Инструмент: {self.current_tool} | Цвет: {color_name} | Размер: {self.brush_size}px")
    
    def get_color_name(self):
        if self.current_color == QColor(255, 0, 0):
            return "красный"
        elif self.current_color == QColor(0, 0, 255):
            return "синий"
        elif self.current_color == QColor(0, 255, 0):
            return "зеленый"
        elif self.current_color == QColor(0, 0, 0):
            return "черный"
        else:
            return "пользовательский"