from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QImage

class FileManager:
    @staticmethod
    def save_image(image, parent_window):
        """Сохраняет изображение в файл"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                parent_window,
                "Сохранить изображение",
                "my_drawing.png",
                "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg)"
            )
            
            if filename:
                success = image.save(filename)
                if success:
                    QMessageBox.information(parent_window, "Успех", "Изображение сохранено!")
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
                "Images (*.png *.jpg *.jpeg *.bmp)"
            )
            
            if filename:
                image = QImage(filename)
                if not image.isNull():
                    QMessageBox.information(parent_window, "Успех", "Изображение загружено!")
                    return image
                else:
                    QMessageBox.warning(parent_window, "Ошибка", "Не удалось загрузить изображение")
                    return None
            return None
        except Exception as e:
            QMessageBox.critical(parent_window, "Ошибка", f"Ошибка при загрузке: {str(e)}")
            return None