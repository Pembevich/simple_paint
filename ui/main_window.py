from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, 
                             QSlider, QMenuBar, QStatusBar, 
                             QMessageBox, QFileDialog, QColorDialog)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction, QPainter, QColor, QPen, QImage
from models.drawing_tools import BrushTool, LineTool, RectangleTool, EllipseTool, EraserTool
from utils.settings_manager import SettingsManager

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.image = QImage(self.size(), QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)
        self.drawing = False
        self.last_point = QPoint()
        self.current_tool = BrushTool()
        self.current_color = QColor(0, 0, 0)
        self.brush_size = 5

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.image)
            self.current_tool.draw(painter, self.last_point, event.pos(), 
                                 self.current_color, self.brush_size)
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def clear(self):
        self.image.fill(Qt.GlobalColor.white)
        self.update()

    def set_tool(self, tool):
        self.current_tool = tool

    def set_color(self, color):
        self.current_color = color

    def set_brush_size(self, size):
        self.brush_size = size

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager()
        self.setWindowTitle("SimplePaint")
        self.setGeometry(100, 100, 800, 600)
        
        self.current_color = QColor(0, 0, 0)
        self.brush_size = 5
        self.current_tool = "brush"
        
        self.setup_ui()
        self.load_settings()
        
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
        self.clear_btn = QPushButton("Очистить")
        
        tools_layout.addWidget(self.brush_btn)
        tools_layout.addWidget(self.line_btn)
        tools_layout.addWidget(self.rect_btn)
        tools_layout.addWidget(self.ellipse_btn)
        tools_layout.addWidget(self.eraser_btn)
        tools_layout.addWidget(self.clear_btn)
        tools_layout.addStretch()
        
        # Правая часть (холст и настройки)
        right_layout = QVBoxLayout()
        
        # Панель настроек
        settings_layout = QHBoxLayout()
        settings_layout.addWidget(QLabel("Цвет:"))
        
        # Кнопки цветов
        self.red_btn = QPushButton()
        self.red_btn.setStyleSheet("background-color: red; border: 1px solid black;")
        self.red_btn.setFixedSize(30, 30)
        
        self.blue_btn = QPushButton()
        self.blue_btn.setStyleSheet("background-color: blue; border: 1px solid black;")
        self.blue_btn.setFixedSize(30, 30)
        
        self.green_btn = QPushButton()
        self.green_btn.setStyleSheet("background-color: green; border: 1px solid black;")
        self.green_btn.setFixedSize(30, 30)
        
        self.black_btn = QPushButton()
        self.black_btn.setStyleSheet("background-color: black; border: 1px solid black;")
        self.black_btn.setFixedSize(30, 30)
        
        self.custom_color_btn = QPushButton("Другой")
        self.custom_color_btn.setFixedSize(60, 30)
        
        settings_layout.addWidget(self.red_btn)
        settings_layout.addWidget(self.blue_btn)
        settings_layout.addWidget(self.green_btn)
        settings_layout.addWidget(self.black_btn)
        settings_layout.addWidget(self.custom_color_btn)
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
        
        # Холст
        self.canvas = CanvasWidget()
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
        
        self.new_action = QAction("Новый", self)
        self.open_action = QAction("Открыть", self)
        self.save_action = QAction("Сохранить", self)
        exit_action = QAction("Выход", self)
        
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # Меню Правка
        edit_menu = menubar.addMenu("Правка")
        self.clear_action = QAction("Очистить", self)
        edit_menu.addAction(self.clear_action)
        
        # Меню Справка
        help_menu = menubar.addMenu("Справка")
        about_action = QAction("О программе", self)
        help_menu.addAction(about_action)
        
        # Подключаем выход и о программе
        exit_action.triggered.connect(self.close)
        about_action.triggered.connect(self.show_about)
    
    def connect_signals(self):
        # Инструменты
        self.brush_btn.clicked.connect(lambda: self.set_tool("brush"))
        self.line_btn.clicked.connect(lambda: self.set_tool("line"))
        self.rect_btn.clicked.connect(lambda: self.set_tool("rectangle"))
        self.ellipse_btn.clicked.connect(lambda: self.set_tool("ellipse"))
        self.eraser_btn.clicked.connect(lambda: self.set_tool("eraser"))
        self.clear_btn.clicked.connect(self.clear_canvas)
        
        # Цвета
        self.red_btn.clicked.connect(lambda: self.set_color(QColor(255, 0, 0)))
        self.blue_btn.clicked.connect(lambda: self.set_color(QColor(0, 0, 255)))
        self.green_btn.clicked.connect(lambda: self.set_color(QColor(0, 255, 0)))
        self.black_btn.clicked.connect(lambda: self.set_color(QColor(0, 0, 0)))
        self.custom_color_btn.clicked.connect(self.choose_custom_color)
        
        # Размер кисти
        self.size_slider.valueChanged.connect(self.set_brush_size)
        
        # Меню
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.clear_action.triggered.connect(self.clear_canvas)
    
    def load_settings(self):
        """Загружает настройки при запуске"""
        # Загрузка размера окна
        size = self.settings_manager.get_setting("window_size")
        if size:
            self.resize(size[0], size[1])
        
        # Загрузка последнего инструмента
        last_tool = self.settings_manager.get_setting("last_tool")
        if last_tool:
            self.set_tool(last_tool)
        
        # Загрузка последнего цвета
        last_color = self.settings_manager.get_setting("last_color")
        if last_color:
            color = QColor(last_color[0], last_color[1], last_color[2])
            self.set_color(color)
        
        # Загрузка размера кисти
        brush_size = self.settings_manager.get_setting("brush_size")
        if brush_size:
            self.set_brush_size(brush_size)
            self.size_slider.setValue(brush_size)
    
    def set_tool(self, tool):
        self.current_tool = tool
        if tool == "brush":
            self.canvas.set_tool(BrushTool())
        elif tool == "line":
            self.canvas.set_tool(LineTool())
        elif tool == "rectangle":
            self.canvas.set_tool(RectangleTool())
        elif tool == "ellipse":
            self.canvas.set_tool(EllipseTool())
        elif tool == "eraser":
            self.canvas.set_tool(EraserTool())
        self.update_status()
        self.settings_manager.set_setting("last_tool", tool)
    
    def set_color(self, color):
        self.current_color = color
        self.canvas.set_color(color)
        self.update_status()
        # Сохраняем цвет в настройках
        self.settings_manager.set_setting("last_color", 
                                         [color.red(), color.green(), color.blue()])
    
    def set_brush_size(self, size):
        self.brush_size = size
        self.size_label.setText(f"{size}px")
        self.canvas.set_brush_size(size)
        self.update_status()
        self.settings_manager.set_setting("brush_size", size)
    
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
    
    def new_file(self):
        """Создает новый файл"""
        self.canvas.clear()
    
    def open_file(self):
        """Открывает изображение"""
        from utils.file_manager import FileManager
        image = FileManager.load_image(self)
        if image:
            self.canvas.image = image.scaled(self.canvas.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.canvas.update()
    
    def save_file(self):
        """Сохраняет изображение"""
        from utils.file_manager import FileManager
        FileManager.save_image(self.canvas.image, self)
    
    def clear_canvas(self):
        """Очищает холст"""
        self.canvas.clear()
    
    def choose_custom_color(self):
        """Выбор произвольного цвета"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_color(color)
    
    def show_about(self):
        """Показывает окно 'О программе'"""
        QMessageBox.about(self, "О программе SimplePaint", 
                         "SimplePaint - простой графический редактор\n\n"
                         "Разработано в рамках учебного проекта\n"
                         "Возможности:\n"
                         "- Рисование кистью\n" 
                         "- Геометрические фигуры\n"
                         "- Сохранение и загрузка изображений\n"
                         "- Сохранение настроек между запусками")
    
    def closeEvent(self, event):
        """Сохраняет настройки при закрытии"""
        self.settings_manager.set_setting("window_size", [self.width(), self.height()])
        self.settings_manager.set_setting("last_tool", self.current_tool)
        self.settings_manager.set_setting("last_color", 
                                         [self.current_color.red(), 
                                          self.current_color.green(), 
                                          self.current_color.blue()])
        self.settings_manager.set_setting("brush_size", self.brush_size)
        event.accept()