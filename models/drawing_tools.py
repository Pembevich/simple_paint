from PyQt6.QtGui import QPainter, QPen, QColor, QImage
from PyQt6.QtCore import QPoint, QRect, Qt
from collections import deque

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
        pen = QPen(color, brush_size, cap=Qt.PenCapStyle.RoundCap)
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
        pen = QPen(QColor(255, 255, 255), brush_size, cap=Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(start_point, end_point)

class FillTool(DrawingTool):
    def __init__(self):
        super().__init__()
        self.name = "fill"
    
    def draw(self, painter, start_point, end_point, color, brush_size):
        """Реализация заливки области"""
        pass
    
    def flood_fill(self, image, start_point, new_color):
        """Алгоритм заливки области (flood fill)"""
        try:
            old_color = image.pixelColor(start_point.x(), start_point.y())
            
            if old_color == new_color:
                return False
            
            queue = deque([start_point])
            visited = set()
            
            while queue:
                point = queue.popleft()
                x, y = point.x(), point.y()
                
                # Проверяем границы изображения
                if (x < 0 or x >= image.width() or 
                    y < 0 or y >= image.height()):
                    continue
                
                if (x, y) in visited:
                    continue
                
                if image.pixelColor(x, y) != old_color:
                    continue
                image.setPixelColor(x, y, new_color)
                visited.add((x, y))
                queue.append(QPoint(x + 1, y))
                queue.append(QPoint(x - 1, y))
                queue.append(QPoint(x, y + 1))
                queue.append(QPoint(x, y - 1))
            
            return True
            
        except Exception as e:
            print(f"Ошибка при заливке: {e}")
            return False