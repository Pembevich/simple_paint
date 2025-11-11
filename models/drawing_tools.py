from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import QPoint, QRect

class DrawingTool:
    def __init__(self):
        self.name = "base_tool"
    
    def draw(self, painter, start_point, end_point, color, brush_size):
        pass

class BrushTool(DrawingTool):
    def __init__(self):
        super().__init__()
        self.name = "brush"
    
    def draw(self, painter, start_point, end_point, color, brush_size):
        pen = QPen(color, brush_size)
        painter.setPen(pen)
        painter.drawLine(start_point, end_point)

class LineTool(DrawingTool):
    def __init__(self):
        super().__init__()
        self.name = "line"
    
    def draw(self, painter, start_point, end_point, color, brush_size):
        pen = QPen(color, brush_size)
        painter.setPen(pen)
        painter.drawLine(start_point, end_point)

class RectangleTool(DrawingTool):
    def __init__(self):
        super().__init__()
        self.name = "rectangle"
    
    def draw(self, painter, start_point, end_point, color, brush_size):
        pen = QPen(color, brush_size)
        painter.setPen(pen)
        rect = QRect(start_point, end_point)
        painter.drawRect(rect)

class EllipseTool(DrawingTool):
    def __init__(self):
        super().__init__()
        self.name = "ellipse"
    
    def draw(self, painter, start_point, end_point, color, brush_size):
        pen = QPen(color, brush_size)
        painter.setPen(pen)
        rect = QRect(start_point, end_point)
        painter.drawEllipse(rect)

class EraserTool(DrawingTool):
    def __init__(self):
        super().__init__()
        self.name = "eraser"
    
    def draw(self, painter, start_point, end_point, color, brush_size):
        pen = QPen(QColor(255, 255, 255), brush_size)
        painter.setPen(pen)
        painter.drawLine(start_point, end_point)