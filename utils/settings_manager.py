import json
import os

class SettingsManager:
    def __init__(self):
        self.settings_file = "app_settings.json"
        self.default_settings = {
            "window_size": [800, 600],
            "last_color": [0, 0, 0],
            "brush_size": 5,
            "last_tool": "brush",
            "recent_files": []
        }
        self.settings = self.load_settings()

    def load_settings(self):
        """Загружает настройки из файла"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.default_settings.copy()
        except Exception:
            return self.default_settings.copy()

    def save_settings(self):
        """Сохраняет настройки в файл"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
            return False

    def get_setting(self, key):
        """Получает значение настройки"""
        return self.settings.get(key, self.default_settings.get(key))

    def set_setting(self, key, value):
        """Устанавливает значение настройки"""
        self.settings[key] = value
        self.save_settings()

    def add_recent_file(self, filepath):
        """Добавляет файл в список недавних"""
        if filepath in self.settings["recent_files"]:
            self.settings["recent_files"].remove(filepath)
        self.settings["recent_files"].insert(0, filepath)
        self.settings["recent_files"] = self.settings["recent_files"][:5]  # максимум 5 файлов
        self.save_settings()