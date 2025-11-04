class DrawingTool:
    def __init__(self):
        pass
    
    def draw(self, painter, start_point, end_point):
        pass

class BrushTool(DrawingTool):
    def draw(self, painter, start_point, end_point):
        # Здесь будет логика рисования кистью
        pass

class LineTool(DrawingTool):
    def draw(self, painter, start_point, end_point):
        # Здесь будет логика рисования линии
        pass