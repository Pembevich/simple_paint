from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QImage
from models.drawing_tools import BrushTool, LineTool, RectangleTool, EllipseTool, EraserTool, FillTool

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
        self.temp_image = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.rect())
        
        if self.drawing and self.temp_image:
            painter.drawImage(self.rect(), self.temp_image, self.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            self.start_point = event.pos()
            
            # Для заливки - выполняем сразу при клике
            if self.current_tool.name == "fill":
                self.perform_fill(event.pos())
                self.drawing = False
            else:
                self.temp_image = QImage(self.size(), QImage.Format.Format_ARGB32)
                self.temp_image.fill(Qt.GlobalColor.transparent)

    def mouseMoveEvent(self, event):
        if self.drawing and self.current_tool.name != "fill":
            if self.current_tool.name in ["brush", "eraser"]:
                painter = QPainter(self.image)
                self.current_tool.draw(painter, self.last_point, event.pos(), 
                                     self.current_color, self.brush_size)
                self.last_point = event.pos()
                self.update()
            else:
                self.temp_image.fill(Qt.GlobalColor.transparent)
                painter = QPainter(self.temp_image)
                self.current_tool.draw(painter, self.start_point, event.pos(),
                                     self.current_color, self.brush_size)
                self.update()

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.MouseButton.LeftButton and 
            self.drawing and self.current_tool.name != "fill"):
            if self.current_tool.name not in ["brush", "eraser"]:
                painter = QPainter(self.image)
                self.current_tool.draw(painter, self.start_point, event.pos(),
                                     self.current_color, self.brush_size)
            self.temp_image = None
            self.update()
            self.drawing = False

    def perform_fill(self, point):
        """Выполняет заливку области"""
        if self.current_tool.name == "fill" and hasattr(self.current_tool, 'flood_fill'):
            success = self.current_tool.flood_fill(self.image, point, self.current_color)
            if success:
                self.update()
            else:
                print("Заливка не выполнена")

    def clear(self):
        self.image.fill(Qt.GlobalColor.white)
        self.update()

    def set_tool(self, tool):
        self.current_tool = tool

    def set_color(self, color):
        self.current_color = color

    def set_brush_size(self, size):
        self.brush_size = size