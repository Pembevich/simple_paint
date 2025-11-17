import json
import os

class SettingsManager:
    def __init__(self):
        self.data_dir = "data"
        self.settings_file = os.path.join(self.data_dir, "app_settings.json")
        self.default_settings = {
            "window_size": [800, 600],
            "last_color": [0, 0, 0],
            "brush_size": 5,
            "last_tool": "brush",
            "recent_files": []
        }
        
        # Создаем папку data если её нет
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.settings = self.load_settings()

    def load_settings(self):
        """Загружает настройки из файла"""
        try:
            if os.path.exists(self.settings_file):
                print(f"Найден файл настроек: {self.settings_file}")
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    print("Настройки загружены:", settings)
                    return settings
            else:
                print("Файл настроек не найден, используются настройки по умолчанию")
                return self.default_settings.copy()
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
            return self.default_settings.copy()

    def save_settings(self):
        """Сохраняет настройки в файл"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            print("Настройки сохранены:", self.settings)
            return True
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
            return False

    def get_setting(self, key):
        """Получает значение настройки"""
        value = self.settings.get(key, self.default_settings.get(key))
        print(f"Получена настройка {key}: {value}")
        return value

    def set_setting(self, key, value):
        """Устанавливает значение настройки"""
        print(f"Установка настройки {key}: {value}")
        self.settings[key] = value
        self.save_settings()

    def add_recent_file(self, filepath):
        """Добавляет файл в список недавних"""
        if filepath in self.settings["recent_files"]:
            self.settings["recent_files"].remove(filepath)
        self.settings["recent_files"].insert(0, filepath)
        self.settings["recent_files"] = self.settings["recent_files"][:5]
        self.save_settings()