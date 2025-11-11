from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QImage
import os

class FileManager:
    @staticmethod
    def save_image(image, parent_window):
        """Сохраняет изображение в файл"""
        try:
            filename, selected_filter = QFileDialog.getSaveFileName(
                parent_window,
                "Сохранить изображение",
                "my_drawing.png",
                "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;BMP Files (*.bmp);;All Files (*)"
            )
            
            if filename:
                # Определяем формат по расширению
                format_name = "PNG"  # по умолчанию
                if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                    format_name = "JPEG"
                elif filename.lower().endswith('.bmp'):
                    format_name = "BMP"
                
                success = image.save(filename, format_name)
                if success:
                    QMessageBox.information(parent_window, "Успех", f"Изображение сохранено как {format_name}!")
                    return True
                else:
                    QMessageBox.warning(parent_window, "Ошибка", "Не удалось сохранить изображение")
                    return False
            return False
        except Exception as e:
            QMessageBox.critical(parent_window, "Ошибка", f"Ошибка при сохранении: {str(e)}")
            return False

    @staticmethod
    def load_image(parent_window):
        """Загружает изображение из файла"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                parent_window,
                "Открыть изображение",
                "",
                "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
            )
            
            if filename:
                image = QImage(filename)
                if not image.isNull():
                    QMessageBox.information(parent_window, "Успех", "Изображение загружено!")
                    return image
                else:
                    QMessageBox.warning(parent_window, "Ошибка", "Не удалось загрузить изображение или формат не поддерживается")
                    return None
            return None
        except Exception as e:
            QMessageBox.critical(parent_window, "Ошибка", f"Ошибка при загрузке: {str(e)}")
            return None

    @staticmethod
    def export_to_png(image, parent_window):
        """Экспорт в PNG с настройками"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                parent_window,
                "Экспорт в PNG",
                "drawing.png",
                "PNG Files (*.png)"
            )
            
            if filename:
                success = image.save(filename, "PNG")
                if success:
                    return True
                else:
                    QMessageBox.warning(parent_window, "Ошибка", "Не удалось экспортировать изображение")
                    return False
            return False
        except Exception as e:
            QMessageBox.critical(parent_window, "Ошибка", f"Ошибка при экспорте: {str(e)}")
            return False