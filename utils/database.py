import sqlite3
import datetime
import os
from PyQt6.QtGui import QColor

class DatabaseManager:
    def __init__(self):
        self.data_dir = "data"
        self.db_file = os.path.join(self.data_dir, 'paint_history.db')
        
        # Создаем папку data если её нет
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.conn = sqlite3.connect(self.db_file)
        self.create_tables()

    def create_tables(self):
        """Создает таблицы в базе данных"""
        cursor = self.conn.cursor()
        
        # Таблица сессий рисования
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drawing_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                tools_used TEXT
            )
        ''')
        
        # Таблица действий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drawing_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                tool_name TEXT NOT NULL,
                color TEXT NOT NULL,
                brush_size INTEGER,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES drawing_sessions (id)
            )
        ''')
        
        # Таблица сохраненных файлов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saved_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                filename TEXT NOT NULL,
                file_format TEXT NOT NULL,
                save_time TEXT NOT NULL,
                file_size INTEGER,
                FOREIGN KEY (session_id) REFERENCES drawing_sessions (id)
            )
        ''')
        
        self.conn.commit()

    def start_session(self):
        """Начинает новую сессию рисования"""
        try:
            cursor = self.conn.cursor()
            start_time = datetime.datetime.now().isoformat()
            cursor.execute(
                'INSERT INTO drawing_sessions (start_time) VALUES (?)',
                (start_time,)
            )
            self.conn.commit()
            session_id = cursor.lastrowid
            print(f"Сессия #{session_id} начата в {start_time}")
            return session_id
        except Exception as e:
            print(f"Ошибка начала сессии: {e}")
            return 1

    def log_action(self, session_id, tool_name, color, brush_size):
        """Логирует действие рисования"""
        try:
            cursor = self.conn.cursor()
            timestamp = datetime.datetime.now().isoformat()
            
            # Конвертируем QColor в строку
            if isinstance(color, QColor):
                color_str = f"{color.red()},{color.green()},{color.blue()}"
            else:
                color_str = str(color)
            
            cursor.execute(
                '''INSERT INTO drawing_actions 
                   (session_id, tool_name, color, brush_size, timestamp) 
                   VALUES (?, ?, ?, ?, ?)''',
                (session_id, tool_name, color_str, brush_size, timestamp)
            )
            self.conn.commit()
            print(f"Действие записано: {tool_name}, цвет: {color_str}, размер: {brush_size}")
        except Exception as e:
            print(f"Ошибка записи действия: {e}")

    def log_file_save(self, session_id, filename, file_format, file_size=0):
        """Логирует сохранение файла"""
        try:
            cursor = self.conn.cursor()
            save_time = datetime.datetime.now().isoformat()
            cursor.execute(
                '''INSERT INTO saved_files 
                   (session_id, filename, file_format, save_time, file_size) 
                   VALUES (?, ?, ?, ?, ?)''',
                (session_id, filename, file_format, save_time, file_size)
            )
            self.conn.commit()
            print(f"Сохранение файла записано: {filename}")
        except Exception as e:
            print(f"Ошибка записи информации о файле: {e}")

    def end_session(self, session_id):
        """Завершает сессию рисования"""
        try:
            cursor = self.conn.cursor()
            end_time = datetime.datetime.now().isoformat()
            cursor.execute(
                'UPDATE drawing_sessions SET end_time = ? WHERE id = ?',
                (end_time, session_id)
            )
            self.conn.commit()
            print(f"Сессия #{session_id} завершена в {end_time}")
        except Exception as e:
            print(f"Ошибка завершения сессии: {e}")

    def get_tools_stats(self, session_id):
        """Получает статистику по использованию инструментов"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT tool_name, COUNT(*) as usage_count 
                FROM drawing_actions 
                WHERE session_id = ? 
                GROUP BY tool_name
                ORDER BY usage_count DESC
            ''', (session_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения статистики инструментов: {e}")
            return []

    def get_colors_stats(self, session_id):
        """Получает статистику по использованию цветов"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT color, COUNT(*) as usage_count 
                FROM drawing_actions 
                WHERE session_id = ? 
                GROUP BY color
                ORDER BY usage_count DESC
            ''', (session_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения статистики цветов: {e}")
            return []

    def get_session_info(self, session_id):
        """Получает информацию о сессии"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT start_time, 
                       (SELECT COUNT(*) FROM drawing_actions WHERE session_id = ?) as actions_count
                FROM drawing_sessions 
                WHERE id = ?
            ''', (session_id, session_id))
            return cursor.fetchone()
        except Exception as e:
            print(f"Ошибка получения информации о сессии: {e}")
            return None

    def get_actions_history(self, session_id, limit=50):
        """Получает историю действий"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT timestamp, tool_name, color, brush_size
                FROM drawing_actions 
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (session_id, limit))
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения истории действий: {e}")
            return []

    def get_saved_files(self, session_id):
        """Получает список сохраненных файлов"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT filename, file_format, save_time, file_size
                FROM saved_files 
                WHERE session_id = ?
                ORDER BY save_time DESC
            ''', (session_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения списка файлов: {e}")
            return []

    def get_all_sessions(self):
        """Получает список всех сессий"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, start_time, end_time,
                       (SELECT COUNT(*) FROM drawing_actions WHERE session_id = drawing_sessions.id) as actions_count
                FROM drawing_sessions 
                ORDER BY start_time DESC
            ''')
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения списка сессий: {e}")
            return []

    def get_session_duration(self, session_id):
        """Получает продолжительность сессии"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT start_time, end_time 
                FROM drawing_sessions 
                WHERE id = ?
            ''', (session_id,))
            result = cursor.fetchone()
            if result and result[1]:
                start = datetime.datetime.fromisoformat(result[0])
                end = datetime.datetime.fromisoformat(result[1])
                duration = end - start
                return str(duration).split('.')[0]
            return "В процессе"
        except Exception as e:
            print(f"Ошибка получения продолжительности сессии: {e}")
            return "Неизвестно"

    def get_most_used_tool_all_time(self):
        """Получает самый популярный инструмент за все время"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT tool_name, COUNT(*) as usage_count 
                FROM drawing_actions 
                GROUP BY tool_name
                ORDER BY usage_count DESC
                LIMIT 1
            ''')
            return cursor.fetchone()
        except Exception as e:
            print(f"Ошибка получения самого популярного инструмента: {e}")
            return None

    def get_total_actions_count(self):
        """Получает общее количество действий за все время"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM drawing_actions')
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Ошибка получения общего количества действий: {e}")
            return 0

    def clear_old_data(self, days=30):
        """Очищает данные старше указанного количества дней"""
        try:
            cursor = self.conn.cursor()
            cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()
            
            cursor.execute('''
                DELETE FROM drawing_actions 
                WHERE session_id IN (
                    SELECT id FROM drawing_sessions 
                    WHERE start_time < ?
                )
            ''', (cutoff_date,))
            
            cursor.execute('''
                DELETE FROM saved_files 
                WHERE session_id IN (
                    SELECT id FROM drawing_sessions 
                    WHERE start_time < ?
                )
            ''', (cutoff_date,))
            
            cursor.execute('DELETE FROM drawing_sessions WHERE start_time < ?', (cutoff_date,))
            
            self.conn.commit()
            print(f"Данные старше {days} дней очищены")
        except Exception as e:
            print(f"Ошибка очистки старых данных: {e}")

    def get_database_size(self):
        """Получает размер файла базы данных"""
        try:
            if os.path.exists(self.db_file):
                return os.path.getsize(self.db_file)
            return 0
        except Exception as e:
            print(f"Ошибка получения размера БД: {e}")
            return 0

    def close(self):
        """Закрывает соединение с БД"""
        try:
            self.conn.close()
            print("Соединение с БД закрыто")
        except Exception as e:
            print(f"Ошибка закрытия БД: {e}")