from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QImage, QCursor
from PyQt6.QtCore import Qt
from models.drawing_tools import BrushTool, LineTool, RectangleTool, EllipseTool, EraserTool


class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.image = QImage(self.size(), QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)
        self.drawing = False
        self.last_point = QPoint()
        self.start_point = QPoint()
        self.current_tool = BrushTool()
        self.current_color = QColor(0, 0, 0)
        self.brush_size = 5
        self.temp_image = None  # Для временного предпросмотра
        
        # Устанавливаем курсор по умолчанию
        self.update_cursor()

    def paintEvent(self, event):
        painter = QPainter(self)
        # Рисуем основное изображение
        painter.drawImage(self.rect(), self.image, self.rect())
        
        # Если рисуем фигуру - рисуем временный предпросмотр
        if self.drawing and self.temp_image:
            painter.drawImage(self.rect(), self.temp_image, self.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            self.start_point = event.pos()
            # Создаем временное изображение для предпросмотра
            self.temp_image = QImage(self.size(), QImage.Format.Format_ARGB32)
            self.temp_image.fill(Qt.GlobalColor.transparent)

    def mouseMoveEvent(self, event):
        if self.drawing:
            # Для кисти и ластика рисуем сразу
            if self.current_tool.name in ["brush", "eraser"]:
                painter = QPainter(self.image)
                self.current_tool.draw(painter, self.last_point, event.pos(), 
                                     self.current_color, self.brush_size)
                self.last_point = event.pos()
                self.update()
            # Для фигур - рисуем предпросмотр
            else:
                # Очищаем временное изображение
                self.temp_image.fill(Qt.GlobalColor.transparent)
                painter = QPainter(self.temp_image)
                # Рисуем фигуру на временном изображении
                self.current_tool.draw(painter, self.start_point, event.pos(),
                                     self.current_color, self.brush_size)
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            # Для фигур - рисуем окончательно на основном изображении
            if self.current_tool.name not in ["brush", "eraser"]:
                painter = QPainter(self.image)
                self.current_tool.draw(painter, self.start_point, event.pos(),
                                     self.current_color, self.brush_size)
            # Очищаем временное изображение
            self.temp_image = None
            self.update()
            self.drawing = False

    def clear(self):
        self.image.fill(Qt.GlobalColor.white)
        self.update()

    def set_tool(self, tool):
        self.current_tool = tool
        self.update_cursor()

    def set_color(self, color):
        self.current_color = color

    def set_brush_size(self, size):
        self.brush_size = size

    def update_cursor(self):
        """Обновляет курсор в зависимости от выбранного инструмента"""
        if self.current_tool.name == "brush":
            # Создаем курсор кисти (крестик)
            pixmap = QImage(32, 32, QImage.Format.Format_ARGB32)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawLine(16, 0, 16, 32)  # Вертикальная линия
            painter.drawLine(0, 16, 32, 16)  # Горизонтальная линия
            painter.end()
            cursor = QCursor(pixmap, 16, 16)  # Центр курсора
        elif self.current_tool.name == "eraser":
            # Курсор круга для ластика
            self.setCursor(Qt.CursorShape.CrossCursor)
        elif self.current_tool.name == "line":
            self.setCursor(Qt.CursorShape.CrossCursor)
        elif self.current_tool.name == "rectangle":
            self.setCursor(Qt.CursorShape.CrossCursor)
        elif self.current_tool.name == "ellipse":
            self.setCursor(Qt.CursorShape.CrossCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)